"""add last few columns to posts table

Revision ID: 21329cae7b05
Revises: cee9ba1da2c9
Create Date: 2023-04-05 16:29:24.759390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21329cae7b05'
down_revision = 'cee9ba1da2c9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()')),)


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
