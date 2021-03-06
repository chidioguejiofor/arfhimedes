"""Modify UserStory model

Revision ID: f07db47ad149
Revises: 5f64bcfe93e0
Create Date: 2020-03-04 15:04:09.764289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f07db47ad149'
down_revision = '5f64bcfe93e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_story', sa.Column('assignee_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_story', 'user', ['assignee_id'], ['id'], onupdate='CASCADE', ondelete='RESTRICT')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_story', type_='foreignkey')
    op.drop_column('user_story', 'assignee_id')
    # ### end Alembic commands ###
