import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page

from auth_helper import AUTH_STATE_PATH
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


@pytest.fixture(scope="session")
def auth_state_path() -> str:
    """Путь к файлу с сохранённым состоянием авторизации (auth_state.json)."""
    if not os.path.exists(AUTH_STATE_PATH):
        raise RuntimeError(
            f"Файл {AUTH_STATE_PATH} не найден. "
            "Сначала выполните генерацию состояния: python auth_helper.py"
        )
    return AUTH_STATE_PATH


@pytest.fixture
def auth_page(page: Page):
    """Фикстура, создающая объект страницы авторизации и открывающая BASE_URL."""
    auth = AuthPage(page)
    auth.navigate()
    yield auth


@pytest.fixture
def authenticated_page(browser: Browser, auth_state_path: str) -> Page:
    """Фикстура, возвращающая уже авторизованную страницу на основе auth_state.json."""
    context = browser.new_context(storage_state=auth_state_path)
    page = context.new_page()
    yield page
    context.close()

