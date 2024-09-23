"""Adicionado price a photo

Revision ID: 7f380ac024d0
Revises: a9878c954ef7
Create Date: 2024-09-20 14:40:40.931842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f380ac024d0'
down_revision: Union[str, None] = 'a9878c954ef7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  # Verificar se a coluna 'price' já existe antes de adicioná-la
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [column['name'] for column in inspector.get_columns('photos')]
    
    if 'price' not in columns:
        op.add_column('photos', sa.Column('price', sa.Float(), nullable=False, server_default='0.0'))
        op.alter_column('photos', 'price', server_default=None)



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('photos', 'price')
    # ### end Alembic commands ###
