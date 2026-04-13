#  Streaming ML Systems (AIOps Real-Time System)

#   Streaming ML system (this project)
#   runs continuously in real time (event-driven)
#   consumes data from Kafka stream (aiops-stream)
#   maintains sliding window (e.g., 60 seconds per service)
#   builds features on the fly (req count, error rate, latency, CPU, memory)
#   applies trained Isolation Forest model in real time
#   detects anomalies instantly as data arrives
#   stores results into Elasticsearch
#   triggers alerts via Slack and PagerDuty
#   👉 This is REAL-TIME (not batch processing)

from kafka import KafkaConsumer
from collections import defaultdict, deque
from datetime import datetime
import pandas as pd
import numpy as np
import json
import requests

from sklearn.ensemble import IsolationForest
from elasticsearch import Elasticsearch

# =========================
# CONFIG
# =========================

KAFKA_TOPIC = "aiops-stream"
KAFKA_SERVER = "localhost:9092"

SERVICES = ["catalogue", "user", "cart", "shipping", "payment"]
WINDOW_SIZE = 60

# OpenTelemetry concept: data already arrives via Kafka
# (Collector pushes metrics/logs into Kafka topic)

es = Elasticsearch("http://localhost:9200")

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# =========================
# ALERT CONFIG
# =========================

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
PAGERDUTY_ROUTING_KEY = "your-pagerduty-key"

# =========================
# STATE
# =========================

windows = defaultdict(lambda: deque())
models = {s: IsolationForest(contamination=0.05) for s in SERVICES}
trained = {s: False for s in SERVICES}

# =========================
# SERVICE EXTRACTION
# =========================

def get_service(event):
    return event.get("service") or event.get("service_name") or "unknown"

# =========================
# SLIDING WINDOW (60s)
# =========================

def update_window(service, event):
    now = datetime.utcnow()
    windows[service].append((now, event))

    while windows[service] and (now - windows[service][0][0]).seconds > WINDOW_SIZE:
        windows[service].popleft()

# =========================
# FEATURE ENGINEERING
# =========================

def build_features(service):
    data = [e for _, e in windows[service]]

    if not data:
        return None

    df = pd.DataFrame(data)

    for col in ["status", "request_time", "cpu", "memory"]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return {
        "service": service,
        "timestamp": datetime.utcnow().isoformat(),

        "req_count": len(df),
        "error_rate": (df["status"] >= 500).mean() if "status" in df else 0,
        "avg_latency": df["request_time"].mean() if "request_time" in df else 0,
        "p95_latency": df["request_time"].quantile(0.95) if "request_time" in df else 0,
        "cpu": df["cpu"].mean() if "cpu" in df else 0,
        "memory": df["memory"].mean() if "memory" in df else 0,
    }

# =========================
# ML MODEL
# =========================

def predict(service, features):
    X = np.array([[
        features["req_count"],
        features["error_rate"],
        features["avg_latency"],
        features["p95_latency"],
        features["cpu"],
        features["memory"]
    ]])

    global models, trained

    if not trained[service]:
        models[service].fit(X)
        trained[service] = True
        return 1

    return models[service].predict(X)[0]

# =========================
# ELASTICSEARCH
# =========================

def send_to_es(features, score):
    doc = features.copy()
    doc["anomaly"] = int(score == -1)

    es.index(index="aiops-anomalies", document=doc)

# =========================
# ALERTING LAYER
# =========================

def send_slack_alert(features):
    message = {
        "text": f"🚨 AIOps Alert\nService: {features['service']}\nError Rate: {features['error_rate']:.2f}\nLatency: {features['avg_latency']:.2f}"
    }

    try:
        requests.post(SLACK_WEBHOOK_URL, json=message)
    except Exception as e:
        print("Slack alert failed:", e)


def send_pagerduty_alert(features):
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "payload": {
            "summary": f"AIOps anomaly detected in {features['service']}",
            "severity": "critical",
            "source": "aiops-engine"
        }
    }

    try:
        requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)
    except Exception as e:
        print("PagerDuty alert failed:", e)

# =========================
# ALERT DECISION LOGIC
# =========================

def trigger_alerts(features, score):
    if score == -1 and features["error_rate"] > 0.2:
        send_slack_alert(features)
        send_pagerduty_alert(features)

# =========================
# MAIN LOOP
# =========================

print("🚀 AIOps + OpenTelemetry + Kafka Engine Started...")

for msg in consumer:
    event = msg.value

    service = get_service(event)

    if service not in SERVICES:
        continue

    update_window(service, event)

    features = build_features(service)

    if not features:
        continue

    score = predict(service, features)

    send_to_es(features, score)

    trigger_alerts(features, score)

    print(f"[{service}] anomaly={score} req={features['req_count']}")
