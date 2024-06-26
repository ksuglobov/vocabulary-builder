"""Initial migration

Revision ID: bbe34c804410
Revises:
Create Date: 2024-06-25 15:14:10.974406

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "bbe34c804410"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "words",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("word", sa.String(), nullable=False),
        sa.Column("part_of_speech", sa.String(), nullable=False),
        sa.Column("transcription", sa.String(), nullable=False),
        sa.Column("audio", sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "semantics",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("word_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["word_id"],
            ["words.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "examples",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("semantic_id", sa.Uuid(), nullable=False),
        sa.Column("example", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["semantic_id"],
            ["semantics.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("semantic_id", sa.Uuid(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("word", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["semantic_id"],
            ["semantics.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "examples_translations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("translation_id", sa.Uuid(), nullable=False),
        sa.Column("example", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["translation_id"],
            ["translations.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("examples_translations")
    op.drop_table("translations")
    op.drop_table("examples")
    op.drop_table("semantics")
    op.drop_table("words")
    op.drop_table("users")
    # ### end Alembic commands ###
