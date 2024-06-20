"""Main application file for Vocabulary Builder."""

import gettext
import os
from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from src.db.crud import get_random_word
from src.db.database import SessionLocal

app = FastAPI()

def get_db():
    """
    Provides a database session for dependency injection.

    :yields: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="src/templates")

def _(language: str):
    """
    Retrieves the gettext translation function for the specified language.

    :param language: Language code (e.g., 'ru', 'fr').
    :return: The translation function for the specified language.
    """
    try:
        translations = gettext.translation(
            domain="translations",
            localedir=os.path.join(os.path.dirname(__file__), "locales"),
            languages=[language]
        )
    except FileNotFoundError:
        translations = gettext.NullTranslations()
    return translations.gettext

def fetch_random_word_data(db: Session):
    """
    Fetches a random word and its translations from the database.

    :param db: Database session.
    :return: A dictionary with word data.
    """
    random_row = get_random_word(db)
    data = {
        'word': random_row.word,
        'translated_word': random_row.translated_word,
        'context': random_row.context,
        'translated_context': random_row.translated_context,
    }
    return data

@app.get('/', response_class=HTMLResponse)
def get_main_page(request: Request, db: Session = Depends(get_db)):
    """
    Serves the main page in the default language (Russian).

    :param request: HTTP request.
    :param db: Database session dependency.
    :return: HTML response with the main page content.
    """
    return handle_main_page(request, db)

@app.get('/{language}', response_class=HTMLResponse)
def get_main_page_in_language(request: Request, language: str, db: Session = Depends(get_db)):
    """
    Serves the main page in the specified language.

    :param request: HTTP request.
    :param language: Language code (e.g., 'ru', 'fr').
    :param db: Database session dependency.
    :return: HTML response with the main page content in the specified language.
    """
    return handle_main_page(request, db, language)

def handle_main_page(request: Request, db: Session, language: str = 'ru'):
    """
    Handles the main page rendering with the specified language.

    :param request: HTTP request.
    :param db: Database session.
    :param language: Language code (default is 'ru').
    :return: HTML response with the main page content.
    """
    context = fetch_random_word_data(db)
    context.update({'_': _(language)})
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context=context,
    )

@app.get('/new_word', response_class=JSONResponse)
def get_new_word(db: Session = Depends(get_db)):
    """
    Fetches a new random word and returns it as a JSON response.

    :param db: Database session dependency.
    :return: JSON response with the new word data.
    """
    data = fetch_random_word_data(db)
    return data
