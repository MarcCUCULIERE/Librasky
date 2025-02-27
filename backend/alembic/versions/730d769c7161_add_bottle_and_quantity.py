"""Add_bottle_and_quantity

Revision ID: 730d769c7161
Revises: 1c5288ab09e5
Create Date: 2025-02-27 22:10:33.717662

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# Déclarations requises par Alembic
revision = '730d769c7161'
down_revision = '1c5288ab09e5'
branch_labels = None
depends_on = None

def upgrade():
    # Vérifier les colonnes existantes
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('whiskies')]
    
    # Ajout des colonnes si elles n'existent pas
    if 'quantity' not in columns:
        op.add_column('whiskies', sa.Column('quantity', sa.Integer(), nullable=True, server_default='1'))
    
    if 'bottles' not in columns:
        op.add_column('whiskies', sa.Column('bottles', sa.JSON(), nullable=True))
        # Initialiser les données bottles pour les entrées existantes
        conn.execute("""
            UPDATE whiskies 
            SET bottles = json('[{"id": 1, "is_opened": false, "remaining_percentage": 100}]')
            WHERE bottles IS NULL
        """)

def downgrade():
    # Vérifier les colonnes existantes avant de les supprimer
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns('whiskies')]
    
    if 'bottles' in columns:
        op.drop_column('whiskies', 'bottles')
    if 'quantity' in columns:
        op.drop_column('whiskies', 'quantity')