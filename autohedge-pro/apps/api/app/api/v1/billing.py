from fastapi import APIRouter
router = APIRouter()

@router.get("/plans")
async def plans() -> list[dict]:
    return [
        {"id": "free", "name": "Free", "price": 0, "interval": "month",
         "description": "Paper trading only", "features": ["1 portfolio", "$50k paper", "All 12 strategies"]},
        {"id": "pro", "name": "Pro", "price": 99, "interval": "month",
         "description": "For active retail traders",
         "features": ["Unlimited paper", "Unlimited backtests", "Walk-forward optimization", "Monte Carlo", "Email support"]},
        {"id": "aum", "name": "AUM", "price": None, "interval": "year",
         "description": "0.5% of AUM (annual) for live trading",
         "features": ["Live trading via Alpaca/IBKR", "Custom strategies", "Dedicated CSM", "SOC2 + audit logs"]},
    ]
