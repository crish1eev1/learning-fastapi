"""create posts 2nd try

Revision ID: bd35f88f6d24
Revises: dcc80d5e57d7
Create Date: 2022-09-22 18:37:47.788026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd35f88f6d24'
down_revision = 'dcc80d5e57d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
