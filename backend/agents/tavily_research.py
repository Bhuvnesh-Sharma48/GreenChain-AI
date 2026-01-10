import httpx

TAVILY_ENDPOINT = "https://api.tavily.com/search"

async def fetch_disruption_signals(tavily_api_key: str, product: str, origin: str, destination: str):
    """
    Uses Tavily to fetch disruption related signals:
    - strikes, port congestion, floods, geopolitical issues, logistics delays
    """
    query = f"supply chain disruption {product} {origin} {destination} port delay strike flood logistics"
    payload = {
        "api_key": tavily_api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
        "include_answer": True
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(TAVILY_ENDPOINT, json=payload)
        resp.raise_for_status()
        data = resp.json()

    results = []
    for r in data.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content_snippet": (r.get("content") or "")[:240]
        })

    return {
        "query": query,
        "answer_summary": data.get("answer", ""),
        "sources": results
    }
