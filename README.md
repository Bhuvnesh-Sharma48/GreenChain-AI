# GreenChain AI — Supply Chain Decision Copilot (Agentic AI)

GreenChain AI is an **agentic AI supply chain copilot** that helps businesses make better supply chain decisions by combining:
- **Inventory optimization (EOQ, safety stock, reorder point)**
- **Live disruption intelligence** from the web (Tavily)
- **Multi-agent reasoning** using **Gemini**
- **Actionable business outputs** (Risk report, Efficiency plan, Action plan)

It is built as a production-style two-service application:

- **FastAPI backend** → agent pipeline + calculations + Gemini + Tavily  
- **Streamlit frontend** → dashboard UI for decision making

---

## Features

### Inventory Strategy Engine
- EOQ (Economic Order Quantity)
- Safety stock (based on service level)
- Reorder point
- Interpretation in business-friendly language

### Disruption Signals (Tavily)
- Web-based disruption evidence for route/product
- Summary + clickable sources

### Agentic AI Reports (Gemini)
- **Risk report**: top risks + mitigation plan + quick wins
- **Efficiency plan**: transport + packaging + waste reduction
- **Action plan**: 30/90-day roadmap + KPIs

### Beautiful Dashboard UI
- Dark theme UI
- Banner + logo support
- Clean structured text outputs (no raw JSON)
- Downloadable report

---

## Tech Stack

**Frontend**
- Streamlit

**Backend**
- FastAPI + Uvicorn
- Google Gemini API (`google-generativeai`)
- Tavily Search API

---

## Architecture

```txt
Streamlit Frontend (Dashboard)
        |
        | POST /analyze_supply_chain
        v
FastAPI Backend (Agent Controller)
        |
        |--> Inventory Agent (math, EOQ & safety stock)
        |--> Tavily Agent (web disruption signals)
        |--> Risk Agent (Gemini)
        |--> Efficiency Agent (Gemini)
        |--> Planner Agent (Gemini)
        |
        v
Response -> Frontend Renders Report
