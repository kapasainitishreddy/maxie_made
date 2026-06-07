from fastapi import APIRouter
from app.api.v1.notebooks import router as notebooks_router
from app.api.v1.backtest import router as backtest_router
from app.api.v1.marketplace import router as marketplace_router
from app.api.v1.billing import router as billing_router
api_router = APIRouter()
api_router.include_router(notebooks_router, prefix="/notebooks", tags=["notebooks"])
api_router.include_router(backtest_router, prefix="/backtest", tags=["backtest"])
api_router.include_router(marketplace_router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
