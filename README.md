# AdPulse: Real-Time VAST Telemetry & Campaign Performance Pipeline

**AdPulse** is an end-to-end data engineering and analytics pipeline designed to ingest, process, and analyze raw Digital Video & Display VAST (Digital Video Ad Serving Template) telemetry data. 

The system simulates high-volume ad serving events (impressions, quartile video plays, completions, and conversions), loads structured telemetry into a PostgreSQL database, and visualizes real-time performance anomalies via an interactive Metabase dashboard.

---

## 📸 Executive Dashboard Overview

![Hook Rate vs VTR by Format](dashboard/Metabase-Hook%20Rate%20vs%20VTR%20by%20Format-7_31_2026,%2010_37_29%20PM.png)

> **Key Finding:** While initial viewer engagement (**Hook Rate**) remains stable across all ad formats (~39%–42%), **CTV (Connected TV) Video Completion Rate (VTR)** experiences a ~50% performance drop compared to Display and OLV. This directly pinpoints a simulated VAST tag firing failure on midpoint/quartile events in CTV environments.

---

## Architecture & Data Flow
1. **Synthetic Telemetry Generation:** Custom Python scripts simulate thousands of impression and video tracking events (`impression`, `q1_25`, `q2_50`, `q3_75`, `q4_100`, `conversion`) across Display, OLV, and CTV channels.
2. **Database Ingestion & ETL:** Python (`Pandas` + `SQLAlchemy`) deduplicates event IDs, truncates active tables for clean re-runs, and batches inserts into PostgreSQL.
3. **Relational Database Storage:** Standardized database schema enforcing primary key constraints and indexing on `campaign_id`, `format`, and `event_type`.
4. **Business Intelligence & Analytics:** Native SQL aggregation in Metabase calculating core advertising KPIs (**Hook Rate**, **VTR**, **CPM Cost**, and **Conversion Funnels**).

---

## Tech Stack & Tools

* **Language:** Python 3.9+
* **Database:** PostgreSQL
* **ORMs / Libraries:** Pandas, SQLAlchemy, Psycopg2
* **Data Visualization & BI:** Metabase
* **Containerization:** Docker Desktop
* **Version Control:** Git & GitHub

## Core Business Metrics Calculated 📊 

* **Hook Rate (%):** Measures immediate creative capture (25% quartile video plays divided by impressions).
  $$\text{Hook Rate} = \left( \frac{\text{q1\_25 Plays}}{\text{Impressions}} \right) \times 100$$
* **Video Completion Rate (VTR %):** Measures total ad retention (100% video completions divided by impressions).
  $$\text{VTR} = \left( \frac{\text{q4\_100 Completions}}{\text{Impressions}} \right) \times 100$$

---

## To Getting Started Locally

### Prerequisites

* Python 3.9+
* PostgreSQL running locally on port `5432`
* Docker Desktop (or Java runtime for Metabase)

### 1. Clone the Repository & Setup Virtual Environment

```bash
git clone [https://github.com/your-username/AdPulse.git](https://github.com/your-username/AdPulse.git)
cd AdPulse 

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pandas sqlalchemy psycopg2-binary

### 2. Database Setup (Make sure that PostgreSQL is running on your system, then create the database schema)

### 3. Load Telemetry Data into PostgreSQL 
### by using python database/load_data.py

### 4. 4. Launch Metabase Dashboard
### Run Metabase via Docker:
### docker run -d -p 3000:3000 --name metabase metabase/metabase


### Repository Structure 

├── data/
│   └── raw_vast_telemetry.csv   # Synthetic VAST event dataset
├── database/
│   ├── schema.sql              # PostgreSQL table definitions & indexing
│   └── load_data.py            # Ingestion, deduplication & ETL script
├── docs/
│   └── hook_rate_vs_vtr.png    # Dashboard visualization preview
├── pipeline/
│   └── generator.py            # Synthetic telemetry event generation script
├── .gitignore
└── README.md
