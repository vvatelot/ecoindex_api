"""First migration

Revision ID: fd9a1f5662c8
Revises: 
Create Date: 2022-09-12 15:03:22.363502

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "fd9a1f5662c8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "apiecoindex",
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column("nodes", sa.Integer(), nullable=False),
        sa.Column("requests", sa.Integer(), nullable=False),
        sa.Column("grade", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("ges", sa.Float(), nullable=True),
        sa.Column("water", sa.Float(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.Column("page_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("host", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("initial_ranking", sa.Integer(), nullable=False),
        sa.Column("initial_total_results", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("apiecoindex")
    # ### end Alembic commands ###
