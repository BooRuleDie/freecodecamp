"""add foreign key to posts table

Revision ID: e88e89e764b5
Revises: 441a8e5c1e3d
Create Date: 2022-10-25 08:36:46.330746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e88e89e764b5'
down_revision = '441a8e5c1e3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.BigInteger, nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    
