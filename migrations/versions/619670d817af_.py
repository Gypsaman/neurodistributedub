"""empty message

Revision ID: 619670d817af
Revises: 
Create Date: 2025-01-22 16:43:33.889096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '619670d817af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=50), nullable=True))


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
