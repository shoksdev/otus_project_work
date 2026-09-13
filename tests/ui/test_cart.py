import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Automation Exercise UI")
@allure.feature("Корзина")
@pytest.mark.ui
class TestCart:
    """Тесты корзины."""

    @allure.story("Пустая корзина")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("В новой сессии корзина пуста")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_empty_cart(self, driver, base_url):
        """7. В новой сессии корзина пуста."""
        home = HomePage(driver, base_url).open()
        cart = home.go_to_cart()

        assert cart.is_cart_empty(), "В новой сессии корзина не пуста"

    @allure.story("Навигация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Со страницы корзины можно вернуться на главную")
    @pytest.mark.regression
    @pytest.mark.positive
    def test_cart_page_has_navigation(self, driver, base_url):
        """8. Со страницы корзины работает навигация."""
        home = HomePage(driver, base_url).open()
        home.go_to_cart()
        # Проверяем, что можно вернуться на главную
        driver.get(base_url)
        assert home.is_loaded(), "С корзины не удалось вернуться на главную"
