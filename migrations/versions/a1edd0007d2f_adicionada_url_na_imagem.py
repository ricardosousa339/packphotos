"""adicionada url na imagem

Revision ID: a1edd0007d2f
Revises: b0e91e362d40
Create Date: 2024-09-03 23:49:15.827264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1edd0007d2f'
down_revision: Union[str, None] = 'b0e91e362d40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('photos', sa.Column('url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('photos', 'url')
