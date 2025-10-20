import pandas as pd

def risk_score(df: pd.DataFrame) -> pd.DataFrame:
    score = []
    for _, r in df.iterrows():
        s = 0
        if r["Actual_Cost"] > r["Planned_Cost"]: s += 2
        if r["Actual_Duration"] > r["Planned_Duration"]: s += 2
        if r["Completion_Pct"] < 60: s += 1
        s += {"Low":0,"Medium":1,"High":2}.get(r["Risk_Level"],1)
        s += {"On Track":0,"At Risk":1,"Delayed":2}.get(r["Status"],1)
        score.append(s)
    out = df[["Project_ID","Phase","Status","Risk_Level"]].copy()
    out["Risk_Score_0to9"] = score
    return out.sort_values("Risk_Score_0to9", ascending=False).reset_index(drop=True)
