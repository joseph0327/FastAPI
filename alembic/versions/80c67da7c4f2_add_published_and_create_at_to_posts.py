"""add published and create_at to posts

Revision ID: 80c67da7c4f2
Revises: a3f9cc69559b
Create Date: 2023-09-11 17:24:18.420620

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80c67da7c4f2'
down_revision: Union[str, None] = 'a3f9cc69559b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
