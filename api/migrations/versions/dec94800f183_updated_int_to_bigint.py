"""Updated int to bigint

Revision ID: dec94800f183
Revises: 
Create Date: 2023-07-08 19:00:28.386895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dec94800f183'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_comment='ID of the category',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('categories_id_seq'::regclass)"))
    op.alter_column('items', 'category_id',
               existing_type=sa.BIGINT(),
               type_=sa.Integer(),
               existing_comment="ID of the item's category",
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'category_id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_comment="ID of the item's category",
               existing_nullable=False)
    op.alter_column('categories', 'id',
               existing_type=sa.Integer(),
               type_=sa.BIGINT(),
               existing_comment='ID of the category',
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('categories_id_seq'::regclass)"))
    # ### end Alembic commands ###