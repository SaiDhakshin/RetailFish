"""add ohlcv lookup index

Revision ID: e0464b3d7a04
Revises: 6c1426fb8614
Create Date: 2026-07-09 15:38:37.306417

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0464b3d7a04'
down_revision: Union[str, Sequence[str], None] = '6c1426fb8614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
