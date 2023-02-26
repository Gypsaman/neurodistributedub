"""empty message

Revision ID: 8337475d9e1c
Revises: 24a40d96cfd4
Create Date: 2023-02-24 12:27:51.431236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8337475d9e1c'
down_revision = '24a40d96cfd4'
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
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('date_available', sa.DateTime(), nullable=True),
    sa.Column('date_due', sa.DateTime(), nullable=True),
    sa.Column('submitted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.String(length=10), nullable=False),
    sa.Column('answer_id', sa.String(length=10), nullable=False),
    sa.Column('display_order', sa.Integer(), nullable=True),
    sa.Column('answer_txt', sa.String(length=100), nullable=True),
    sa.Column('corrrect_answer', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'question_id', 'answer_id')
    )
    op.create_table('questions',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.String(length=10), nullable=False),
    sa.Column('question', sa.String(length=500), nullable=True),
    sa.Column('display_order', sa.Integer(), nullable=True),
    sa.Column('answer_chosen', sa.String(length=20), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'question_id')
    )
    # op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.drop_table('questions')
    op.drop_table('answers')
    op.drop_table('quizzes')
    op.drop_table('User')
    # ### end Alembic commands ###
