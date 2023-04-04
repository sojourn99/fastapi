"""create posts table

Revision ID: b7048465a4f5
Revises: 
Create Date: 2023-04-04 16:36:11.122318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7048465a4f5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id",
                    sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("title", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
