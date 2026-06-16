"""Add campaign media."""

from alembic import op
import sqlalchemy as sa

revision = "20260616_0002"
down_revision = "20260615_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "campaign_media",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "campaign_id",
            sa.Uuid(),
            sa.ForeignKey("campaigns.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(30), nullable=False),
        sa.Column("media_type", sa.String(30), nullable=False),
        sa.Column("role", sa.String(60), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(120), nullable=False),
        sa.Column("provider", sa.String(50)),
        sa.Column("model", sa.String(100)),
        sa.Column("prompt", sa.Text()),
        sa.Column("metadata", sa.JSON()),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_campaign_media_campaign_id", "campaign_media", ["campaign_id"])
    op.create_index("ix_campaign_media_media_type", "campaign_media", ["media_type"])
    op.create_index("ix_campaign_media_role", "campaign_media", ["role"])


def downgrade() -> None:
    op.drop_table("campaign_media")
