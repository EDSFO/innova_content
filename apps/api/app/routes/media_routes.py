import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models import Campaign, CampaignMedia, User
from app.schemas.campaign import CampaignMediaResponse
from app.security import get_current_user
from app.services.campaign_service import owned_campaign
from app.services.image_service import (
    ImageGenerationUnavailable,
    generate_social_image,
    log_image_generation_error,
)

router = APIRouter(prefix="/media", tags=["media"])


@router.post("/campaigns/{campaign_id}/social-image", response_model=CampaignMediaResponse)
def generate_campaign_social_image(
    campaign_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    campaign = owned_campaign(db, campaign_id, user.id)
    try:
        media = generate_social_image(db, campaign)
    except ImageGenerationUnavailable as exc:
        log_image_generation_error(db, campaign, exc)
        db.commit()
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        log_image_generation_error(db, campaign, exc)
        db.commit()
        raise HTTPException(
            status_code=502,
            detail="Falha ao gerar imagem. Verifique a chave/modelo da OpenAI e tente novamente.",
        ) from exc
    db.commit()
    db.refresh(media)
    return media


@router.get("/{media_id}/download")
def download_media(
    media_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    media = db.scalar(
        select(CampaignMedia)
        .join(Campaign)
        .where(CampaignMedia.id == media_id, Campaign.user_id == user.id)
    )
    if not media:
        raise HTTPException(status_code=404, detail="Midia nao encontrada")
    path = Path(media.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Arquivo de midia nao encontrado")
    return FileResponse(path, media_type=media.mime_type, filename=media.file_name)
