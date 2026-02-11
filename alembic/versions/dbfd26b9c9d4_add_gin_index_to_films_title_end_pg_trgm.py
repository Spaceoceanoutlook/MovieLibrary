"""add gin index to films.title end pg_trgm

Revision ID: dbfd26b9c9d4
Revises: a60a7d4892ab
Create Date: 2025-09-08 14:35:16.134829

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "dbfd26b9c9d4"
down_revision: Union[str, Sequence[str], None] = "a60a7d4892ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
