# 🚀 AIOps-Based Microservices Anomaly Detection System Using Kafka & Machine Learning

## 📌 Overview
A real-time AIOps pipeline designed to detect anomalies in microservices by analyzing live application telemetry streaming through Kafka. The system consumes metrics and events in real time, applies sliding window-based aggregation, performs feature engineering, and builds structured datasets per service. Using an unsupervised Isolation Forest model, it detects unusual behavior patterns across distributed microservices. This system demonstrates how machine learning can be integrated with streaming observability pipelines to improve system reliability, incident detection, and operational efficiency in modern cloud-native environments.

It is designed as a real-time alternative to batch-based AIOps systems, enabling immediate detection and response to production incidents such as latency spikes, error surges, and infrastructure degradation.

It combines:
- 📡 Kafka-based real-time streaming ingestion
- 📊 Observability signals (metrics/events/log-style telemetry)
- 🤖 Machine Learning (Isolation Forest anomaly detection)
- 📦 Elasticsearch for indexing and observability search
- 🚨 Alerting via Slack and PagerDuty

---

## 🧰 Tech Stack
- Python
- Apache Kafka
- Pandas
- NumPy
- Scikit-learn (Isolation Forest)
- Elasticsearch
- Requests (Slack + PagerDuty APIs)

---

## 🏗️ Architecture
The system follows a real-time streaming AIOps architecture:

