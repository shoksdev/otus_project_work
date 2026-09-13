import allure
import requests

from conftest import API_AUTH_CREDENTIALS, API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - DeleteBooking")
class TestDeleteBooking:
    """Тесты для удаления бронирования."""

    @allure.story("Удаление (DELETE)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление брони с Cookie-токеном")
    def test_delete_booking_with_cookie_token(self, auth_token):
        """Удаление бронирования с Cookie-токеном."""
        payload = {
            "firstname": "ToDelete",
            "lastname": "Me",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-05-01", "checkout": "2024-05-05"},
            "additionalneeds": "None",
        }

        with allure.step("Setup: создание брони для удаления"):
            create_resp = requests.post(f"{API_BASE_URL}/booking", json=payload)
            booking_id = create_resp.json()["bookingid"]
            allure.attach(
                str(booking_id),
                name="Booking ID to delete",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(f"DELETE /booking/{booking_id} с Cookie-токеном"):
            response = requests.delete(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"token={auth_token}",
                },
            )
            attach_response(response)

        with allure.step("Проверка 201 Created"):
            assert response.status_code == 201

        with allure.step("Проверка, что бронь действительно удалена"):
            get_resp = requests.get(f"{API_BASE_URL}/booking/{booking_id}")
            assert get_resp.status_code == 404

    @allure.story("Удаление (DELETE)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление брони с Basic Auth")
    def test_delete_booking_with_basic_auth(self, basic_auth_headers):
        """Удаление бронирования с Basic Auth."""
        payload = {
            "firstname": "ToDeleteBasic",
            "lastname": "Me",
            "totalprice": 150,
            "depositpaid": False,
            "bookingdates": {"checkin": "2024-06-01", "checkout": "2024-06-05"},
            "additionalneeds": "None",
        }

        with allure.step("Setup: создание брони для удаления"):
            create_resp = requests.post(f"{API_BASE_URL}/booking", json=payload)
            booking_id = create_resp.json()["bookingid"]
            allure.attach(
                str(booking_id),
                name="Booking ID to delete",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step(f"DELETE /booking/{booking_id} с Basic Auth"):
            response = requests.delete(f"{API_BASE_URL}/booking/{booking_id}", headers=basic_auth_headers)
            attach_response(response)

        with allure.step("Проверка 201 Created"):
            assert response.status_code == 201

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("DELETE без авторизации запрещён")
    def test_delete_booking_without_auth(self):
        """Удаление без авторизации — должно быть запрещено."""
        payload = {
            "firstname": "NoDelete",
            "lastname": "Me",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-07-01", "checkout": "2024-07-05"},
            "additionalneeds": "None",
        }

        with allure.step("Setup: создание брони"):
            create_resp = requests.post(f"{API_BASE_URL}/booking", json=payload)
            booking_id = create_resp.json()["bookingid"]

        with allure.step("DELETE /booking без авторизации"):
            response = requests.delete(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={"Content-Type": "application/json"},
            )
            attach_response(response)

        with allure.step("Проверка 403 Forbidden"):
            assert response.status_code == 403

        with allure.step("Cleanup: удаление с токеном"):
            token = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS).json()["token"]
            requests.delete(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={"Cookie": f"token={token}"},
            )
