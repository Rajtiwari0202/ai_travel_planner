"""initial public demo schema

Revision ID: 20260623_0001
Revises:
Create Date: 2026-06-23
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260623_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trip_records",
        sa.Column("trip_id", sa.String(length=64), primary_key=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("owner_hash", sa.String(length=96), nullable=True),
        sa.Column("request_json", sa.Text(), nullable=False),
        sa.Column("plan_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_trip_records_status", "trip_records", ["status"])
    op.create_index("ix_trip_records_owner_hash", "trip_records", ["owner_hash"])
    op.create_index("ix_trip_owner_created", "trip_records", ["owner_hash", "created_at"])
    op.create_table(
        "agent_event_records",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("trip_id", sa.String(length=64), sa.ForeignKey("trip_records.trip_id", ondelete="CASCADE"), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_event_records_trip_id", "agent_event_records", ["trip_id"])
    op.create_index("ix_agent_event_records_event_id", "agent_event_records", ["event_id"], unique=True)
    op.create_index("ix_agent_event_trip_sequence", "agent_event_records", ["trip_id", "sequence"])


def downgrade() -> None:
    op.drop_index("ix_agent_event_trip_sequence", table_name="agent_event_records")
    op.drop_index("ix_agent_event_records_event_id", table_name="agent_event_records")
    op.drop_index("ix_agent_event_records_trip_id", table_name="agent_event_records")
    op.drop_table("agent_event_records")
    op.drop_index("ix_trip_owner_created", table_name="trip_records")
    op.drop_index("ix_trip_records_owner_hash", table_name="trip_records")
    op.drop_index("ix_trip_records_status", table_name="trip_records")
    op.drop_table("trip_records")
