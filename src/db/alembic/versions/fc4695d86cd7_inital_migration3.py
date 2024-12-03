"""Inital Migration3

Revision ID: fc4695d86cd7
Revises: 
Create Date: 2023-09-07 18:44:45.206961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fc4695d86cd7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Roles",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "Teams",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("name"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "Users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("team_name", sa.String(), nullable=True),
        sa.Column("role_name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_name"],
            ["Roles.name"],
        ),
        sa.ForeignKeyConstraint(
            ["team_name"],
            ["Teams.name"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "HolidayRequests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("time_of_day", sa.String(length=2), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("team_name", sa.String(), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["team_name"],
            ["Teams.name"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["Users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Insert some data (only for testing to be deleted at a later date)
    op.bulk_insert(
        sa.table("Roles", sa.column("name"), sa.column("description")),
        [
            {"name": "SuperAdmin", "description": "This is a SuperAdmin user"},
            {"name": "Admin", "description": "This is an Admin user"},
            {"name": "User", "description": "This is a Standard user"},
        ],
    )

    op.bulk_insert(
        sa.table("Teams", sa.column("name"), sa.column("description")),
        [
            {"name": "Super", "description": "This is a team for SuperAdmins"},
            {"name": "Team GG", "description": "This is Team GG"},
            {"name": "Team Matrix", "description": "This is Team Matrix"},
            {"name": "Team Mamba", "description": "This is Team Mamba"},
        ],
    )

    op.bulk_insert(
        sa.table(
            "Users",
            sa.column("full_name"),
            sa.column("email"),
            sa.column("password"),
            sa.column("team_name"),
            sa.column("role_name"),
        ),
        [
            {
                "full_name": "SuperAdmin",
                "email": "super@super.com",
                "password": "$2b$12$un/7ge7YyOA2uAOb98r1Qu5qc9JQmI73KOp5jy8/KcC.muX2ib4ua",
                "team_name": "Super",
                "role_name": "SuperAdmin",
            },
            {
                "full_name": "Admin",
                "email": "admin@gg.com",
                "password": "$2b$12$h.EfOTwMQwpp94BprPvor.2Oq4il8HjXpQR6q9oJ0cBf3YclXYabS",
                "team_name": "Team Matrix",
                "role_name": "Admin",
            },
            {
                "full_name": "User",
                "email": "normal@gg.com",
                "password": "$2b$12$szeazF4438sHcUVApqZH1OsdHm7.MbUL2x7wQvVSu3vuSA/t7cTPS",
                "team_name": "Team Matrix",
                "role_name": "User",
            },
        ],
    )

    op.bulk_insert(
        sa.table(
            "HolidayRequests",
            sa.column("description"),
            sa.column("start_date"),
            sa.column("end_date"),
            sa.column("time_of_day"),
            sa.column("user_id"),
            sa.column("team_name"),
            sa.column("approved"),
        ),
        [
            {
                "description": "SuperAdmin Request",
                "start_date": "2021-09-01",
                "end_date": "2021-09-01",
                "time_of_day": "AM",
                "user_id": 1,
                "team_name": "Super",
                "approved": True,
            },
            {
                "description": "Admin Request",
                "start_date": "2021-09-01",
                "end_date": "2021-09-01",
                "time_of_day": "AM",
                "user_id": 2,
                "team_name": "Team Matrix",
                "approved": True,
            },
            {
                "description": "User Request",
                "start_date": "2021-09-01",
                "end_date": "2021-09-01",
                "time_of_day": "AM",
                "user_id": 3,
                "team_name": "Team Matrix",
                "approved": False,
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("HolidayRequests")
    op.drop_table("Users")
    op.drop_table("Teams")
    op.drop_table("Roles")
    # ### end Alembic commands ###
