import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Campaign, CampaignAsset, User
from app.schemas.campaign import AssetResponse, AssetUpdate
from app.security import get_current_user

router = APIRouter(prefix="/assets", tags=["assets"])


@router.patch("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: uuid.UUID,
    payload: AssetUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    asset = db.scalar(
        select(CampaignAsset)
        .join(Campaign)
        .where(CampaignAsset.id == asset_id, Campaign.user_id == user.id)
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset não encontrado")
    asset.content = payload.content
    asset.status = payload.status
    if asset.campaign.status == "generated":
        asset.campaign.status = "review"
    db.commit()
    db.refresh(asset)
    return asset

