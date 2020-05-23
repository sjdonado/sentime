"""empty message

Revision ID: 07d947124ef4
Revises: 
Create Date: 2020-05-22 03:37:35.092428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07d947124ef4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('searches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('query', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('search_id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('pos_score', sa.Integer(), nullable=False),
    sa.Column('neg_score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['search_id'], ['searches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    op.drop_table('searches')
    op.drop_table('users')
    # ### end Alembic commands ###
