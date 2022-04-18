"""create_user_table

Revision ID: da969be9e724
Revises: c18ac27fc951
Create Date: 2022-04-17 22:54:37.698680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da969be9e724'
down_revision = 'c18ac27fc951'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('firstName', sa.String(),
                  nullable=False),
        sa.Column('lastName', sa.String(),
                  nullable=False),
        sa.Column('email', sa.String(),
                  nullable=False,),
        sa.Column('password', sa.String(),
                  nullable=False, ),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('now()'),
                  ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
