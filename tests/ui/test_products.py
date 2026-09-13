import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Automation Exercise UI")
@allure.feature("Товары")
@pytest.mark.ui
class TestProducts:
    """Тесты страницы товаров."""

    @allure.story("Поиск")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Поиск существующего товара возвращает результаты")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_search_existing_product(self, driver, base_url):
        """5. Поиск существующего товара."""
        home = HomePage(driver, base_url).open()
        products = home.go_to_products()
        products.search_product("Dress")

        assert products.is_search_results_visible(), "Заголовок результатов не показан"
        count = products.get_result_count()
        allure.attach(str(count), name="Количество результатов", attachment_type=allure.attachment_type.TEXT)
        assert count > 0, "Поиск 'Dress' не дал результатов"

    @allure.story("Поиск")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск несуществующего товара возвращает пустой список")
    @pytest.mark.regression
    @pytest.mark.negative
    def test_search_nonexistent_product(self, driver, base_url):
        """6. Поиск несуществующего товара."""
        home = HomePage(driver, base_url).open()
        products = home.go_to_products()
        products.search_product("XYZNONEXISTENT123")

        count = products.get_result_count()
        allure.attach(str(count), name="Количество результатов", attachment_type=allure.attachment_type.TEXT)
        assert count == 0, "Поиск несуществующего товара должен давать 0 результатов"
