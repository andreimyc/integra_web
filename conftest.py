import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.auth_page import AuthPage


load_dotenv(override=True)


@pytest.fixture(scope="session")
def username() -> str:
    """Логин для авторизации, берётся из .env (USERNAME)."""
    value = os.getenv("USERNAME")
    if not value:
        raise RuntimeError("USERNAME не задан в .env")
    return value


@pytest.fixture(scope="session")
def password() -> str:
    """Одноразовый код для авторизации, берётся из .env (PASSWORD)."""
    value = os.getenv("PASSWORD")
    if not value:
        raise RuntimeError("PASSWORD не задан в .env")
    return value

@pytest.fixture
def auth_page(page: Page):
    """Фикстура, создающая объект страницы авторизации и открывающая BASE_URL."""
    auth = AuthPage(page)
    auth.navigate()
    yield auth

