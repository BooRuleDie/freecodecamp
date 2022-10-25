"""create posts table

Revision ID: bc9f95bee344
Revises: 
Create Date: 2022-10-25 08:32:05.132957

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc9f95bee344'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
    sa.Column("id", sa.BigInteger, nullable=False, primary_key=True),
    sa.Column("title", sa.String, nullable=False),
    sa.Column("content", sa.String, nullable=False),
    sa.Column("published", sa.Boolean, nullable=False, server_default="true"),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    # pass

def downgrade() -> None:
    op.drop_table("posts")
    # pass


