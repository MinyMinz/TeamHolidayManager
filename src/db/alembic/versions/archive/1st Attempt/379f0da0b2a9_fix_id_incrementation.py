"""fix id incrementation

Revision ID: 379f0da0b2a9
Revises: b7aa32a8e562
Create Date: 2023-08-07 21:43:31.788852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '379f0da0b2a9'
down_revision = 'b7aa32a8e562'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_HolidayRequests_id', table_name='HolidayRequests')
    op.drop_index('ix_Roles_id', table_name='Roles')
    op.drop_index('ix_Teams_id', table_name='Teams')
    op.drop_index('ix_Users_id', table_name='Users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_Users_id', 'Users', ['id'], unique=False)
    op.create_index('ix_Teams_id', 'Teams', ['id'], unique=False)
    op.create_index('ix_Roles_id', 'Roles', ['id'], unique=False)
    op.create_index('ix_HolidayRequests_id', 'HolidayRequests', ['id'], unique=False)
    # ### end Alembic commands ###
