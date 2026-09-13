import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Automation Exercise UI")
@allure.feature("Главная страница")
@pytest.mark.ui
class TestHomePage:
    """Тесты главной страницы."""

    @allure.story("Загрузка главной")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Главная страница корректно загружается")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_home_page_loads(self, driver, base_url):
        """1. Проверка успешной загрузки главной страницы."""
        home = HomePage(driver, base_url).open()
        assert home.is_loaded(), "Главная страница не загрузилась"

    @allure.story("Контент главной")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("На главной отображаются featured-товары")
    @pytest.mark.regression
    @pytest.mark.positive
    def test_featured_products_visible(self, driver, base_url):
        """2. Проверка наличия товаров на главной."""
        home = HomePage(driver, base_url).open()
        count = home.get_featured_count()
        allure.attach(str(count), name="Количество товаров", attachment_type=allure.attachment_type.TEXT)
        assert count > 0, "На главной нет ни одного товара"
