from datetime import datetime

import allure
import requests

from conftest import API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Ping")
class TestPing:
    """Тесты для эндпоинта /ping."""

    @allure.story("Health check")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Проверка работоспособности API")
    @allure.description("GET /ping возвращает 201 Created, если API жив.")
    def test_ping_health_check(self):
        """Проверка работоспособности API."""
        with allure.step("Отправка GET /ping"):
            response = requests.get(f"{API_BASE_URL}/ping")
            attach_response(response)

        with allure.step("Проверка статуса 201"):
            assert response.status_code == 201

    @allure.story("Производительность")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Ping отвечает быстрее 5 секунд")
    def test_ping_response_time(self):
        """Проверка, что ping отвечает быстро (< 5 сек)."""
        with allure.step("Замер времени ответа GET /ping"):
            start = datetime.now()
            response = requests.get(f"{API_BASE_URL}/ping")
            elapsed = (datetime.now() - start).total_seconds()
            attach_response(response)

        allure.attach(
            f"{elapsed:.3f} сек",
            name="Response Time",
            attachment_type=allure.attachment_type.TEXT,
        )

        with allure.step("Проверка статуса и времени"):
            assert response.status_code == 201
            assert elapsed < 5
