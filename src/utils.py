import pandas as pd

def load_project_data(path="data/project_data.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def load_task_log(path="data/task_log.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def kpis(df: pd.DataFrame) -> dict:
    # Basic KPIs for the dashboard/summary
    cost_var = (df["Actual_Cost"].sum() - df["Planned_Cost"].sum()) / max(df["Planned_Cost"].sum(), 1)
    time_var = (df["Actual_Duration"].mean() - df["Planned_Duration"].mean()) / max(df["Planned_Duration"].mean(), 1)
    on_track = int((df["Status"] == "On Track").sum())
    delayed  = int((df["Status"] == "Delayed").sum())
    at_risk  = int((df["Status"] == "At Risk").sum())
    return {
        "projects": int(df["Project_ID"].nunique()),
        "avg_completion_pct": float(df["Completion_Pct"].mean()),
        "cost_variance_pct": float(cost_var * 100),
        "time_variance_pct": float(time_var * 100),
        "on_track": on_track,
        "at_risk": at_risk,
        "delayed": delayed
    }
def finance_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns Budget vs Actual by project with absolute/percentage variance.
    Expects columns: Project_ID, Planned_Cost, Actual_Cost
    """
    out = df[["Project_ID", "Planned_Cost", "Actual_Cost"]].copy()
    out = out.rename(columns={"Planned_Cost": "Budget", "Actual_Cost": "Actual"})
    out["Variance_Amount"] = (out["Actual"] - out["Budget"]).round(2)
    # avoid divide-by-zero
    out["Variance_Pct"] = (out["Variance_Amount"] / out["Budget"].replace(0, 1)).round(4) * 100
    return out.sort_values("Variance_Amount", ascending=False).reset_index(drop=True)
