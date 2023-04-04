"""add content column to posts table

Revision ID: 9bfe5961cc4b
Revises: b7048465a4f5
Create Date: 2023-04-04 16:54:39.420502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bfe5961cc4b'
down_revision = 'b7048465a4f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
