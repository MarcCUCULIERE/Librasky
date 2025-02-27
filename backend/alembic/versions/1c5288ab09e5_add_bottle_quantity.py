"""Add_bottle_quantity

Revision ID: 1c5288ab09e5
Revises: fdeec896c8a4
Create Date: 2025-02-27 22:01:38.942785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON


# revision identifiers, used by Alembic.
revision = '1c5288ab09e5'
down_revision = 'fdeec896c8a4'
branch_labels = None
depends_on = None


# Pour supporter SQLite et PostgreSQL
def get_json_type():
    from sqlalchemy.engine.reflection import Inspector
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    if inspector.get_table_names():  # Check if any tables exist
        dialectname = conn.dialect.name
        if dialectname == 'postgresql':
            return JSON
        return SQLiteJSON
    return SQLiteJSON

def upgrade():
    json_type = get_json_type()
    
    # Ajout des nouvelles colonnes
    op.add_column('whiskies', sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('whiskies', sa.Column('bottles', json_type, nullable=True))
    
    # Initialisation des données existantes
    conn = op.get_bind()
    conn.execute("""
        UPDATE whiskies 
        SET bottles = '[{"id": 1, "is_opened": false, "remaining_percentage": 100}]'
        WHERE bottles IS NULL
    """)

def downgrade():
    op.drop_column('whiskies', 'bottles')
    op.drop_column('whiskies', 'quantity')