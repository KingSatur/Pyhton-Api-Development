"""create_post_table

Revision ID: b21d9245c40d
Revises: 
Create Date: 2022-04-17 22:34:34.935909

"""
from alembic import op
import alembic
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b21d9245c40d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
