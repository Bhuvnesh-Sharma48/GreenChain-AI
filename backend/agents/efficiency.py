import json

def _strict_json(text: str) -> dict:
    text = text.strip()
    s = text.find("{"); e = text.rfind("}")
    if s == -1 or e == -1:
        raise ValueError("No JSON detected.")
    return json.loads(text[s:e+1])

def efficiency_agent(gemini_model, payload: dict) -> dict:
    prompt = f"""
You are a supply chain efficiency consultant focused on business cost reduction.

Context:
Product: {payload['product']}
Origin: {payload['origin']}
Destination: {payload['destination']}
Priority: {payload['priority']}

Return STRICT JSON:
{{
  "transport_efficiency": [
    {{"action":"...", "business_benefit":"...", "effort":"low|medium|high"}}
  ],
  "packaging_damage_reduction": [
    {{"action":"...", "business_benefit":"...", "effort":"low|medium|high"}}
  ],
  "inventory_waste_reduction": [
    {{"action":"...", "business_benefit":"...", "effort":"low|medium|high"}}
  ]
}}

Rules:
- 3 to 5 actions each section
- practical, realistic
- no markdown
"""
    res = gemini_model.generate_content(prompt)
    return _strict_json(res.text)
