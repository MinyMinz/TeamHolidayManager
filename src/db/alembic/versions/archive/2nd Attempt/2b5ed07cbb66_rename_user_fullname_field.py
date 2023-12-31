"""rename user fullname field

Revision ID: 2b5ed07cbb66
Revises: 52df60043934
Create Date: 2023-08-30 23:51:01.118883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b5ed07cbb66'
down_revision = '52df60043934'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('full_name', sa.String(), nullable=True))
    op.drop_column('Users', 'Fullname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('Fullname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('Users', 'full_name')
    # ### end Alembic commands ###
