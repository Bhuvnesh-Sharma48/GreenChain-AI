from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import SupplyChainInput
from agents.controller import run_controller

# -------------------------
# Create FastAPI app FIRST
# -------------------------
app = FastAPI(
    title="GreenChain AI Backend",
    version="1.0.0",
    description="FastAPI backend for GreenChain AI — Supply Chain Decision Copilot",
)

# -------------------------
# CORS middleware (important for Streamlit Cloud)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production, restrict to your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Basic routes
# -------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "GreenChain backend running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# -------------------------
# Main API route
# -------------------------
@app.post("/analyze_supply_chain")
async def analyze_supply_chain(payload: SupplyChainInput):
    """
    Runs the agentic controller pipeline:
    - Inventory calculations
    - Tavily disruption signals
    - Gemini risk report
    - Gemini efficiency plan
    - Gemini action plan
    """
    result = await run_controller(payload)
    return result
