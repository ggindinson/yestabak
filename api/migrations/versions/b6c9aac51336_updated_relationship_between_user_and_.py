"""updated relationship between user and addresses

Revision ID: b6c9aac51336
Revises: 69ecc8e69a91
Create Date: 2023-03-19 22:47:49.880555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6c9aac51336"
down_revision = "69ecc8e69a91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
            comment="Уникальный user_id пользователя из телеграма",
        ),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_column("users", "id")
    # ### end Alembic commands ###
