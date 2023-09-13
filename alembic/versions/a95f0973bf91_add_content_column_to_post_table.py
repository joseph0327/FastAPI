"""add content column to post table

Revision ID: a95f0973bf91
Revises: 14787b4b4317
Create Date: 2023-09-11 16:46:24.166746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a95f0973bf91'
down_revision: Union[str, None] = '14787b4b4317'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
