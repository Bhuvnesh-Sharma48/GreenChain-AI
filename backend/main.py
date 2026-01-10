from fastapi import FastAPI
from dotenv import load_dotenv

from schemas import SupplyChainRequest, SupplyChainResponse
from agents.controller import run_controller

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()

app = FastAPI(title="GreenChain AI Backend", version="2.0")

@app.get("/")
def root():
    return {"status": "ok", "message": "GreenChain AI backend (Gemini + Tavily) running"}

@app.post("/analyze_supply_chain", response_model=SupplyChainResponse)
async def analyze(req: SupplyChainRequest):
    payload = req.model_dump()
    result = await run_controller(payload)
    return result
