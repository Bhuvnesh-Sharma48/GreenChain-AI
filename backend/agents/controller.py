import os
import google.generativeai as genai

from agents.inventory import compute_inventory_strategy
from agents.tavily_research import fetch_disruption_signals
from agents.risk import risk_agent
from agents.efficiency import efficiency_agent
from agents.planner import planner_agent


def pick_working_model(preferred: str | None = None) -> str:
    """
    Picks a model that supports generateContent for THIS API key.
    This avoids 404 NotFound errors due to model access/region issues.
    """
    models = list(genai.list_models())

    # 1) If preferred model provided, try that first (exact match)
    if preferred:
        for m in models:
            if m.name.endswith(preferred) or m.name == preferred:
                if "generateContent" in getattr(m, "supported_generation_methods", []):
                    return m.name

    # 2) Otherwise select first model supporting generateContent
    for m in models:
        if "generateContent" in getattr(m, "supported_generation_methods", []):
            return m.name

    raise RuntimeError("No Gemini model found that supports generateContent for this API key.")


async def run_controller(payload: dict):
    # Configure Gemini
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    preferred = os.getenv("GEMINI_MODEL", "").strip() or None
    model_name = pick_working_model(preferred)

    # Print chosen model (debug)
    print("USING GEMINI MODEL:", model_name)

    gemini_model = genai.GenerativeModel(model_name)

    # Inventory (math)
    inventory = compute_inventory_strategy(
        monthly_demand=payload["monthly_demand"],
        lead_time_days=payload["lead_time_days"],
        holding_cost_per_unit_year=payload["holding_cost_per_unit_year"],
        ordering_cost=payload["ordering_cost"],
        service_level=payload["service_level"],
    )

    # Tavily disruption signals
    tavily_key = os.getenv("TAVILY_API_KEY", "")
    disruption_signals = await fetch_disruption_signals(
        tavily_api_key=tavily_key,
        product=payload["product"],
        origin=payload["origin"],
        destination=payload["destination"],
    )

    # Gemini Agents
    risks = risk_agent(gemini_model, payload, disruption_signals)
    efficiency = efficiency_agent(gemini_model, payload)
    plan = planner_agent(gemini_model, payload, inventory, risks, efficiency)

    return {
        "inventory_strategy": inventory,
        "disruption_signals": disruption_signals,
        "risk_report": risks,
        "efficiency_plan": efficiency,
        "action_plan": plan,
    }
