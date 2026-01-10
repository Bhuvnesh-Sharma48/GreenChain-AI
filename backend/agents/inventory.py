import math

Z_TABLE = {0.90: 1.28, 0.95: 1.65, 0.97: 1.88, 0.98: 2.05, 0.99: 2.33}

def nearest_z(service_level: float) -> float:
    closest = min(Z_TABLE.keys(), key=lambda k: abs(k - service_level))
    return Z_TABLE[closest]

def compute_inventory_strategy(
    monthly_demand: int,
    lead_time_days: int,
    holding_cost_per_unit_year: float,
    ordering_cost: float,
    service_level: float
):
    annual_demand = monthly_demand * 12
    daily_demand = annual_demand / 365

    eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit_year)

    demand_during_lead = daily_demand * lead_time_days

    sigma_daily = 0.15 * daily_demand
    sigma_lead = sigma_daily * math.sqrt(lead_time_days)

    z = nearest_z(service_level)
    safety_stock = z * sigma_lead
    reorder_point = demand_during_lead + safety_stock

    orders_per_year = annual_demand / eoq
    days_between_orders = 365 / orders_per_year

    return {
        "annual_demand_units": round(annual_demand, 2),
        "daily_demand_units": round(daily_demand, 3),
        "eoq_units": round(eoq, 2),
        "orders_per_year": round(orders_per_year, 2),
        "avg_days_between_orders": round(days_between_orders, 1),
        "lead_time_days": lead_time_days,
        "safety_stock_units": round(safety_stock, 2),
        "reorder_point_units": round(reorder_point, 2),
        "interpretation": [
            f"Order about {round(eoq)} units each replenishment.",
            f"Place order when inventory falls to ~{round(reorder_point)} units.",
            f"Keep safety stock ~{round(safety_stock)} units."
        ]
    }
