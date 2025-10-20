from fastapi import FastAPI
from src.utils import load_project_data, load_task_log, kpis, finance_table
from src.forecast_model import predict_delays
from src.risk_analysis import risk_score
from src.summary_generator import generate_summary

app = FastAPI(title="ProjectPulse API")

@app.get("/kpis")
def get_kpis():
    df = load_project_data()
    metrics = kpis(df)
    return metrics


@app.get("/forecast")
def get_forecast():
    df = load_project_data()
    result = predict_delays(df)
    return result.to_dict(orient="records")


@app.get("/risks")
def get_risks():
    df = load_project_data()
    result = risk_score(df)
    return result.to_dict(orient="records")


@app.get("/summary")
def get_summary():
    df = load_project_data()
    metrics = kpis(df)
    text = generate_summary(metrics)
    return {"executive_summary": text}


@app.get("/finance")
def get_finance():
    df = load_project_data()
    result = finance_table(df)
    return result.to_dict(orient="records")


@app.get("/")
def root():
    return {
        "message": "✅ ProjectPulse API is running!",
        "endpoints": [
            "/kpis",
            "/forecast",
            "/risks",
            "/summary"
        ]
    }
