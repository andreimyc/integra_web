import pytest
from playwright.sync_api import Page

from pages.auth_page import AuthPage


class TestAuthPage:
    """Тесты для страницы авторизации.

    Здесь остаётся один эталонный тест полного флоу логина, остальные
    сценарные тесты должны использовать уже авторизованную страницу
    через фикстуру `authenticated_page`.
    """

    @pytest.mark.auth
    @pytest.mark.auth_flow
    def test_successful_login(
        self,
        page: Page,
        auth_page: AuthPage,
        username: str,
        password: str,
    ) -> None:
        """Проверяет, что после успешной авторизации открывается страница /ru/invoices."""
        auth_page.enter_username(username)
        auth_page.enter_code(password)

        assert auth_page.is_invoices_page_open(), (
            f"Ожидали переход на /ru/invoices, получили: {page.url}"
        )