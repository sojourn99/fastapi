"""add phone number

Revision ID: 296d2663e8c9
Revises: 31072b0cd5f7
Create Date: 2023-04-05 16:44:52.350122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '296d2663e8c9'
down_revision = '31072b0cd5f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