[//]: # (![Architecture]&#40;https://raw.githubusercontent.com/balusena/mlops-aiops-dataops-gitops/main/aiops-streaming-ml-project/aiops-streaming-ml.png&#41;)

<h2 align="center">
</h2>
<p align="center">
  <img src="https://raw.githubusercontent.com/balusena/mlops-aiops-dataops-gitops/main/aiops-streaming-ml-project/aiops-streaming-ml.png" width="3000"/>
</p>

- Microservices emit telemetry data (status, latency, CPU, memory)
- OpenTelemetry-style collector pushes events into Kafka topic (`aiops-stream`)
- Kafka consumer continuously reads streaming events
- A 60-second sliding window is maintained per service
- Feature engineering aggregates raw telemetry into ML-ready metrics
- Isolation Forest model detects anomalies per service
- Results are indexed into Elasticsearch (`aiops-anomalies`)
- Alerts are triggered via Slack and PagerDuty when thresholds are breached

---

## 📊 Services Monitored
The system monitors multiple microservices independently:

- catalogue service
- user service
- cart service
- shipping service
- payment service

Each service has its own isolated behavioral pattern and anomaly detection logic.

---

## 📈 Feature Engineering (Sliding Window - 60 Seconds)

The system continuously computes features using a rolling time window:

### Request Metrics
- Request count in last 60 seconds
- Error rate (HTTP 5xx percentage)

### Latency Metrics
- Average response time
- 95th percentile latency (P95)

### Infrastructure Metrics
- CPU utilization
- Memory utilization

These features represent real-time service health and performance behavior.

---

## 🤖 Machine Learning Model

The system uses **Isolation Forest**, an unsupervised anomaly detection algorithm.

- One model is maintained per microservice
- No labeled dataset is required
- Model learns “normal behavior” dynamically
- Contamination factor: 5%

### Output Interpretation:
- `1` → Normal behavior
- `-1` → Anomalous behavior

This makes it suitable for production environments where labeled failures are not available.

---

## ⚙️ Workflow

1. Kafka consumer reads event from `aiops-stream`
2. Service name is extracted from payload
3. Event is stored in 60-second sliding window
4. Feature engineering builds aggregated metrics
5. Isolation Forest predicts anomaly score
6. Result is stored in Elasticsearch
7. Alert conditions are evaluated
8. Slack and PagerDuty alerts are triggered if required
9. Real-time logs are printed for monitoring

---

## 🚨 Alerting Layer

Alerts are triggered when BOTH conditions are met:

- Isolation Forest prediction = `-1` (anomaly detected)
- Error rate > 20%

### Alert Channels:
- Slack webhook for instant notifications
- PagerDuty for incident management and on-call escalation

This ensures that only meaningful production anomalies trigger alerts.

---

## 📦 Elasticsearch Storage

All processed telemetry and anomaly detection results are stored in Elasticsearch for search, observability, and historical analysis.

### Index Name:
- aiops-anomalies

### Stored Data Includes:
- Service name (catalogue, user, cart, shipping, payment)
- Timestamp of detection
- Aggregated feature metrics:
    - Request count
    - Error rate
    - Average latency
    - P95 latency
    - CPU usage
    - Memory usage
- ML prediction result:
    - 1 → Normal
    - -1 → Anomaly

### Purpose:
- Enable observability dashboards (Kibana)
- Track historical anomalies per service
- Debug production incidents
- Analyze service performance trends over time
- Support incident investigations and RCA (Root Cause Analysis)

---

## ▶️ Run Instructions

### Install Dependencies
pip install kafka-python pandas numpy scikit-learn elasticsearch requests

### Start Required Services
- Kafka cluster
- Elasticsearch instance
- Microservices or event producer (for telemetry simulation)

### Run Application
python main.py

---

## 🧪 Sample Event Payload

{
"service": "payment",
"status": 500,
"request_time": 850,
"cpu": 0.9,
"memory": 0.75
}

---

## 📡 Output Example

[payment] anomaly=-1 req=45

- Result stored in Elasticsearch index (`aiops-anomalies`)
- Slack alert triggered if threshold conditions are met
- PagerDuty incident triggered for critical anomalies

---

## 💡 Why This Project

- Real-time AIOps streaming architecture using Kafka
- Production-like observability pipeline simulation
- ML-based anomaly detection without labeled data
- Sliding window feature engineering for time-series behavior
- Combines DevOps + Data Engineering + MLOps concepts
- Automated incident detection and alerting system

---

## 🚀 Future Improvements

- Model persistence (save/load Isolation Forest models)
- Kafka consumer scaling using consumer groups
- Grafana dashboards for visualization
- Prometheus integration for deeper metrics monitoring
- Advanced deep learning models (LSTM / Autoencoders)
- Dynamic threshold-based alert tuning
- Dead-letter queue (DLQ) for failed events

---

## 🧾 Summary

Kafka streams telemetry → sliding window metrics → Isolation Forest detects anomalies → Elasticsearch stores results → alerts triggered in real time

---

## 👥 Who Is This For?

> [!IMPORTANT]
> This collection is perfect for:
>
> - **DevOps & DevSecOps & MLOps Engineers**: Get quick access to the tools you use every day.
> - **Sysadmins**: Simplify operations with easy-to-follow guides.
> - **Developers**: Understand the infrastructure behind your applications.
> - **DevOps Newcomers**: Transform from beginner to expert with in-depth concepts and hands-on projects.

## 🛠️ How to Use This Repository

> [!NOTE]
> 1. **Explore the Categories**: Navigate through the folders to find the tool or technology you’re interested in.
> 2. **Use the Repositories**: Each repository is designed to provide quick access to the most important concepts and projects.

## 🤝 Contributions Welcome!

We believe in the power of community! If you have a tip, command, or configuration that you'd like to share, please contribute to this repository. Whether it’s a new tool or an addition to an existing content, your input is valuable.

## 📢 Stay Updated

This repository is constantly evolving with new tools and updates. Make sure to ⭐ star this repo to keep it on your radar!

## Liking the Project?

# ⭐❤️

If you find this project helpful, please consider giving it a ⭐! It helps others discover the project and keeps me motivated to improve it.

Thank you for your support!
---
## ✍🏼 Author

### Bala Senapathi
DevSecOps Engineer | Cloud & Automation | MLOps | AIOps | GitOps Specialist

![Author Image](https://github.com/balusena/aws-devsecops-end-to-end-platform/blob/main/banner.png)

---
Made with ❤️ and passion to contribute to the DevOps community by [Bala Senapathi](https://github.com/balusena)
