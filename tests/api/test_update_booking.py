import allure
import requests

from conftest import API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - UpdateBooking")
class TestUpdateBooking:
    """Тесты для полного обновления бронирования (PUT)."""

    @allure.story("Обновление (PUT)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Обновление брони с Cookie-токеном")
    def test_update_booking_with_cookie_token(self, created_booking, auth_headers):
        """Обновление бронирования с Cookie-токеном."""
        booking_id, _ = created_booking
        update_data = {
            "firstname": "James",
            "lastname": "Smith",
            "totalprice": 250,
            "depositpaid": False,
            "bookingdates": {"checkin": "2024-02-01", "checkout": "2024-02-15"},
            "additionalneeds": "Dinner",
        }

        with allure.step(f"PUT /booking/{booking_id} с Cookie-токеном"):
            response = requests.put(
                f"{API_BASE_URL}/booking/{booking_id}",
                json=update_data,
                headers=auth_headers,
            )
            attach_response(response)

        with allure.step("Проверка обновлённых полей"):
            assert response.status_code == 200
            data = response.json()
            assert data["firstname"] == "James"
            assert data["lastname"] == "Smith"
            assert data["totalprice"] == 250

    @allure.story("Обновление (PUT)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Обновление брони с Basic Auth")
    def test_update_booking_with_basic_auth(self, created_booking, basic_auth_headers):
        """Обновление бронирования с Basic Auth."""
        booking_id, _ = created_booking
        update_data = {
            "firstname": "Robert",
            "lastname": "Johnson",
            "totalprice": 300,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-03-01", "checkout": "2024-03-10"},
            "additionalneeds": "Late checkout",
        }

        with allure.step(f"PUT /booking/{booking_id} с Basic Auth"):
            response = requests.put(
                f"{API_BASE_URL}/booking/{booking_id}",
                json=update_data,
                headers=basic_auth_headers,
            )
            attach_response(response)

        with allure.step("Проверка обновлённых полей"):
            assert response.status_code == 200
            assert response.json()["firstname"] == "Robert"

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Обновление брони без авторизации запрещено")
    def test_update_booking_without_auth(self, created_booking):
        """Обновление бронирования без авторизации — должно быть запрещено."""
        booking_id, _ = created_booking
        update_data = {
            "firstname": "Hacker",
            "lastname": "Hacker",
            "totalprice": 0,
            "depositpaid": False,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
            "additionalneeds": "",
        }

        with allure.step("PUT /booking без заголовков авторизации"):
            response = requests.put(
                f"{API_BASE_URL}/booking/{booking_id}",
                json=update_data,
                headers={"Content-Type": "application/json"},
            )
            attach_response(response)

        with allure.step("Проверка 403 Forbidden"):
            assert response.status_code == 403
