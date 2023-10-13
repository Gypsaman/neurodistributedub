"""empty message

Revision ID: 2e8b04ae9719
Revises: 8381ceb3431a
Create Date: 2023-02-26 15:43:35.813959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e8b04ae9719'
down_revision = '8381ceb3431a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('User',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('email', sa.String(length=50), nullable=True),
    # sa.Column('password', sa.String(length=50), nullable=True),
    # sa.Column('first_name', sa.String(length=50), nullable=True),
    # sa.Column('last_name', sa.String(length=50), nullable=True),
    # sa.Column('student_id', sa.String(length=10), nullable=True),
    # sa.Column('section', sa.Integer(), nullable=True),
    # sa.Column('role', sa.String(length=10), nullable=True),
    # sa.ForeignKeyConstraint(['section'], ['sections.id'], ),
    # sa.PrimaryKeyConstraint('id'),
    # sa.UniqueConstraint('email'),
    # sa.UniqueConstraint('student_id')
    # )
    # op.drop_table('user')
    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.create_foreign_key('questions', 'questions', ['question_id'], ['question_id'])

    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('multiple_retries', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.drop_column('multiple_retries')

    with op.batch_alter_table('answers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.VARCHAR(length=50), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('student_id', sa.VARCHAR(length=10), nullable=True),
    sa.Column('role', sa.VARCHAR(length=10), nullable=True),
    sa.Column('section', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['section'], ['sections.id'], name='usersection'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('student_id')
    )
    op.drop_table('User')
    # ### end Alembic commands ###