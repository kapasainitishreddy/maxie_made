from fastapi import APIRouter
router = APIRouter()

@router.get("/plans")
async def plans() -> list[dict]:
    return [
        {"id": "researcher", "name": "Researcher", "price": 199, "interval": "month",
         "features": ["10 notebooks", "100 backtests/mo", "NL→code translator", "Community marketplace"]},
        {"id": "quant", "name": "Quant", "price": 499, "interval": "month",
         "features": ["Unlimited notebooks", "Unlimited backtests", "Walk-forward + Monte Carlo", "Premium marketplace access", "Alpaca paper trading"]},
        {"id": "pro", "name": "Pro", "price": 999, "interval": "month",
         "features": ["Everything in Quant", "E2B full sandbox", "Live data feeds (Polygon, FRED)", "Custom data sources", "API access", "Priority support"]},
    ]
