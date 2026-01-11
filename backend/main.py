from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import SupplyChainRequest, SupplyChainResponse
from agents.controller import run_controller

# -------------------------
# Create app FIRST
# -------------------------
app = FastAPI(
    title="GreenChain AI Backend",
    version="1.0.0",
    description="FastAPI backend for GreenChain AI — Supply Chain Decision Copilot",
)

# -------------------------
# CORS (required for Streamlit Cloud)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Health routes
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "GreenChain backend running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# -------------------------
# Main endpoint
# -------------------------
@app.post("/analyze_supply_chain", response_model=SupplyChainResponse)
async def analyze_supply_chain(payload: SupplyChainRequest):
    """
    Runs agentic controller pipeline:
    - Inventory calculations
    - Tavily disruption signals
    - Gemini risk report
    - Gemini efficiency plan
    - Gemini action plan
    """
    result = await run_controller(payload.model_dump())
    return result
