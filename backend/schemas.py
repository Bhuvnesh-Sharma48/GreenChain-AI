from pydantic import BaseModel, Field
from typing import Dict, Any, Literal, List

class SupplyChainRequest(BaseModel):
    product: str
    origin: str
    destination: str

    monthly_demand: int = Field(..., gt=0)
    lead_time_days: int = Field(14, gt=0)

    holding_cost_per_unit_year: float = Field(20.0, gt=0)
    ordering_cost: float = Field(200.0, gt=0)

    service_level: float = Field(0.95, ge=0.5, le=0.99)

    priority: Literal["low_cost", "fast_delivery", "sustainability"] = "sustainability"

class SupplyChainResponse(BaseModel):
    inventory_strategy: Dict[str, Any]
    disruption_signals: Dict[str, Any]
    risk_report: Dict[str, Any]
    efficiency_plan: Dict[str, Any]
    action_plan: Dict[str, Any]
