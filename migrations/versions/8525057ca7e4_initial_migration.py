"""Initial migration

Revision ID: 8525057ca7e4
Revises: ac5278d2d4c8
Create Date: 2024-09-03 11:51:05.678870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8525057ca7e4'
down_revision: Union[str, None] = 'ac5278d2d4c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###