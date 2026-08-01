# AdPulse: Real-Time VAST Telemetry & Campaign Performance Pipeline

**AdPulse** is an end-to-end data engineering and analytics pipeline designed to ingest, process, and analyze raw Digital Video & Display VAST (Digital Video Ad Serving Template) telemetry data. 

The system simulates high-volume ad serving events (impressions, quartile video plays, completions, and conversions), loads structured telemetry into a PostgreSQL database, and visualizes real-time performance anomalies via an interactive Metabase dashboard.

---

## 📸 Executive Dashboard Overview

![Hook Rate vs VTR by Format](dashboard/Metabase-Hook%20Rate%20vs%20VTR%20by%20Format-7_31_2026,%2010_37_29%20PM.png)

> **Key Finding:** While initial viewer engagement (**Hook Rate**) remains stable across all ad formats (~39%–42%), **CTV (Connected TV) Video Completion Rate (VTR)** experiences a ~50% performance drop compared to Display and OLV. This directly pinpoints a simulated VAST tag firing failure on midpoint/quartile events in CTV environments.

---

## Architecture & Data Flow
[ Synthetic Generator ] ➡️ [ Raw CSV Telemetry ] ➡️ [ Python Ingestion Pipeline ]
⬇️
[ Metabase Analytics ] ⬅️ [ Optimized SQL Queries ] ⬅️ [ PostgreSQL Database ]

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

-- Executed in database/schema.sql
CREATE TABLE raw_ad_telemetry (
    event_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    campaign_id VARCHAR(20) NOT NULL,
    campaign_name VARCHAR(100),
    format VARCHAR(20),
    event_type VARCHAR(20),
    cost NUMERIC(8, 4),
    revenue NUMERIC(8, 2)
);

CREATE INDEX idx_campaign_format ON raw_ad_telemetry(campaign_id, format);
CREATE INDEX idx_event_type ON raw_ad_telemetry(event_type);

### 3. Load Telemetry Data into PostgreSQL 
python database/load_data.py

### 4. 4. Launch Metabase Dashboard
docker run -d -p 3000:3000 --name metabase metabase/metabase

1. Navigate to http://localhost:3000 in your browser.
2. Connect Metabase to PostgreSQL using host host.docker.internal (Docker) or localhost.
3. Open the SQL Query Editor and run the performance query:

SELECT 
    format,
    COUNT(CASE WHEN event_type = 'impression' THEN 1 END) AS impressions,
    COUNT(CASE WHEN event_type = 'q1_25' THEN 1 END) AS q1_25_plays,
    COUNT(CASE WHEN event_type = 'q4_100' THEN 1 END) AS completions,
    ROUND((COUNT(CASE WHEN event_type = 'q1_25' THEN 1 END)::decimal / NULLIF(COUNT(CASE WHEN event_type = 'impression' THEN 1 END), 0)) * 100, 2) AS hook_rate_pct,
    ROUND((COUNT(CASE WHEN event_type = 'q4_100' THEN 1 END)::decimal / NULLIF(COUNT(CASE WHEN event_type = 'impression' THEN 1 END), 0)) * 100, 2) AS vtr_pct
FROM raw_ad_telemetry
GROUP BY format;

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
