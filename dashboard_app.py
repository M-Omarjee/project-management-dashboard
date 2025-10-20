# dashboard_app.py
from datetime import datetime, timezone
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import numpy as np

st.set_page_config(page_title="ProjectPulse Dashboard", layout="wide")
st.title("📈 ProjectPulse Dashboard")
st.caption(f"Data refreshed: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

# --- API base ---
BASE = st.sidebar.text_input("API Base URL", "http://127.0.0.1:8000")

def fetch_json(path: str):
    try:
        r = requests.get(f"{BASE}{path}", timeout=15)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

# --- Fetch data ---
kpis, e1     = fetch_json("/kpis")
forecast, e2 = fetch_json("/forecast")
risks, e3    = fetch_json("/risks")
summary, e4  = fetch_json("/summary")
finance, e5  = fetch_json("/finance")

# Hard-stop on critical endpoints only
if any([e1, e2, e3, e4]):
    st.error("\n\n".join([e for e in [e1, e2, e3, e4] if e]))
    st.stop()
if e5:
    st.warning("Finance endpoint failed to load. Finance tab will be limited.")

# --- To DataFrames ---
forecast = pd.DataFrame(forecast)
risks    = pd.DataFrame(risks)
finance  = pd.DataFrame(finance) if isinstance(finance, list) and len(finance) > 0 else pd.DataFrame()

# Attach Phase/Status to Finance using risks table meta
project_meta = risks[["Project_ID", "Phase", "Status"]].drop_duplicates()
if not finance.empty:
    finance = finance.merge(project_meta, on="Project_ID", how="left")

# --- Sidebar filters (global) ---
st.sidebar.header("Filters")
phase_sel  = st.sidebar.multiselect("Project Phase", sorted(project_meta["Phase"].dropna().unique()))
status_sel = st.sidebar.multiselect("Status",        sorted(project_meta["Status"].dropna().unique()))

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if "Phase" in df.columns and phase_sel:
        df = df[df["Phase"].isin(phase_sel)]
    if "Status" in df.columns and status_sel:
        df = df[df["Status"].isin(status_sel)]
    return df

forecast_f = apply_filters(forecast.copy())
risks_f    = apply_filters(risks.copy())
finance_f  = apply_filters(finance.copy()) if not finance.empty else finance

# --- Tabs ---
overview, finance_tab = st.tabs(["📊 Overview", "💰 Finance"])

with overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", kpis["projects"])
    c2.metric("Avg Completion", f"{kpis['avg_completion_pct']:.1f}%")
    c3.metric("Cost Variance", f"{kpis['cost_variance_pct']:.1f}%")
    c4.metric("Time Variance", f"{kpis['time_variance_pct']:.1f}%")

    st.markdown("### Delay Probability by Project")
    if not forecast_f.empty:
        fig = px.bar(
            forecast_f, x="Project_ID", y="Delay_Probability",
            color="Status", barmode="group", text="Delay_Probability"
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(yaxis_title="% Delay Probability", xaxis_title="", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No forecast rows after filters.")

    st.markdown("### Risk Register")
    st.dataframe(risks_f, use_container_width=True)

    st.markdown("### Executive Summary")
    st.write(summary["executive_summary"] if isinstance(summary, dict) else summary)

with finance_tab:
    st.subheader("💰 Budget vs Actual")

    if not finance_f.empty:
        # Grouped bar chart
        fig = px.bar(finance_f, x="Project_ID", y=["Budget", "Actual"], barmode="group", title=None)
        fig.update_layout(yaxis_title="£", xaxis_title="")
        fig.update_yaxes(tickprefix="£", separatethousands=True)
        st.plotly_chart(fig, use_container_width=True)

        # Variance table with conditional colouring
        nice = finance_f.copy()
        nice["Variance_Pct"] = nice["Variance_Pct"].round(1)

        def color_variance(val):
            if val > 0:  # over budget
                return "background-color:#ffe5e5"
            if val < 0:  # under budget
                return "background-color:#e6ffea"
            return "background-color:#f3f3f3"

        styled = (
            nice.style
            .format({
                "Budget": "£{:,.0f}",
                "Actual": "£{:,.0f}",
                "Variance_Amount": "£{:,.0f}",
                "Variance_Pct": "{:.1f}%"
            })
            .apply(lambda col: [color_variance(v) if col.name in ["Variance_Amount", "Variance_Pct"] else "" for v in col], axis=0)
        )

        st.markdown("#### Variance Table")
        st.dataframe(styled, use_container_width=True)

        # CSV download
        csv = nice.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Finance CSV", csv, "finance.csv", "text/csv")
    else:
        st.info("Finance data not available or filtered out.")
