import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load variables from the .env file
load_dotenv()

# Build connection string from environment variables
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Handle password formatting if a password is required
if PASSWORD:
    DB_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
else:
    DB_URI = f"postgresql://{USER}@{HOST}:{PORT}/{DB_NAME}"


def load_csv_to_postgres():
    print("Reading data/raw_vast_telemetry.csv...")
    df = pd.read_csv("data/raw_vast_telemetry.csv")

    # Deduplicate event IDs
    df = df.drop_duplicates(subset=["event_id"])

    print("Connecting to PostgreSQL...")
    engine = create_engine(DB_URI)

    print("Clearing old records from 'raw_ad_telemetry'...")
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE raw_ad_telemetry;"))
        conn.commit()

    print(f"Loading {len(df)} rows into 'raw_ad_telemetry' table...")
    df.to_sql("raw_ad_telemetry", con=engine, if_exists="append", index=False)

    print("✅ Data successfully loaded into PostgreSQL!")


if __name__ == "__main__":
    load_csv_to_postgres()