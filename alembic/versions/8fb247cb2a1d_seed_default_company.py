"""seed default company

Revision ID: 8fb247cb2a1d
Revises: de6c650e4343
Create Date: 2026-06-25 15:16:04.219725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fb247cb2a1d'
down_revision: Union[str, Sequence[str], None] = 'de6c650e4343'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO companies (
            company_id,
            company_name,
            email,
            phone,
            address,
            is_active
        )
        VALUES (
            'COMP_00001',
            'ABC Technologies',
            'admin@abctech.com',
            '9876543210',
            'Mohali, Punjab',
            true
        )
        ON CONFLICT (company_id) DO NOTHING;
    """)


def downgrade():
    op.execute("""
        DELETE FROM companies
        WHERE company_id = 'COMP_00001';
    """)
