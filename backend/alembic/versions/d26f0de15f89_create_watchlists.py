"""create watchlists

Revision ID: d26f0de15f89
Revises: e0464b3d7a04
Create Date: 2026-07-11 07:56:34.881534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd26f0de15f89'
down_revision: Union[str, Sequence[str], None] = 'e0464b3d7a04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "watchlists",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "watchlist_items",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "watchlist_id",
            sa.Integer(),
            sa.ForeignKey(
                "watchlists.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "instrument_id",
            sa.Integer(),
            sa.ForeignKey(
                "instruments.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uq_watchlist_item",
        "watchlist_items",
        [
            "watchlist_id",
            "instrument_id",
        ],
    )

    op.create_index(
        "idx_watchlist_name",
        "watchlists",
        ["name"],
    )

    op.create_index(
        "idx_watchlist_item_watchlist",
        "watchlist_items",
        ["watchlist_id"],
    )

    op.create_index(
        "idx_watchlist_item_instrument",
        "watchlist_items",
        ["instrument_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "idx_watchlist_item_instrument",
        table_name="watchlist_items",
    )

    op.drop_index(
        "idx_watchlist_item_watchlist",
        table_name="watchlist_items",
    )

    op.drop_constraint(
        "uq_watchlist_item",
        "watchlist_items",
        type_="unique",
    )

    op.drop_table(
        "watchlist_items",
    )

    op.drop_index(
        "idx_watchlist_name",
        table_name="watchlists",
    )

    op.drop_table(
        "watchlists",
    )
