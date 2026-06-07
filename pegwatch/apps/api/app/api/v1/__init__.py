"""API v1 routes."""
from fastapi import APIRouter

from app.api.v1 import alerts, billing, peg, stablecoins, webhooks

api_router = APIRouter()
api_router.include_router(stablecoins.router, prefix="/stablecoins", tags=["stablecoins"])
api_router.include_router(peg.router, prefix="/peg", tags=["peg"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
