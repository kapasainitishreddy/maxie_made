"""API v1."""
from fastapi import APIRouter
from app.api.v1.accounts import router as accounts_router
from app.api.v1.recommendations import router as recs_router
from app.api.v1.savings import router as savings_router
from app.api.v1.billing import router as billing_router

api_router = APIRouter()
api_router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(recs_router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(savings_router, prefix="/savings", tags=["savings"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
