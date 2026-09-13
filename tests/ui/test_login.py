import allure
import pytest

from pages.home_page import HomePage


@allure.epic("Automation Exercise UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLogin:
    """Тесты авторизации."""

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Вход с неверными данными показывает ошибку")
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_login_invalid_credentials(self, driver, base_url):
        """3. Неверные данные для входа → ошибка."""
        home = HomePage(driver, base_url).open()
        login_page = home.go_to_login()
        login_page.login("invalid@example.com", "wrongpassword")

        assert login_page.is_login_error_visible(), "При неверных данных не показана ошибка"

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Регистрация с уже существующим email показывает ошибку")
    @pytest.mark.regression
    @pytest.mark.negative
    def test_signup_existing_email(self, driver, base_url):
        """4. Существующий email → ошибка регистрации."""
        home = HomePage(driver, base_url).open()
        login_page = home.go_to_login()
        # admin@example.com уже зарегистрирован на automationexercise.com
        login_page.signup("Test User", "admin@example.com")

        assert login_page.is_signup_error_visible(), "При регистрации с существующим email не показана ошибка"
