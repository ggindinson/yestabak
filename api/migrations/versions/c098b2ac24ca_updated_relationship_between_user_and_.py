"""updated relationship between user and addresses

Revision ID: c098b2ac24ca
Revises: 4e5c6afac234
Create Date: 2023-03-19 15:54:05.874909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c098b2ac24ca"
down_revision = "4e5c6afac234"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "users", ["telegram_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    # ### end Alembic commands ###
