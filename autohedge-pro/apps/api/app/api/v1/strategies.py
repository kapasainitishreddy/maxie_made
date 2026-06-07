"""Strategy catalog."""
from fastapi import APIRouter
from app.services.strategies import list_strategies, get_strategy

router = APIRouter()


@router.get("/catalog")
async def catalog() -> list[dict]:
    return list_strategies()


@router.get("")
async def list_user_strategies() -> list[dict]:
    # In a real app, fetch from DB; here return catalog as placeholder
    return list_strategies()
