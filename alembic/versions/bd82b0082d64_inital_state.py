"""inital state

Revision ID: bd82b0082d64
Revises: 
Create Date: 2023-03-03 23:56:48.611685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd82b0082d64"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("active", sa.Boolean, server_default=sa.sql.true(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("products", "active")
