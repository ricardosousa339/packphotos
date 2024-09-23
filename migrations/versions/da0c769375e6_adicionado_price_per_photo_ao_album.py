"""Adicionado price_per_photo ao Album

Revision ID: da0c769375e6
Revises: 7f380ac024d0
Create Date: 2024-09-20 16:29:01.461691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da0c769375e6'
down_revision: Union[str, None] = '7f380ac024d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('albums', sa.Column('price_per_photo', sa.Float(), nullable=False, server_default='0.0'))
    # ### end Alembic commands ###
    op.alter_column('albums', 'price_per_photo', server_default=None)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('albums', 'price_per_photo')
    # ### end Alembic commands ###