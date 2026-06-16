import base64
import time
import uuid
from pathlib import Path

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.models import Campaign, CampaignMedia, GenerationLog


class ImageGenerationUnavailable(RuntimeError):
    pass


def build_social_image_prompt(campaign: Campaign, result: dict | None = None) -> str:
    result = result or {}
    linkedin_post = result.get("linkedin_post") or _asset_content(campaign, "linkedin_post")
    instagram_caption = result.get("instagram_caption") or _asset_content(
        campaign, "instagram_caption"
    )
    strategy = result.get("strategy") or campaign.strategy or {}
    source_text = "\n\n".join(
        item
        for item in [
            f"Tema: {campaign.theme or campaign.title}",
            f"Publico-alvo: {campaign.audience or 'empresarios e gestores'}",
            f"Objetivo: {campaign.objective or 'gerar autoridade'}",
            f"Tom: {campaign.tone or 'consultivo'}",
            f"Dor principal: {strategy.get('pain', '')}",
            f"Solucao proposta: {strategy.get('solution', '')}",
            f"Post LinkedIn: {linkedin_post}",
            f"Legenda Instagram: {instagram_caption}",
        ]
        if item.strip()
    )
    return (
        "Crie uma imagem quadrada 1:1 para acompanhar uma publicacao B2B no LinkedIn "
        "e no Instagram. Estilo profissional, moderno, claro e confiavel. "
        "Use uma composicao visual que comunique transformacao digital, eficiencia "
        "operacional e automacao empresarial sem parecer generica. "
        "Nao inclua textos pequenos, marcas d'agua, logotipos falsos ou interfaces "
        "ilegiveis. Evite excesso de elementos. A imagem deve funcionar sem depender "
        "de texto dentro da arte.\n\n"
        f"Contexto da campanha:\n{source_text}"
    )


def generate_social_image(
    db: Session,
    campaign: Campaign,
    result: dict | None = None,
    *,
    replace_existing: bool = True,
) -> CampaignMedia:
    settings = get_settings()
    if not settings.openai_api_key:
        raise ImageGenerationUnavailable("OPENAI_API_KEY nao configurada")

    prompt = build_social_image_prompt(campaign, result)
    started = time.perf_counter()
    response = OpenAI(api_key=settings.openai_api_key).images.generate(
        model=settings.openai_image_model,
        prompt=prompt,
        size=settings.openai_image_size,
        quality=settings.openai_image_quality,
    )
    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    storage_dir = Path(settings.media_storage_dir)
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{campaign.id}-social-image-{uuid.uuid4().hex}.png"
    file_path = storage_dir / file_name
    file_path.write_bytes(image_bytes)

    media = None
    if replace_existing:
        media = next((item for item in campaign.media if item.role == "social_image"), None)
    if media:
        _delete_if_inside_storage(media.file_path, storage_dir)
        media.file_path = str(file_path)
        media.file_name = file_name
        media.mime_type = "image/png"
        media.provider = "openai"
        media.model = settings.openai_image_model
        media.prompt = prompt
        media.status = "ready"
        media.media_metadata = _metadata(settings)
    else:
        media = CampaignMedia(
            campaign_id=campaign.id,
            channel="social",
            media_type="image",
            role="social_image",
            file_path=str(file_path),
            file_name=file_name,
            mime_type="image/png",
            provider="openai",
            model=settings.openai_image_model,
            prompt=prompt,
            status="ready",
            media_metadata=_metadata(settings),
        )
        db.add(media)

    db.add(
        GenerationLog(
            campaign_id=campaign.id,
            node_name="image_generator",
            provider="openai",
            model=settings.openai_image_model,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
            status="success",
            error_message=None,
        )
    )
    return media


def log_image_generation_error(db: Session, campaign: Campaign, error: Exception) -> None:
    settings = get_settings()
    db.add(
        GenerationLog(
            campaign_id=campaign.id,
            node_name="image_generator",
            provider="openai",
            model=settings.openai_image_model,
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency_ms=None,
            status="error",
            error_message=str(error),
        )
    )


def _asset_content(campaign: Campaign, asset_type: str) -> str:
    asset = next((item for item in campaign.assets if item.asset_type == asset_type), None)
    return asset.content if asset else ""


def _metadata(settings) -> dict:
    return {
        "channels": ["linkedin", "instagram"],
        "size": settings.openai_image_size,
        "quality": settings.openai_image_quality,
        "format": "png",
    }


def _delete_if_inside_storage(file_path: str, storage_dir: Path) -> None:
    path = Path(file_path)
    try:
        if path.resolve().is_relative_to(storage_dir.resolve()) and path.exists():
            path.unlink()
    except OSError:
        pass
