"""updated last_updated_at column

Revision ID: 04adff414b3d
Revises: f4a40c4de230
Create Date: 2023-02-18 15:08:00.409315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "04adff414b3d"
down_revision = "f4a40c4de230"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "items",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_comment="Дата создания товара",
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "items",
        "last_updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_comment="Дата последнего обновления данных товара",
    )
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_comment="Дата создания пользователя",
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "users",
        "last_updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_comment="Дата последнего обновления данных пользователя",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "last_updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_comment="Дата последнего обновления данных пользователя",
    )
    op.alter_column(
        "users",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_comment="Дата создания пользователя",
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "items",
        "last_updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_comment="Дата последнего обновления данных товара",
    )
    op.alter_column(
        "items",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_comment="Дата создания товара",
        existing_server_default=sa.text("now()"),
    )
    # ### end Alembic commands ###
