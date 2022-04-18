"""fix_post_table

Revision ID: 6c144f41d9af
Revises: 737de6150e3e
Create Date: 2022-04-17 23:24:03.251274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c144f41d9af'
down_revision = '737de6150e3e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('posts', 'rating', server_default='0', type_=sa.Integer())
    op.alter_column('posts', 'created_at', server_default='now()',
                    type_=sa.TIMESTAMP(timezone=True))


def downgrade():
    op.alter_column('posts', 'rating', server_default='now()',
                    type_=sa.TIMESTAMP(timezone=True))
    op.alter_column('posts', 'created_at', type_=sa.String)
