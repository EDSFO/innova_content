from typing import NotRequired, TypedDict


class ContentGenerationState(TypedDict):
    campaign_id: str
    user_id: str
    theme: str
    input_text: str | None
    input_type: str
    audience: str
    objective: str
    tone: str
    cta: str
    requested_asset: str
    summary: NotRequired[str]
    key_points: NotRequired[list[str]]
    strategy: NotRequired[dict]
    linkedin_post: NotRequired[str]
    instagram_caption: NotRequired[str]
    youtube_title: NotRequired[str]
    youtube_description: NotRequired[str]
    youtube_script: NotRequired[str]
    hashtags: NotRequired[list[str]]
    video_scenes: NotRequired[list[dict]]
    quality_score: NotRequired[int]
    review_notes: NotRequired[list[str]]
    errors: NotRequired[list[str]]
    persistence_ready: NotRequired[bool]
    logs: NotRequired[list[dict]]

