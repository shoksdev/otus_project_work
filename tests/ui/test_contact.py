import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Automation Exercise UI")
@allure.feature("Contact Us")
@pytest.mark.ui
class TestContact:
    """Тесты страницы обратной связи."""

    @allure.story("Загрузка страницы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Страница Contact Us корректно загружается")
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_contact_page_loads(self, driver, base_url):
        """9. Страница Contact Us загружается и показывает GET IN TOUCH."""
        home = HomePage(driver, base_url).open()
        contact = home.go_to_contact()

        assert contact.is_loaded(), "Страница Contact Us не показывает 'GET IN TOUCH'"

    @allure.story("Отправка формы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешная отправка формы обратной связи")
    @pytest.mark.regression
    @pytest.mark.positive
    def test_submit_contact_form(self, driver, base_url, faker_instance):
        """10. Заполнение и отправка формы обратной связи."""
        home = HomePage(driver, base_url).open()
        contact = home.go_to_contact()

        contact.fill_form(
            name=faker_instance.name(),
            email=faker_instance.email(),
            subject="Test Subject",
            message="Это тестовое сообщение из автоматизированного UI-теста.",
        )
        contact.submit()

        assert contact.is_success_message_visible(), "После отправки формы не показано сообщение об успехе"
