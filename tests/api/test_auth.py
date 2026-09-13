import allure
import requests

from conftest import API_AUTH_CREDENTIALS, API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Auth")
class TestAuth:
    """Тесты для эндпоинта /auth."""

    @allure.story("Создание токена")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешное создание токена с валидными данными")
    @allure.description("Проверяет, что POST /auth с валидными учётными данными возвращает непустой токен.")
    def test_create_token_success(self):
        """Успешное создание токена с валидными данными."""
        with allure.step("Отправка POST /auth"):
            response = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS)
            attach_response(response)

        with allure.step("Проверка статуса и тела ответа"):
            assert response.status_code == 200
            data = response.json()
            assert "token" in data
            assert isinstance(data["token"], str)
            assert len(data["token"]) > 0

    @allure.story("Создание токена")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание токена с неверными учётными данными")
    def test_create_token_invalid_credentials(self):
        """Создание токена с неверными учётными данными."""
        with allure.step("Отправка POST /auth с неверными данными"):
            response = requests.post(f"{API_BASE_URL}/auth", json={"username": "wrong", "password": "wrong"})
            attach_response(response)

        with allure.step("Проверка отсутствия токена в ответе"):
            assert response.status_code == 200
            data = response.json()
            assert "token" not in data or data.get("reason") == "Bad credentials"

    @allure.story("Валидация входных данных")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание токена с пустым телом запроса")
    def test_create_token_empty_body(self):
        """Создание токена с пустым телом запроса."""
        with allure.step("Отправка POST /auth с пустым JSON"):
            response = requests.post(
                f"{API_BASE_URL}/auth",
                json={},
                headers={"Content-Type": "application/json"},
            )
            attach_response(response)

        with allure.step("Проверка отсутствия токена"):
            assert response.status_code == 200
            assert "token" not in response.json()

    @allure.story("Валидация входных данных")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание токена без пароля")
    def test_create_token_missing_password(self):
        """Создание токена без пароля."""
        with allure.step("Отправка POST /auth без password"):
            response = requests.post(f"{API_BASE_URL}/auth", json={"username": "admin"})
            attach_response(response)

        assert response.status_code == 200
        assert "token" not in response.json()

    @allure.story("Валидация входных данных")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание токена без имени пользователя")
    def test_create_token_missing_username(self):
        """Создание токена без имени пользователя."""
        with allure.step("Отправка POST /auth без username"):
            response = requests.post(f"{API_BASE_URL}/auth", json={"password": "password123"})
            attach_response(response)

        assert response.status_code == 200
        assert "token" not in response.json()
