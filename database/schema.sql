-- Creating table to load the raw data into PostgreSQL
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

-- Now I am going to index the frequency queried columns for performance
CREATE INDEX idx_campaign_format ON raw_ad_telemetry(campaign_id, format);
CREATE INDEX idx_event_type ON raw_ad_telemetry(event_type);
