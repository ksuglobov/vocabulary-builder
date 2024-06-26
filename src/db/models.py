"""
Database models.
"""

import uuid
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import BaseModel


class WordModel(BaseModel):
    """
    Represents a word with its translations and usage contexts.

    :param id: Primary key.
    :param word: The word in the original language.
    :param translated_word: The translated word.
    :param context: The context in which the word is used in the original language.
    :param translated_context: The translated context.
    """
    __tablename__ = 'words'
    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    word: Mapped[str] = mapped_column(nullable=False)
    translated_word: Mapped[str] = mapped_column(nullable=False)
    context: Mapped[str] = mapped_column(nullable=False)
    translated_context: Mapped[str] = mapped_column(nullable=False)
