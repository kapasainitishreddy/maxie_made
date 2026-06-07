"""Notebooks API."""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.core.errors import NotFoundError
from app.models.notebook import Notebook

router = APIRouter()


class NotebookCreate(BaseModel):
    name: str
    description: str = ""
    cells: list = []


class CellExecute(BaseModel):
    code: str


@router.get("")
async def list_notebooks(db: Annotated[AsyncSession, Depends(get_db)]) -> list[dict]:
    res = await db.execute(select(Notebook).order_by(Notebook.updated_at.desc()))
    return [{"id": str(n.id), "name": n.name, "description": n.description, "updated_at": n.updated_at.isoformat()} for n in res.scalars()]


@router.post("")
async def create_notebook(body: NotebookCreate, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    n = Notebook(org_id=uuid.uuid4(), name=body.name, description=body.description, cells=body.cells)
    db.add(n)
    await db.flush()
    return {"id": str(n.id), "name": n.name}


@router.get("/{nb_id}")
async def get_notebook(nb_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    n = await db.get(Notebook, nb_id)
    if not n: raise NotFoundError("Notebook not found")
    return {"id": str(n.id), "name": n.name, "description": n.description, "cells": n.cells}


@router.post("/{nb_id}/execute")
async def execute_cell(nb_id: uuid.UUID, body: CellExecute, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    """Execute a code cell in a restricted Python sandbox."""
    n = await db.get(Notebook, nb_id)
    if not n: raise NotFoundError("Notebook not found")
    from app.services.backtester import Backtester
    from app.services.data import DataFetcher
    import pandas as pd
    prices = await DataFetcher.fetch("SPY", "2023-01-01", "2024-01-01")
    bt = Backtester(body.code, prices)
    return bt.run()
