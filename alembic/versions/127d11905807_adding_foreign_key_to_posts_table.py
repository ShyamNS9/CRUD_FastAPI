"""adding foreign-key to posts table

Revision ID: 127d11905807
Revises: fab6e96740c0
Create Date: 2022-12-04 22:57:10.447375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127d11905807'
down_revision = 'fab6e96740c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'post_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
