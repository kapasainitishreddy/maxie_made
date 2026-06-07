"""API v1 router aggregator."""

from fastapi import APIRouter

from app.api.v1.patents import router as patents_router
from app.api.v1.landscapes import router as landscapes_router
from app.api.v1.watchlist import router as watchlist_router
from app.api.v1.reports import router as reports_router
from app.api.v1.billing import router as billing_router
from app.api.v1.mcp import mcp_router

api_router = APIRouter()
api_router.include_router(patents_router, prefix="/patents", tags=["patents"])
api_router.include_router(landscapes_router, prefix="/landscapes", tags=["landscapes"])
api_router.include_router(watchlist_router, prefix="/watchlist", tags=["watchlist"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
api_router.include_router(mcp_router, prefix="/mcp", tags=["mcp"])
