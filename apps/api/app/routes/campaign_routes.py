import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.connection import get_db
from app.models import Campaign, User
from app.schemas.campaign import CampaignCreate, CampaignResponse, RegenerateRequest
from app.security import get_current_user
from app.services.campaign_service import create_campaign, generate_campaign, owned_campaign

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create(
    payload: CampaignCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return create_campaign(db, user, payload)


@router.get("", response_model=list[CampaignResponse])
def list_campaigns(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    status_filter: str | None = Query(None, alias="status"),
    objective: str | None = None,
):
    query = (
        select(Campaign)
        .options(selectinload(Campaign.assets))
        .where(Campaign.user_id == user.id)
        .order_by(Campaign.created_at.desc())
    )
    if status_filter:
        query = query.where(Campaign.status == status_filter)
    if objective:
        query = query.where(Campaign.objective == objective)
    return list(db.scalars(query).unique())


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return owned_campaign(db, campaign_id, user.id)


@router.post("/{campaign_id}/generate", response_model=CampaignResponse)
def generate(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return generate_campaign(db, owned_campaign(db, campaign_id, user.id))


@router.post("/{campaign_id}/regenerate", response_model=CampaignResponse)
def regenerate(
    campaign_id: uuid.UUID,
    payload: RegenerateRequest,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return generate_campaign(
        db, owned_campaign(db, campaign_id, user.id), payload.asset_type
    )


def change_status(db: Session, campaign: Campaign, new_status: str) -> Campaign:
    campaign.status = new_status
    db.commit()
    return owned_campaign(db, campaign.id, campaign.user_id)


@router.post("/{campaign_id}/approve", response_model=CampaignResponse)
def approve(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    campaign = owned_campaign(db, campaign_id, user.id)
    if not campaign.assets:
        raise HTTPException(status_code=409, detail="Gere conteúdo antes de aprovar")
    return change_status(db, campaign, "approved")


@router.post("/{campaign_id}/archive", response_model=CampaignResponse)
def archive(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return change_status(db, owned_campaign(db, campaign_id, user.id), "archived")


@router.post("/{campaign_id}/duplicate", response_model=CampaignResponse, status_code=201)
def duplicate(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    source = owned_campaign(db, campaign_id, user.id)
    payload = CampaignCreate(
        title=f"Cópia de {source.title}",
        theme=source.theme,
        input_type=source.input_type,
        input_text=source.input_text,
        audience=source.audience,
        objective=source.objective,
        tone=source.tone,
        cta=source.cta,
    )
    return create_campaign(db, user, payload)


@router.delete("/{campaign_id}", status_code=204)
def delete(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    db.delete(owned_campaign(db, campaign_id, user.id))
    db.commit()
    return Response(status_code=204)

