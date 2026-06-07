from fastapi import APIRouter
from app.api.v1.strategies import router as strategies_router
from app.api.v1.backtest import router as backtest_router
from app.api.v1.portfolio import router as portfolio_router
from app.api.v1.billing import router as billing_router

api_router = APIRouter()
api_router.include_router(strategies_router, prefix="/strategies", tags=["strategies"])
api_router.include_router(backtest_router, prefix="/backtest", tags=["backtest"])
api_router.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
