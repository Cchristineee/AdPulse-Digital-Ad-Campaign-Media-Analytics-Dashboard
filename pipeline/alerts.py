import pandas as pd

# Threshold configs
TARGET_CPA_THRESHOLDS = {
    "CMP_101": 25.0,  # Target CPA $25.00
    "CMP_102": 40.0,  # Target CPA $40.00
    "CMP_103": 50.0,  # Target CPA $50.00
}

VTR_BASELINE_PCT = 6.0  # Alert if VTR drops below 6.0% (indicates tag failure)

# Default alerting thresholds for KPIs and metrics
def load_processed_kpis(file_path: str) -> pd.DataFrame:
    """Loads the aggregated KPI dataset."""
    return pd.read_csv(file_path)

def evaluate_alerts(df: pd.DataFrame) -> list[dict]:
    """Evaluates campaign metrics against defined thresholds and tag health baselines."""
    alerts = []

    for _, row in df.iterrows():
        cmp_id = row["campaign_id"]
        cmp_name = row["campaign_name"]
        ad_format = row["format"]
        vtr = row["vtr_pct"]
        cpa = row["cpa"]
        target_cpa = TARGET_CPA_THRESHOLDS.get(cmp_id, 30.0)

    # 1. Tag Firing / Execution Error Detection (Low VTR relative to funnel)
    if vtr < VTR_BASELINE_PCT:
            alerts.append({
                "severity": "CRITICAL",
                "type": "TAG_FIRING_ERROR",
                "campaign": f"{cmp_name} ({cmp_id})",
                "format": ad_format,
                "message": f"Possible VAST tag drop-off! VTR is {vtr:.2f}% (Baseline: {VTR_BASELINE_PCT}%). Check 50%/75% quartile telemetry.",
            })

    # 2. Target CPA Breach Detection
    if cpa > target_cpa:
            overage_pct = ((cpa - target_cpa) / target_cpa) * 100
            alerts.append({
                "severity": "WARNING",
                "type": "CPA_THRESHOLD_EXCEEDED",
                "campaign": f"{cmp_name} ({cmp_id})",
                "format": ad_format,
                "message": f"CPA (${cpa:.2f}) exceeded target (${target_cpa:.2f}) by {overage_pct:.1f}%.",
            })

    return alerts

def print_alert_report(alerts: list[dict]):
    """Formats and prints alert logs to the console."""
    print("=" * 80)
    print(" 🚨 ADPULSE AUTOMATED SYSTEM ALERTS 🚨")
    print("=" * 80)

    if not alerts:
        print("All campaigns and ad tags operating within normal parameters.")
        return

    for alert in alerts:
        icon = "🔴" if alert["severity"] == "CRITICAL" else "🟡"
        print(f"{icon} [{alert['severity']}] {alert['type']}")
        print(f"   Campaign: {alert['campaign']} | Format: {alert['format']}")
        print(f"   Details:  {alert['message']}")
        print("-" * 80)


if __name__ == "__main__":
    kpi_file = "data/processed_campaign_kpis.csv"

    print("Evaluating campaign health and telemetry...")
    kpi_df = load_processed_kpis(kpi_file)
    active_alerts = evaluate_alerts(kpi_df)

    print_alert_report(active_alerts)