import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from pages.auth_page import AuthPage


AUTH_STATE_PATH = "auth_state.json"


def generate_auth_state() -> None:
    """Проходит полный флоу авторизации и сохраняет storage_state в auth_state.json."""
    load_dotenv(override=True)

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not username:
        raise RuntimeError("USERNAME не задан в .env")
    if not password:
        raise RuntimeError("PASSWORD не задан в .env")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        auth_page = AuthPage(page)
        auth_page.navigate()
        auth_page.enter_username(username)
        auth_page.enter_code(password)

        if not auth_page.is_invoices_page_open():
            raise AssertionError(
                f"После авторизации не открылась ожидаемая страница /ru/invoices, текущий URL: {page.url}"
            )

        context.storage_state(path=AUTH_STATE_PATH)

        context.close()
        browser.close()


if __name__ == "__main__":
    generate_auth_state()

