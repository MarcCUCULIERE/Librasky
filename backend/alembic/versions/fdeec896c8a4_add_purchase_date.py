"""Add_purchase_date

Revision ID: fdeec896c8a4
Revises: 
Create Date: 2025-02-27 00:33:43.609249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdeec896c8a4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('whiskies', sa.Column('purchase_date', sa.Date(), nullable=True))

def downgrade():
    op.drop_column('whiskies', 'purchase_date')
