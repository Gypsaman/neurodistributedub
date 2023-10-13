"""empty message

Revision ID: 19e81d0d39c9
Revises: 44d30823a996
Create Date: 2023-01-24 19:04:51.584263

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19e81d0d39c9'
down_revision = '44d30823a996'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.drop_column('comment')

    # ### end Alembic commands ###