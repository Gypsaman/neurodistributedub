"""empty message

Revision ID: 7d50cfce229c
Revises: c580f7e1b3ba
Create Date: 2023-10-23 13:48:34.364706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d50cfce229c'
down_revision = 'c580f7e1b3ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_duedates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_header', sa.Integer(), nullable=True),
    sa.Column('section', sa.Integer(), nullable=True),
    sa.Column('date_due', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_header'], ['quiz_header.id'], ),
    sa.ForeignKeyConstraint(['section'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('quiz_header', schema=None) as batch_op:
        batch_op.drop_column('date_due')
        batch_op.drop_column('date_available')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_header', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_available', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('date_due', sa.DATETIME(), nullable=True))

    op.drop_table('quiz_duedates')
    # ### end Alembic commands ###