"""seed roles

Revision ID: 7e9b90a020bb
Revises: d1b72804ce0b
Create Date: 2026-05-07 16:53:09.125562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e9b90a020bb'
down_revision: Union[str, Sequence[str], None] = 'd1b72804ce0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO roles (name)
        VALUES ('admin'), ('user'), ('moderator')
        ON CONFLICT (name) DO NOTHING;
    """)

def downgrade():
    op.execute("""
        DELETE FROM roles WHERE name IN ('admin', 'user', 'moderator');
    """)
