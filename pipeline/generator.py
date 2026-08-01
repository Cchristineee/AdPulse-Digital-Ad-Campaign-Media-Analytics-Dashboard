import random
from datetime import datetime, timedelta
import pandas as pd

# ✧˖° Setting seed for reproducibility ✧˖°
campaigns = [
    {
        "id": "CMP_101",
        "name": "Summer Apparel",
        "format": "OLV",
        "budget": 5000,
        "target_cpa": 25.0,
    },
    {
        "id": "CMP_102",
        "name": "Tech Gadgets Launch",
        "format": "CTV",
        "budget": 12000,
        "target_cpa": 40.0,
    },
    {
        "id": "CMP_103",
        "name": "B2B SaaS Trial",
        "format": "Display",
        "budget": 3000,
        "target_cpa": 50.0,
    },
]

formats = ["Display", "OLV", "CTV"]
events = [
    "impression",
    "q1_25",
    "q2_50",
    "q3_75",
    "q4_100",
    "click",
    "conversion",
]

records = []
start_time = datetime.now() - timedelta(days=3)

for _ in range(10000):
    cmp = random.choice(campaigns)
    event_time = start_time + timedelta(seconds=random.randint(0, 259200))

    # ✧˖° Simulating VAST quartile funnel decay ✧˖°
    rand_val = random.random()
    if rand_val < 0.50:
        event = "impression"
    elif rand_val < 0.70:
        event = "q1_25"
    elif rand_val < 0.85:
        event = "q2_50"
    elif rand_val < 0.93:
        event = "q3_75"
    elif rand_val < 0.97:
        event = "q4_100"
    elif rand_val < 0.99:
        event = "click"
    else:
        event = "conversion"

    # ✧˖° Inject an intentional bug: CTV fails at 50% quartile (simulating tag execution failure) ✧˖°
    if (
        cmp["format"] == "CTV"
        and event in ["q2_50", "q3_75", "q4_100"]
        and random.random() < 0.4
    ):
        continue  # Event dropped / tag failed to fire

    records.append({
        "event_id": f"EVT_{random.randint(100000, 999999)}",
        "timestamp": event_time.strftime("%Y-%m-%d %H:%M:%S"),
        "campaign_id": cmp["id"],
        "campaign_name": cmp["name"],
        "format": cmp["format"],
        "event_type": event,
        "cost": (
            round(random.uniform(0.002, 0.015), 4)
            if event == "impression"
            else 0.0
        ),
        "revenue": (
            round(random.uniform(30.0, 120.0), 2)
            if event == "conversion"
            else 0.0
        ),
    })

df = pd.DataFrame(records)
df.to_csv("data/raw_vast_telemetry.csv", index=False)
print(
    f"Generated {len(df)} synthetic ad telemetry records in data/raw_vast_telemetry.csv"
)