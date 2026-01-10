import json

def _strict_json(text: str) -> dict:
    text = text.strip()
    s = text.find("{"); e = text.rfind("}")
    if s == -1 or e == -1:
        raise ValueError("No JSON detected.")
    return json.loads(text[s:e+1])

def planner_agent(gemini_model, payload: dict, inventory: dict, risks: dict, efficiency: dict) -> dict:
    prompt = f"""
You are an operations project manager.

Supply chain: {payload}
Inventory strategy: {inventory}
Risk report: {risks}
Efficiency plan: {efficiency}

Return STRICT JSON:
{{
  "executive_summary": ["...", "...", "..."],
  "plan_30_days": [
    {{"task":"...", "owner":"Ops|Procurement|Logistics|Finance|QA", "expected_result":"..."}}
  ],
  "plan_90_days": [
    {{"task":"...", "owner":"Ops|Procurement|Logistics|Finance|QA", "expected_result":"..."}}
  ],
  "kpis": [
    {{"kpi":"...", "target":"..."}}
  ]
}}

Rules:
- 4-6 bullets in executive_summary
- 6-8 tasks in each plan
- 6-10 KPIs
- no markdown
"""
    res = gemini_model.generate_content(prompt)
    return _strict_json(res.text)
