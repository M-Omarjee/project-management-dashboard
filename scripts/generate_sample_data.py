import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)
Path("data").mkdir(parents=True, exist_ok=True)

projects = ["NHS-001","NHS-002","NHS-003","NHS-004","NHS-005"]
phases   = ["Design","Build","Fit-Out","Go-Live"]

rows = []
for pid in projects:
    planned_duration = np.random.randint(60, 220)
    actual_duration  = int(planned_duration * np.random.normal(1.05, 0.12))
    planned_cost     = np.random.randint(500_000, 5_000_000)
    actual_cost      = int(planned_cost * np.random.normal(1.07, 0.15))
    completion       = np.clip(np.random.normal(0.72, 0.15), 0.2, 0.98)
    risk_level       = np.random.choice(["Low","Medium","High"], p=[0.35,0.45,0.20])
    phase            = np.random.choice(phases, p=[0.25,0.45,0.25,0.05])
    status           = np.random.choice(["On Track","At Risk","Delayed"], p=[0.55,0.25,0.20])

    rows.append({
        "Project_ID": pid,
        "Phase": phase,
        "Planned_Duration": planned_duration,
        "Actual_Duration": actual_duration,
        "Planned_Cost": planned_cost,
        "Actual_Cost": actual_cost,
        "Completion_Pct": round(completion*100,1),
        "Risk_Level": risk_level,
        "Status": status
    })

df = pd.DataFrame(rows)
df.to_csv("data/project_data.csv", index=False)

# A simple task log for Gantt-style visuals / forecasting
tasks = []
for pid in projects:
    for i in range(1, 6):
        planned = np.random.randint(10, 40)
        actual  = int(planned * np.random.normal(1.06, 0.2))
        tasks.append({
            "Project_ID": pid,
            "Task_Name": f"Task {i}",
            "Planned_Days": planned,
            "Actual_Days": actual,
            "Owner": np.random.choice(["PM","Contractor","Trust IT","Clinical Leads"]),
            "Percent_Complete": np.clip(int(np.random.normal(70, 20)), 10, 100)
        })
pd.DataFrame(tasks).to_csv("data/task_log.csv", index=False)

print("✅ Wrote data/project_data.csv and data/task_log.csv")
