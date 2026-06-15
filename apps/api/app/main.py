from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.routes.asset_routes import router as asset_router
from app.routes.auth_routes import router as auth_router
from app.routes.campaign_routes import router as campaign_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/api")
app.include_router(campaign_router, prefix="/api")
app.include_router(asset_router, prefix="/api")


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok", "environment": settings.app_env}
