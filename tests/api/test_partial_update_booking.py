import allure
import requests

from conftest import API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - PartialUpdateBooking")
class TestPartialUpdateBooking:
    """Тесты для частичного обновления (PATCH)."""

    @allure.story("Частичное обновление (PATCH)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Частичное обновление только firstname")
    def test_partial_update_firstname(self, created_booking, auth_headers):
        """Частичное обновление — только firstname."""
        booking_id, original = created_booking

        with allure.step(f"PATCH /booking/{booking_id} с firstname=PatchedName"):
            response = requests.patch(
                f"{API_BASE_URL}/booking/{booking_id}",
                json={"firstname": "PatchedName"},
                headers=auth_headers,
            )
            attach_response(response)

        with allure.step("Проверка: firstname изменён, остальное сохранено"):
            assert response.status_code == 200
            data = response.json()
            assert data["firstname"] == "PatchedName"
            assert data["lastname"] == original["lastname"]
            assert data["totalprice"] == original["totalprice"]

    @allure.story("Частичное обновление (PATCH)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Частичное обновление нескольких полей")
    def test_partial_update_multiple_fields(self, created_booking, auth_headers):
        """Частичное обновление нескольких полей."""
        booking_id, _ = created_booking

        with allure.step(f"PATCH /booking/{booking_id} с двумя полями"):
            response = requests.patch(
                f"{API_BASE_URL}/booking/{booking_id}",
                json={"totalprice": 999, "additionalneeds": "Spa"},
                headers=auth_headers,
            )
            attach_response(response)

        with allure.step("Проверка обновлённых полей"):
            assert response.status_code == 200
            data = response.json()
            assert data["totalprice"] == 999
            assert data["additionalneeds"] == "Spa"

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("PATCH без авторизации запрещён")
    def test_partial_update_without_auth(self, created_booking):
        """PATCH без авторизации — должно быть запрещено."""
        booking_id, _ = created_booking

        with allure.step("PATCH /booking без заголовков авторизации"):
            response = requests.patch(
                f"{API_BASE_URL}/booking/{booking_id}",
                json={"firstname": "NoAuth"},
                headers={"Content-Type": "application/json"},
            )
            attach_response(response)

        with allure.step("Проверка 403 Forbidden"):
            assert response.status_code == 403
