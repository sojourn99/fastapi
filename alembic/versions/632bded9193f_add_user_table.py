"""add user table

Revision ID: 632bded9193f
Revises: 9bfe5961cc4b
Create Date: 2023-04-05 16:14:47.337580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '632bded9193f'
down_revision = '9bfe5961cc4b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
