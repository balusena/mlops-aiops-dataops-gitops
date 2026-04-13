# Batch-ML-Systems

# Batch ML system
# runs every 1–5 minutes
# fetches data from Elasticsearch + Prometheus
# builds dataset
# trains model again and again



import requests
import pandas as pd
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from sklearn.ensemble import IsolationForest

# -----------------------------
# CONFIG
# -----------------------------
ES_HOST = "http://localhost:9200"
ES_INDEX = "filebeat-*"
PROM_URL = "http://localhost:9090"

SERVICES = ["catalogue", "user", "cart", "shipping", "payment"]

es = Elasticsearch(ES_HOST)

# -----------------------------
# FETCH LOGS (1-MIN WINDOW)
# -----------------------------
def fetch_logs():
    now = datetime.utcnow()
    past = now - timedelta(minutes=1)

    query = {
        "query": {
            "range": {
                "@timestamp": {
                    "gte": past.isoformat(),
                    "lte": now.isoformat()
                }
            }
        }
    }

    res = es.search(index=ES_INDEX, body=query, size=10000)
    logs = [h["_source"] for h in res["hits"]["hits"]]

    df = pd.DataFrame(logs)

    if df.empty:
        return df

    df["service"] = df["url"].str.extract(r"/api/([^/]+)/")
    return df


# -----------------------------
# PROMETHEUS QUERY
# -----------------------------
def query_promql(query):
    try:
        r = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query})
        return float(r.json()["data"]["result"][0]["value"][1])
    except:
        return 0.0


# -----------------------------
# FETCH METRICS PER SERVICE
# -----------------------------
def fetch_metrics(service):
    return {
        "cpu_usage": query_promql(
            f'rate(container_cpu_usage_seconds_total{{container="{service}"}}[1m])'
        ),
        "memory_usage": query_promql(
            f'container_memory_usage_bytes{{container="{service}"}}'
        ),
        "request_rate": query_promql(
            f'rate(http_requests_total{{service="{service}"}}[1m])'
        )
    }


# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
def build_features(df):
    results = []

    for service in SERVICES:
        svc_df = df[df["service"] == service]

        if svc_df.empty:
            continue

        svc_df["status"] = pd.to_numeric(svc_df["status"], errors="coerce")
        svc_df["request_time"] = pd.to_numeric(svc_df["request_time"], errors="coerce")
        svc_df["upstream_response_time"] = pd.to_numeric(
            svc_df["upstream_response_time"], errors="coerce"
        )

        metrics = fetch_metrics(service)

        features = {
            "timestamp": datetime.utcnow(),
            "service": service,

            # Logs
            "req_count": len(svc_df),
            "error_rate": (svc_df["status"] >= 500).mean(),
            "client_error_rate": ((svc_df["status"] >= 400) & (svc_df["status"] < 500)).mean(),
            "avg_latency": svc_df["request_time"].mean(),
            "p95_latency": svc_df["request_time"].quantile(0.95),
            "avg_upstream_time": svc_df["upstream_response_time"].mean(),

            # Metrics
            "cpu_usage": metrics["cpu_usage"],
            "memory_usage": metrics["memory_usage"],
            "request_rate": metrics["request_rate"],
        }

        results.append(features)

    return pd.DataFrame(results)


# -----------------------------
# SAVE DATASET
# -----------------------------
def save(df, file="aiops_dataset.csv"):
    try:
        old = pd.read_csv(file)
        df = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(file, index=False)


# -----------------------------
# TRAIN MODEL PER SERVICE
# -----------------------------
def train_model(df):
    models = {}

    for service in df["service"].unique():
        svc_df = df[df["service"] == service].drop(columns=["service", "timestamp"])

        model = IsolationForest(contamination=0.05)
        model.fit(svc_df.fillna(0))

        df.loc[df["service"] == service, "anomaly"] = model.predict(svc_df.fillna(0))

        models[service] = model

    return models, df


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():
    logs_df = fetch_logs()

    if logs_df.empty:
        print("No logs in this window")
        return

    features_df = build_features(logs_df)

    if features_df.empty:
        return

    save(features_df)

    full_df = pd.read_csv("aiops_dataset.csv")

    models, result = train_model(full_df)

    print(result.tail())


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    run_pipeline()
