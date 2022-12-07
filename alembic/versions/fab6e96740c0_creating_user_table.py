"""creating user table

Revision ID: fab6e96740c0
Revises: 7e04476a5463
Create Date: 2022-12-04 22:46:43.707501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fab6e96740c0'
down_revision = '7e04476a5463'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('user_name')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
