import os
from typing import Final, Optional

from playwright.sync_api import Page


class BasePage:
    """Базовый класс для всех Page Object-ов.

    Содержит общую логику работы со страницами:
    - хранение ссылки на `Page`;
    - базовый URL тестируемого приложения;
    - типовой метод навигации и ожидания загрузки.
    """

    LOAD_STATE: Final[str] = "networkidle"

    def __init__(self, page: Page, base_url: Optional[str] = None) -> None:
        self.page: Page = page
        # Позволяем переопределять base_url при необходимости (например, в тестах)
        self.base_url: str = base_url or os.getenv("BASE_URL", "")
        if not self.base_url:
            raise RuntimeError("BASE_URL не задан в окружении (.env)")

    def navigate(self, relative_path: str = "") -> "BasePage":
        """Переход на базовый URL или URL с относительным путём.

        Примеры:
        - navigate() -> BASE_URL
        - navigate("/ru/invoices") -> BASE_URL + "/ru/invoices"
        """
        url = self.base_url.rstrip("/")
        if relative_path:
            # допускаем как "/path", так и "path"
            url = f"{url}/{relative_path.lstrip('/')}"

        self.page.goto(url)
        self.page.wait_for_load_state(self.LOAD_STATE)
        return self

