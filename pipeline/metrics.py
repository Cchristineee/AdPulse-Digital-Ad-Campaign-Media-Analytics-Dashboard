import pandas as pd
import numpy as np

def load_telemetry(file_path: str) -> pd.DataFrame:
    """Loads raw telemetry CSV and parses timestamps."""
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def calculate_campaign_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates raw event-level telemetry into campaign-level media KPIs."""

    # 1. Pivot event types into columns (impressions, quartiles, clicks, conversions)
    event_counts = (
        df.groupby(["campaign_id", "campaign_name", "format", "event_type"])
        .size()
        .unstack(fill_value=0)
    )

    # This just ensures that all of the expected event columns exist even if the count is 0
    expected_events = [
        "impression",
        "q1_25",
        "q2_50",
        "q3_75",
        "q4_100",
        "click",
        "conversion",
    ]
    for event in expected_events:
        if event not in event_counts.columns:
            event_counts[event] = 0

    # 2. Aggregating spend and revenue totals
    financials = (
        df.groupby(["campaign_id", "campaign_name", "format"])
        .agg(total_spend=("cost", "sum"), total_revenue=("revenue", "sum"))
    )

    # 3. Combine event counts and financials
    kpi_df = financials.join(event_counts).reset_index()

    # 4. Compute Media KPIs
    # Impressions & Quartiles
    impressions = kpi_df["impression"]
    q1_plays = kpi_df["q1_25"]
    completions = kpi_df["q4_100"]
    conversions = kpi_df["conversion"]
    spend = kpi_df["total_spend"]
    revenue = kpi_df["total_revenue"]

    # Prevent division by zero
    kpi_df["hook_rate_pct"] = np.where(
        impressions > 0, (q1_plays / impressions) * 100, 0.0
    )
    kpi_df["vtr_pct"] = np.where(
        impressions > 0, (completions / impressions) * 100, 0.0
    )
    kpi_df["cpv"] = np.where(completions > 0, spend / completions, 0.0)
    kpi_df["cpa"] = np.where(conversions > 0, spend / conversions, 0.0)
    kpi_df["roas"] = np.where(spend > 0, revenue / spend, 0.0)

    # Format rounding for clear presentation
    kpi_df = kpi_df.round(
        {
            "total_spend": 2,
            "total_revenue": 2,
            "hook_rate_pct": 2,
            "vtr_pct": 2,
            "cpv": 4,
            "cpa": 2,
            "roas": 2,
        }
    )

    # Reorder columns for dashboard/reporting readability
    column_order = [
        "campaign_id",
        "campaign_name",
        "format",
        "impression",
        "q1_25",
        "q4_100",
        "conversion",
        "total_spend",
        "total_revenue",
        "hook_rate_pct",
        "vtr_pct",
        "cpv",
        "cpa",
        "roas",
    ]

    return kpi_df[column_order]

if __name__ == "__main__":
    # Load synthetic dataset
    input_file = "data/raw_vast_telemetry.csv"
    output_file = "data/processed_campaign_kpis.csv"

    print("Loading telemetry data...")
    raw_df = load_telemetry(input_file)

    print("Calculating media metrics...")
    summary_kpis = calculate_campaign_kpis(raw_df)

    # Save processed aggregated output
    summary_kpis.to_csv(output_file, index=False)
    print(f"KPI processing complete! Saved to {output_file}\n")

    # Display sample output table
    print(summary_kpis.to_string(index=False))