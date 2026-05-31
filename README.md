# 🏪 Store Intelligence System

## Overview

Store Intelligence System is an AI-powered retail analytics platform that transforms raw CCTV footage into actionable business insights. The system leverages Computer Vision, Object Tracking, Event Processing, and Real-Time Analytics to help retailers understand customer behavior, store performance, and operational efficiency.

Built as part of the **Purplle Tech Challenge 2026**, the platform processes CCTV footage from multiple store cameras to generate footfall analytics, zone-level customer engagement metrics, anomaly detection, and business intelligence dashboards.

---

## Key Features

### 👥 Customer Detection & Tracking

* Person detection using YOLOv8
* Multi-object tracking using ByteTrack
* Persistent customer IDs across frames
* Real-time video analytics pipeline

### 🚪 Footfall Analytics

* Entry counting
* Exit counting
* Visitor tracking
* Footfall event generation

### 🗺️ Zone Analytics

* Consultation Zone Monitoring
* Skincare Zone Monitoring
* Makeup Zone Monitoring
* Zone-wise customer visit tracking
* Most popular zone identification

### 📊 Business Intelligence

* Total Entries
* Total Exits
* Unique Visitors
* Zone Visit Distribution
* Most Popular Zone
* Store Activity Monitoring

### ⚠️ Anomaly Detection

* High Footfall Detection
* Unusual Store Activity Detection
* Zone Congestion Monitoring
* Entry/Exit Imbalance Detection

### 🔗 REST APIs

* Event APIs
* Metrics APIs
* Analytics APIs
* Anomaly APIs
* Heatmap APIs

### 📈 Dashboard

* Real-time metrics visualization
* Zone analytics dashboard
* Event monitoring
* Operational insights

---

## System Architecture

```text
CCTV Cameras
      │
      ▼
YOLOv8 Detection
      │
      ▼
ByteTrack Tracking
      │
      ▼
Event Generator
      │
      ▼
SQLite Database
      │
 ┌────┴────┐
 ▼         ▼
FastAPI   Analytics Engine
 │
 ▼
Streamlit Dashboard
```

---

## Technology Stack

| Component        | Technology |
| ---------------- | ---------- |
| Computer Vision  | YOLOv8     |
| Object Tracking  | ByteTrack  |
| Backend API      | FastAPI    |
| Database         | SQLite     |
| Dashboard        | Streamlit  |
| Language         | Python     |
| Video Processing | OpenCV     |
| ORM              | SQLAlchemy |

---

## Project Structure

```text
store-intelligence-system/
│
├── backend/
│   ├── database.py
│   ├── models.py
│   ├── event_service.py
│   ├── analytics.py
│   ├── anomaly_engine.py
│   └── main.py
│
├── detection/
│   ├── track_people.py
│   ├── cam3_counter.py
│   └── cam2_zone_analytics.py
│
├── dashboard/
│   └── app.py
│
├── database/
│
├── docs/
│   ├── DESIGN.md
│   ├── CHOICES.md
│   └── architecture.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## API Endpoints

### Home

```http
GET /
```

Returns project status.

---

### Events

```http
GET /events
```

Returns all generated store events.

---

### Metrics

```http
GET /metrics
```

Returns:

```json
{
  "entries": 25,
  "exits": 20,
  "unique_visitors": 18
}
```

---

### Analytics

```http
GET /analytics
```

Returns:

```json
{
  "most_popular_zone": "MAKEUP",
  "zone_visits": {
    "MAKEUP": 12,
    "SKINCARE": 7,
    "CONSULTATION": 4
  }
}
```

---

### Anomalies

```http
GET /anomalies
```

Returns detected store anomalies.

---

### Heatmap

```http
GET /heatmap
```

Returns zone activity distribution.

---

## How to Run

### Clone Repository

```bash
git clone <repository-url>
cd store-intelligence-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

```bash
python -m backend.init_db
```

### Run FastAPI

```bash
uvicorn backend.main:app --reload
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Business Insights Generated

The platform can provide:

* Customer Footfall Analysis
* Popular Store Zones
* Customer Engagement Patterns
* Store Activity Monitoring
* Operational Intelligence
* Zone Utilization Analysis
* Retail Performance Insights

---

## Engineering Decisions

### Why YOLOv8?

YOLOv8 provides an excellent balance between accuracy and inference speed, making it suitable for CCTV-based retail analytics.

### Why ByteTrack?

ByteTrack performs robust multi-object tracking and is lightweight enough for practical deployment.

### Why SQLite?

SQLite offers fast setup, zero configuration, and is sufficient for event storage in a hackathon environment.

### Why FastAPI?

FastAPI provides high-performance APIs, automatic documentation, and clean backend architecture.

### Why Streamlit?

Streamlit enables rapid dashboard development and easy visualization of analytics data.

---

## Future Improvements

* Real-time RTSP Camera Integration
* Multi-Camera Customer Re-Identification
* Advanced Heatmap Visualization
* Cloud Deployment
* Kafka Event Streaming
* Predictive Analytics
* Customer Journey Analytics
* Queue Monitoring
* Staff Activity Analytics
* Inventory Correlation Analytics

---

## Challenge Alignment

This solution addresses the key requirements of the Purplle Tech Challenge 2026:

✅ Computer Vision Pipeline

✅ Multi-Object Tracking

✅ Event Generation

✅ Real-Time Analytics

✅ REST APIs

✅ Dashboard Visualization

✅ Anomaly Detection

✅ Production-Oriented Architecture

---

## Author

**Tushar**

Purplle Tech Challenge 2026 Submission
