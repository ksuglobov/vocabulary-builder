"""Update WordModel with UUID default

Revision ID: 134106b1ca86
Revises: 6c66a9f9d49b
Create Date: 2024-06-01 11:14:36.594095

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "134106b1ca86"
down_revision: Union[str, None] = "6c66a9f9d49b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("words") as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.Uuid(),
            nullable=False,
            server_default=sa.text("(uuid_generate_v4())"),
        )
        # Добавьте здесь другие операции ALTER COLUMN, если они есть
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("words") as batch_op:
        batch_op.alter_column(
            "id", existing_type=sa.Uuid(), nullable=False, server_default=None
        )
        # Добавьте здесь другие операции ALTER COLUMN, если они есть
    # ### end Alembic commands ###
