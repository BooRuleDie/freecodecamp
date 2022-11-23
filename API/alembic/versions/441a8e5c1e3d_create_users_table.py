"""create users table

Revision ID: 441a8e5c1e3d
Revises: bc9f95bee344
Create Date: 2022-10-25 08:33:11.543488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '441a8e5c1e3d'
down_revision = 'bc9f95bee344'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", 
    sa.Column("id", sa.BigInteger, primary_key=True, nullable=False),
    sa.Column("email", sa.String, nullable=False, unique=True),
    sa.Column("password", sa.String, nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade() -> None:
    op.drop_table("users")