"""empty message

Revision ID: d2fae7edd236
Revises: 
Create Date: 2022-12-30 08:26:41.973736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2fae7edd236'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('asset_type', sa.Integer(), nullable=True),
    sa.Column('network', sa.String(length=10), nullable=True),
    sa.Column('asset_address', sa.Integer(), nullable=True),
    sa.Column('time_added', sa.DateTime(), nullable=True),
    sa.Column('assignment', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('asset_address')
    )
    op.create_table('assignments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('due', sa.DateTime(), nullable=True),
    sa.Column('inputtype', sa.String(length=10), nullable=True),
    sa.Column('grader', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('grades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('assignment', sa.Integer(), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('dategraded', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('password_reset',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('password_phrase', sa.Integer(), nullable=True),
    sa.Column('phrase_expires', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('wallet', sa.Integer(), nullable=True),
    sa.Column('blockNumber', sa.Integer(), nullable=True),
    sa.Column('timeStamp', sa.DateTime(), nullable=True),
    sa.Column('hash', sa.Integer(), nullable=True),
    sa.Column('nonce', sa.Integer(), nullable=True),
    sa.Column('blockHash', sa.Integer(), nullable=True),
    sa.Column('transactionIndex', sa.Integer(), nullable=True),
    sa.Column('trans_from', sa.Integer(), nullable=True),
    sa.Column('trans_to', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('gas', sa.Integer(), nullable=True),
    sa.Column('gasPrice', sa.Integer(), nullable=True),
    sa.Column('isError', sa.Boolean(), nullable=True),
    sa.Column('txreceipt_status', sa.Boolean(), nullable=True),
    sa.Column('input', sa.String(), nullable=True),
    sa.Column('contractAddress', sa.Integer(), nullable=True),
    sa.Column('cumulativeGasUsed', sa.Integer(), nullable=True),
    sa.Column('gasUsed', sa.Integer(), nullable=True),
    sa.Column('confirmations', sa.String(), nullable=True),
    sa.Column('methodId', sa.String(), nullable=True),
    sa.Column('functionName', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('student_id', sa.String(length=10), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('wallet', sa.Integer(), nullable=True),
    sa.Column('privatekey', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet')
    op.drop_table('user')
    op.drop_table('transactions')
    op.drop_table('password_reset')
    op.drop_table('grades')
    op.drop_table('assignments')
    op.drop_table('assets')
    # ### end Alembic commands ###
