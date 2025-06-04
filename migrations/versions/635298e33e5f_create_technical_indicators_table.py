"""create technical_indicators table

Revision ID: 635298e33e5f
Revises: 
Create Date: 2025-06-04 19:09:37.485928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '635298e33e5f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'technical_indicators',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ticker', sa.String, nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('ma_5', sa.Float),
        sa.Column('ma_20', sa.Float),
        sa.Column('ma_50', sa.Float),
        sa.Column('rsi_14', sa.Float),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint('ticker', 'date', name='uix_ticker_date')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('technical_indicators')
