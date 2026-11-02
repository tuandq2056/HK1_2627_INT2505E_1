"""create orders and order_items

Revision ID: 6b3f4cffdeb0
Revises: 4bbb2688c4c8
Create Date: 2026-11-02 23:25:59.455680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b3f4cffdeb0'
down_revision = '4bbb2688c4c8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.Column('unit_price_cents', sa.Integer(), nullable=False),
    sa.CheckConstraint('qty > 0', name='ck_order_items_qty_positive'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id', 'product_id', name='uq_order_items_order_product')
    )
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_order_items_order_id'), ['order_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_order_items_product_id'), ['product_id'], unique=False)



def downgrade():
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_order_items_product_id'))
        batch_op.drop_index(batch_op.f('ix_order_items_order_id'))

    op.drop_table('order_items')
    op.drop_table('orders')
