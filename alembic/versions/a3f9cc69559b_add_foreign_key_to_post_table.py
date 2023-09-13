"""add foreign key to post table

Revision ID: a3f9cc69559b
Revises: 10e564fbf9e4
Create Date: 2023-09-11 17:12:49.140558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f9cc69559b'
down_revision: Union[str, None] = '10e564fbf9e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('owner_id', sa.Integer(), nullable=False),
                  )
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                            local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE'                       
                          )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
