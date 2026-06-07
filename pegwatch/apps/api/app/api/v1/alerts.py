"""Alerts + alert channels (notification subscriptions)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError, PlanLimitError
from app.core.security import CurrentUser, get_current_user
from app.db import get_db
from app.models.alert import Alert, AlertChannel
from app.schemas.alert import AlertChannelCreate, AlertChannelRead, AlertRead

router = APIRouter()


@router.get("/channels", response_model=list[AlertChannelRead])
async def list_channels(
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> list[AlertChannel]:
    result = await db.execute(
        select(AlertChannel).where(AlertChannel.user_id == user.user_id).order_by(AlertChannel.created_at)
    )
    return list(result.scalars().all())


@router.post("/channels", response_model=AlertChannelRead, status_code=status.HTTP_201_CREATED)
async def create_channel(
    payload: AlertChannelCreate,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> AlertChannel:
    if user.plan == "free":
        raise PlanLimitError("Alert channels require a Pro subscription. Upgrade at /pricing.")
    channel = AlertChannel(user_id=user.user_id, **payload.model_dump())
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel


@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: str,
    db: AsyncSession = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
) -> None:
    result = await db.execute(
        select(AlertChannel).where(AlertChannel.id == channel_id, AlertChannel.user_id == user.user_id)
    )
    channel = result.scalar_one_or_none()
    if not channel:
        raise NotFoundError("Channel not found")
    await db.delete(channel)
    await db.commit()


@router.get("", response_model=list[AlertRead])
async def list_alerts(
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
    limit: int = 50,
) -> list[Alert]:
    """List recent alerts across all stablecoins (global incident feed)."""
    result = await db.execute(select(Alert).order_by(Alert.triggered_at.desc()).limit(limit))
    return list(result.scalars().all())


@router.get("/{alert_id}", response_model=AlertRead)
async def get_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
    _: CurrentUser = Depends(get_current_user),
) -> Alert:
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise NotFoundError("Alert not found")
    return alert
