"""add status to story

Revision ID: 49e8baf1f8a4
Revises: f07db47ad149
Create Date: 2020-03-04 16:18:43.962459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e8baf1f8a4'
down_revision = 'f07db47ad149'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TYPE IF EXISTS status_enum")
    op.execute("CREATE TYPE status_enum AS Enum('APPROVED', 'REJECTED')")
    op.add_column('user_story', sa.Column('status', sa.Enum('APPROVED', 'REJECTED', name='status_enum'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_story', 'status')
    op.execute("DROP TYPE IF EXISTS status_enum")
    # ### end Alembic commands ###
