# 🚀 AIOps-Based Microservices Anomaly Detection System Using Machine Learning

## 📌 Overview
A batch-based AIOps pipeline designed to detect anomalies in microservices by analyzing application logs and system metrics. It collects data from
Elasticsearch and Prometheus at regular intervals, performs feature engineering, and builds structured datasets. Using an unsupervised Isolation
Forest model, it identifies unusual patterns in service behavior. The system helps improve observability, supports proactive incident detection,
and demonstrates how machine learning can enhance reliability and operational efficiency in distributed environments without requiring real-time
streaming infrastructure.

It combines:
- 📄 Application logs (ELK stack)
- 📊 System metrics (Prometheus)
- 🤖 Machine Learning (Isolation Forest)

⚠️ Runs in **batch mode (every 1 minute)**, not real-time streaming.

---

## 🏗️ Architecture
![Architecture](https://raw.githubusercontent.com/balusena/mlops-aiops-dataops-gitops/main/aiops-batch-ml.png)

---

## 🧰 Tech Stack
- Python
- Pandas
- Scikit-learn (Isolation Forest)
- Elasticsearch (logs)
- Prometheus (metrics)

---

## 📊 Features

Logs:
- Request count
- 5xx error rate
- 4xx error rate
- Average latency
- P95 latency
- Upstream response time

Metrics:
- CPU usage
- Memory usage
- Request rate

---

## 🤖 ML Model
- Isolation Forest
- Unsupervised anomaly detection
- Trained per service
- Contamination: 5%

---

## ⚙️ Workflow
1. Fetch logs (last 1 minute)
2. Fetch metrics per service
3. Build features
4. Save to CSV
5. Train model
6. Predict anomalies

---

## 📈 Sample Output
timestamp,service,req_count,error_rate,avg_latency,cpu_usage,anomaly
2026-04-12 10:01,cart,120,0.08,0.45,0.62,1
2026-04-12 10:01,user,98,0.02,0.30,0.40,1
2026-04-12 10:01,payment,60,0.25,1.20,0.85,-1

Interpretation:
- 1 = Normal
- -1 = Anomaly

---

## ▶️ Run

pip install pandas scikit-learn elasticsearch requests

Start services:
- Elasticsearch
- Prometheus

Run:
python main.py

---

## 🧪 Sample Data (Optional)
- elasticsearch_log_data.csv
- prometheus_metric_data.csv

---

## 💡 Why This Project
- Observability (logs + metrics)
- ML-based anomaly detection
- DevOps automation
- AIOps workflow simulation

---

## 🚀 Future Work
- Kafka streaming
- Model persistence
- Slack alerts
- Grafana dashboard

---

## 🧾 Summary
Batch AIOps system that:
- Collects logs + metrics
- Builds features
- Trains Isolation Forest
- Detects anomalies per service

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