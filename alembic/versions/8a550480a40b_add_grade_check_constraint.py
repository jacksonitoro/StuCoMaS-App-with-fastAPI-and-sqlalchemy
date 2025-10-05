"""Add grade check constraint

Revision ID: 8a550480a40b
Revises: c9198d4fe27f
Create Date: 2025-10-02 21:39:11.490636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a550480a40b'
down_revision: Union[str, Sequence[str], None] = 'c9198d4fe27f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "check_grade_range",  # name of the constraint
        "enrollments",  # table name
        "grade >= 1 AND grade <= 5"
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "check_grade_range",
        "enrollments",
        type_="check"
    )
