import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURES = ["Planned_Duration","Actual_Duration","Planned_Cost","Actual_Cost","Completion_Pct"]

def predict_delays(df: pd.DataFrame) -> pd.DataFrame:
    X = df[FEATURES].copy()
    y = (df["Actual_Duration"] > df["Planned_Duration"]).astype(int)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)
    probs = model.predict_proba(X)[:, 1]

    out = df[["Project_ID","Phase","Status"]].copy()
    out["Delay_Probability"] = (probs * 100).round(1)
    return out.sort_values("Delay_Probability", ascending=False).reset_index(drop=True)
