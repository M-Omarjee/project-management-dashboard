from typing import Dict

def generate_summary(kpi: Dict) -> str:
    cost = kpi["cost_variance_pct"]
    time = kpi["time_variance_pct"]
    comp = kpi["avg_completion_pct"]
    delayed = kpi["delayed"]
    at_risk = kpi["at_risk"]

    risk_line = []
    if delayed > 0: risk_line.append(f"{delayed} project(s) delayed")
    if at_risk > 0: risk_line.append(f"{at_risk} at risk")
    risk_line = ", ".join(risk_line) if risk_line else "most projects on track"

    direction_cost = "over" if cost >= 0 else "under"
    direction_time = "slower" if time >= 0 else "faster"

    return (
        f"Portfolio status: average completion {comp:.1f}%. "
        f"Costs are {abs(cost):.1f}% {direction_cost} plan and delivery is {abs(time):.1f}% {direction_time} than planned. "
        f"Risk snapshot: {risk_line}. "
        f"Recommended actions: focus on tasks with low completion and high variance; "
        f"reallocate resources to critical paths and enforce change control on scope creep."
    )
