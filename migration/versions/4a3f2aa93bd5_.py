"""empty message

Revision ID: 4a3f2aa93bd5
Revises: 
Create Date: 2017-05-10 00:55:41.369040

"""

# revision identifiers, used by Alembic.
revision = '4a3f2aa93bd5'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('idx_icd_fts', 'icd', [
        sa.text("to_tsvector('english', 'code || '' '' || coalesce(description, '')')")
    ], postgresql_using='gin')


def downgrade():
    op.drop_index('idx_icd_fts', 'icd')
