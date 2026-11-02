"""create products

Revision ID: 4bbb2688c4c8
Revises: 
Create Date: 2026-11-02 23:24:37.790710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bbb2688c4c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=True),
    sa.Column('price_cents', sa.Integer(), nullable=False),
    sa.Column('qty_in_stock', sa.Integer(), nullable=False),
    sa.Column('archived', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_products_archived'), ['archived'], unique=False)
        batch_op.create_index(batch_op.f('ix_products_sku'), ['sku'], unique=True)



def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_products_sku'))
        batch_op.drop_index(batch_op.f('ix_products_archived'))

    op.drop_table('products')
