"""Description of the migration

Revision ID: 58e8c16cd6b1
Revises: 01f32c6b3c8b
Create Date: 2025-02-24 10:22:42.842143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58e8c16cd6b1'
down_revision: Union[str, None] = '01f32c6b3c8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
