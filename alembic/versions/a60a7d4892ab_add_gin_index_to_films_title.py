"""add gin index to films.title

Revision ID: a60a7d4892ab
Revises: b47c34e44e60
Create Date: 2025-09-08 14:31:07.547071

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a60a7d4892ab"
down_revision: Union[str, Sequence[str], None] = "b47c34e44e60"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Установка расширения
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # Создание индекса
    op.create_index(
        "idx_films_title_trgm",
        "films",
        ["title"],
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )


def downgrade():
    op.drop_index("idx_films_title_trgm", table_name="films")
