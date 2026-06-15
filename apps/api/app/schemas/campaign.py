import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CampaignStatus = Literal["draft", "processing", "generated", "review", "approved", "archived", "error"]
AssetType = Literal[
    "linkedin_post",
    "instagram_caption",
    "youtube_script",
    "youtube_title",
    "youtube_description",
    "hashtags",
    "cta",
    "video_scenes",
]


class CampaignCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    theme: str | None = None
    input_type: Literal["theme", "text"] = "theme"
    input_text: str | None = None
    audience: str | None = None
    objective: str | None = None
    tone: str | None = None
    cta: str | None = None

    @model_validator(mode="after")
    def require_source(self):
        if not (self.theme and self.theme.strip()) and not (self.input_text and self.input_text.strip()):
            raise ValueError("Informe um tema ou texto de entrada")
        return self


class AssetUpdate(BaseModel):
    content: str = Field(min_length=1)
    status: Literal["draft", "review", "approved"] = "review"


class RegenerateRequest(BaseModel):
    asset_type: Literal["linkedin_post", "instagram_caption", "youtube_script", "hashtags", "all"]


class AssetResponse(BaseModel):
    id: uuid.UUID
    campaign_id: uuid.UUID
    channel: str
    asset_type: str
    title: str | None
    content: str
    asset_metadata: dict | list | None
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CampaignResponse(BaseModel):
    id: uuid.UUID
    title: str
    theme: str | None
    input_type: str
    input_text: str | None
    audience: str | None
    objective: str | None
    tone: str | None
    cta: str | None
    status: CampaignStatus
    quality_score: int | None
    review_notes: list | None
    strategy: dict | None
    created_at: datetime
    updated_at: datetime
    assets: list[AssetResponse] = []
    model_config = ConfigDict(from_attributes=True)

