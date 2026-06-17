import json
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.graph.content_graph import content_graph
from app.models import Campaign, CampaignAsset, GenerationLog, User
from app.schemas.campaign import CampaignCreate
from app.services.image_service import (
    ImageGenerationUnavailable,
    generate_social_image,
    log_image_generation_error,
)


def owned_campaign(db: Session, campaign_id: uuid.UUID, user_id: uuid.UUID) -> Campaign:
    campaign = db.scalar(
        select(Campaign)
        .options(selectinload(Campaign.assets), selectinload(Campaign.media))
        .where(Campaign.id == campaign_id, Campaign.user_id == user_id)
        .execution_options(populate_existing=True)
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada")
    return campaign


def create_campaign(db: Session, user: User, payload: CampaignCreate) -> Campaign:
    campaign = Campaign(user_id=user.id, **payload.model_dump())
    db.add(campaign)
    db.commit()
    return owned_campaign(db, campaign.id, user.id)


def generate_campaign(db: Session, campaign: Campaign, requested_asset: str = "all") -> Campaign:
    campaign.status = "processing"
    db.commit()
    state = {
        "campaign_id": str(campaign.id),
        "user_id": str(campaign.user_id),
        "theme": campaign.theme or campaign.title,
        "input_text": campaign.input_text,
        "input_type": campaign.input_type,
        "audience": campaign.audience or "",
        "objective": campaign.objective or "",
        "tone": campaign.tone or "",
        "cta": campaign.cta or "",
        "requested_asset": requested_asset,
    }
    try:
        result = content_graph.invoke(state)
        persist_result(db, campaign, result, requested_asset)
        if requested_asset in {"all", "linkedin_post", "instagram_caption"}:
            try:
                generate_social_image(db, campaign, result)
            except ImageGenerationUnavailable as exc:
                log_image_generation_error(db, campaign, exc)
            except Exception as exc:
                log_image_generation_error(db, campaign, exc)
        campaign.status = "generated"
        campaign.strategy = result.get("strategy")
        campaign.quality_score = result.get("quality_score")
        campaign.review_notes = result.get("review_notes")
    except Exception:
        campaign.status = "error"
        db.commit()
        raise
    db.commit()
    return owned_campaign(db, campaign.id, campaign.user_id)


def persist_result(db: Session, campaign: Campaign, result: dict, requested_asset: str) -> None:
    assets = {
        "linkedin_post": ("linkedin", None, result.get("linkedin_post"), None),
        "instagram_caption": ("instagram", None, result.get("instagram_caption"), None),
        "youtube_title": ("youtube", result.get("youtube_title"), result.get("youtube_title"), None),
        "youtube_description": ("youtube", None, result.get("youtube_description"), None),
        "youtube_script": (
            "youtube",
            result.get("youtube_title"),
            result.get("youtube_script"),
            {"scenes": result.get("video_scenes", [])},
        ),
        "hashtags": ("all", None, "\n".join(result.get("hashtags", [])), {"items": result.get("hashtags", [])}),
        "cta": ("all", None, campaign.cta or result.get("strategy", {}).get("cta", ""), None),
        "video_scenes": (
            "youtube",
            None,
            json.dumps(result.get("video_scenes", []), ensure_ascii=False, indent=2),
            {"items": result.get("video_scenes", [])},
        ),
    }
    requested = set(assets) if requested_asset == "all" else {requested_asset}
    if requested_asset == "youtube_script":
        requested.update({"youtube_title", "youtube_description", "video_scenes"})
    for asset_type in requested:
        channel, title, content, metadata = assets[asset_type]
        if content is None:
            continue
        asset = next((item for item in campaign.assets if item.asset_type == asset_type), None)
        if asset:
            asset.title, asset.content, asset.asset_metadata, asset.status = title, content, metadata, "draft"
        else:
            db.add(
                CampaignAsset(
                    campaign_id=campaign.id,
                    channel=channel,
                    asset_type=asset_type,
                    title=title,
                    content=content,
                    asset_metadata=metadata,
                )
            )
    for log in result.get("logs", []):
        db.add(GenerationLog(campaign_id=campaign.id, **log))
