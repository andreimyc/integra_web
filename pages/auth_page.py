import os

from playwright.sync_api import Locator, Page


class AuthPage:
    """Page Object для страницы авторизации CUPRA.IO."""

    def __init__(self, page: Page) -> None:
        """Инициализация класса AuthPage."""
        self.page = page
        self.base_url = os.getenv("BASE_URL")
        self._init_locators()

    def _init_locators(self) -> None:
        """Инициализация локаторов элементов страницы авторизации/входа."""
        self.username_input: Locator = self.page.get_by_role("textbox").first
        self.login_button: Locator = self.page.get_by_role(
            "button", name="Войти", exact=True
        )
        self.otp_inputs: Locator = self.page.get_by_role("textbox")

    def navigate(self) -> "AuthPage":
        """Переход на стартовую страницу авторизации."""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
        return self

    def enter_username(self, username: str) -> "AuthPage":
        """Ввод логина и переход к форме ввода кода."""
        self.username_input.wait_for(state="visible")
        self.username_input.fill(username)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def enter_code(self, code: str) -> "AuthPage":
        """Ввод 6-значного одноразового кода (по одному символу в каждое поле)."""
        assert len(code) == 6, "Код должен состоять из 6 символов"

        self.page.wait_for_timeout(300)

        for index, char in enumerate(code):
            field = self.otp_inputs.nth(index)
            field.wait_for(state="visible")
            field.fill(char)

        self.page.wait_for_timeout(5000)
        return self

    def is_invoices_page_open(self) -> bool:
        """Проверяет, открыт ли раздел инвойсов."""
        return self.page.url.endswith("/ru/invoices")

