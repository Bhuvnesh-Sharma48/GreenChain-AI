import json
import google.generativeai as genai

def _strict_json(text: str) -> dict:
    """
    Gemini sometimes returns extra text. This attempts to extract JSON safely.
    """
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in Gemini output.")
    return json.loads(text[start:end+1])

def risk_agent(gemini_model, payload: dict, disruption_signals: dict) -> dict:
    prompt = f"""
You are a senior supply chain risk analyst.

Supply chain:
Product: {payload['product']}
Origin: {payload['origin']}
Destination: {payload['destination']}
Monthly demand: {payload['monthly_demand']}
Lead time: {payload['lead_time_days']} days
Priority: {payload['priority']}

Disruption signals from web search:
Summary: {disruption_signals.get('answer_summary', '')}

Sources:
{disruption_signals.get('sources', [])}

Return STRICT JSON only with schema:
{{
  "top_risks": [
    {{"risk":"...", "severity_1_to_5": 1, "probability_1_to_5": 1, "impact":"..."}}
  ],
  "mitigation_plan": ["...", "..."],
  "quick_wins_2_weeks": ["...", "..."],
  "notes": "Short note referencing disruption signals if relevant"
}}

Rules:
- 4-6 risks max
- no markdown, no explanation text
"""
    res = gemini_model.generate_content(prompt)
    return _strict_json(res.text)
