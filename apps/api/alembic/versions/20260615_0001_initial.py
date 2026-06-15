"""Initial schema."""

from alembic import op
import sqlalchemy as sa

revision = "20260615_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table(
        "campaigns",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(240), nullable=False),
        sa.Column("theme", sa.Text()),
        sa.Column("input_type", sa.String(30), nullable=False),
        sa.Column("input_text", sa.Text()),
        sa.Column("audience", sa.String(240)),
        sa.Column("objective", sa.String(80)),
        sa.Column("tone", sa.String(80)),
        sa.Column("cta", sa.Text()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("quality_score", sa.Integer()),
        sa.Column("review_notes", sa.JSON()),
        sa.Column("strategy", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_campaigns_user_id", "campaigns", ["user_id"])
    op.create_index("ix_campaigns_status", "campaigns", ["status"])
    op.create_table(
        "campaign_assets",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "campaign_id",
            sa.Uuid(),
            sa.ForeignKey("campaigns.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(30), nullable=False),
        sa.Column("asset_type", sa.String(60), nullable=False),
        sa.Column("title", sa.String(300)),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_campaign_assets_campaign_id", "campaign_assets", ["campaign_id"])
    op.create_index("ix_campaign_assets_asset_type", "campaign_assets", ["asset_type"])
    op.create_table(
        "generation_logs",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "campaign_id",
            sa.Uuid(),
            sa.ForeignKey("campaigns.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("node_name", sa.String(80), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("prompt_tokens", sa.Integer()),
        sa.Column("completion_tokens", sa.Integer()),
        sa.Column("total_tokens", sa.Integer()),
        sa.Column("latency_ms", sa.Integer()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("error_message", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_generation_logs_campaign_id", "generation_logs", ["campaign_id"])


def downgrade() -> None:
    op.drop_table("generation_logs")
    op.drop_table("campaign_assets")
    op.drop_table("campaigns")
    op.drop_table("users")
