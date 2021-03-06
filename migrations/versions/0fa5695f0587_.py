"""empty message

Revision ID: 0fa5695f0587
Revises: 
Create Date: 2019-08-11 19:52:46.161912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa5695f0587'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buyer_details', sa.Column('phone_number', sa.String(length=20), nullable=False))
    op.add_column('products', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'price')
    op.drop_column('buyer_details', 'phone_number')
    # ### end Alembic commands ###
