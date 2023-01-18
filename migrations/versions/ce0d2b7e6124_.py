"""empty message

Revision ID: ce0d2b7e6124
Revises: c8cf8d1df515
Create Date: 2023-01-18 07:58:05.298756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce0d2b7e6124'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('section', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


# def downgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     with op.batch_alter_table('user', schema=None) as batch_op:
#         batch_op.drop_column('section')

#     # ### end Alembic commands ###
