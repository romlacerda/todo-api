"""Make phone number required

Revision ID: 7864d446a4db
Revises: 53408a15d99d
Create Date: 2025-06-24 19:17:47.212369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7864d446a4db'
down_revision: Union[str, Sequence[str], None] = '53408a15d99d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE users SET phone_number = '000' WHERE phone_number IS NULL")
    op.alter_column("users", "phone_number", nullable=False)


def downgrade() -> None:
    op.alter_column("users", "phone_number", nullable=True)
