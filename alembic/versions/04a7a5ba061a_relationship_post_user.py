"""relationship_post_user

Revision ID: 04a7a5ba061a
Revises: da969be9e724
Create Date: 2022-04-17 23:08:48.569964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04a7a5ba061a'
down_revision = 'da969be9e724'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts',
                          referent_table='users', local_cols=['user_id'],
                          remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'user_id')
