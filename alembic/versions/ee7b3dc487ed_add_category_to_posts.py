"""add category to posts

Revision ID: ee7b3dc487ed
Revises: 
Create Date: 2026-05-01 12:55:22.333395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee7b3dc487ed'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('category', sa.String(length=100), nullable=True, server_default='community-life'))

def downgrade() -> None:
    op.drop_column('posts', 'category')
