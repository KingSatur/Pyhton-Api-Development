"""alter_post_table

Revision ID: c18ac27fc951
Revises: b21d9245c40d
Create Date: 2022-04-17 22:43:25.185809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c18ac27fc951'
down_revision = 'b21d9245c40d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(),  server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column(
        'rating', sa.Integer(), nullable=False,  server_default='0'))


def downgrade():
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'rating')
    op.drop_column('posts', 'created_at')
