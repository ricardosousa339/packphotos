"""adicionada url na imagem

Revision ID: b0e91e362d40
Revises: a2625a0df020
Create Date: 2024-09-03 23:43:35.721291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0e91e362d40'
down_revision: Union[str, None] = 'a2625a0df020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
