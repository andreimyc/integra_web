import pytest
from playwright.sync_api import Page

from pages.auth_page import AuthPage


class TestAuthPage:
    """Тесты для страницы авторизации"""

    @pytest.mark.auth
    def test_successful_login(
        self,
        page: Page,
        auth_page: AuthPage,
        username: str,
        password: str,
    ) -> None:
        """Тест проверяет, что после успешной авторизации открывается страница /ru/invoices."""
        auth_page.enter_username(username)
        auth_page.enter_code(password)

        assert auth_page.is_invoices_page_open(), (
            f"Ожидали переход на /ru/invoices, получили: {page.url}"
        )