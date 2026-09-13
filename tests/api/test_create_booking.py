import allure
import requests

from conftest import API_AUTH_CREDENTIALS, API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - CreateBooking")
class TestCreateBooking:
    """Тесты для создания бронирования."""

    @allure.story("Создание брони")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Успешное создание бронирования")
    def test_create_booking_success(self, booking_payload):
        """Успешное создание бронирования."""
        with allure.step("POST /booking с валидным payload"):
            response = requests.post(f"{API_BASE_URL}/booking", json=booking_payload)
            attach_response(response)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            data = response.json()
            assert "bookingid" in data
            assert "booking" in data
            assert isinstance(data["bookingid"], int)

        with allure.step("Cleanup: удаление созданной брони"):
            token = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS).json()["token"]
            requests.delete(
                f"{API_BASE_URL}/booking/{data['bookingid']}",
                headers={"Cookie": f"token={token}"},
            )

    @allure.story("Создание брони")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание брони возвращает корректные данные")
    def test_create_booking_returns_correct_data(self, booking_payload):
        """Создание и проверка возвращённых данных."""
        with allure.step("POST /booking"):
            response = requests.post(f"{API_BASE_URL}/booking", json=booking_payload)
            attach_response(response)

        with allure.step("Проверка полей созданной брони"):
            assert response.status_code == 200
            booking = response.json()["booking"]
            assert booking["firstname"] == booking_payload["firstname"]
            assert booking["lastname"] == booking_payload["lastname"]
            assert booking["totalprice"] == booking_payload["totalprice"]
            assert booking["depositpaid"] == booking_payload["depositpaid"]
            assert booking["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]

        with allure.step("Cleanup: удаление созданной брони"):
            token = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS).json()["token"]
            requests.delete(
                f"{API_BASE_URL}/booking/{response.json()['bookingid']}",
                headers={"Cookie": f"token={token}"},
            )

    @allure.story("Создание брони")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание бронирования с additionalneeds")
    def test_create_booking_with_additional_needs(self, booking_payload):
        """Создание бронирования с additionalneeds."""
        booking_payload["additionalneeds"] = "Lunch"

        with allure.step("POST /booking с additionalneeds=Lunch"):
            response = requests.post(f"{API_BASE_URL}/booking", json=booking_payload)
            attach_response(response)

        with allure.step("Проверка поля additionalneeds"):
            assert response.status_code == 200
            assert response.json()["booking"]["additionalneeds"] == "Lunch"

        with allure.step("Cleanup"):
            token = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS).json()["token"]
            requests.delete(
                f"{API_BASE_URL}/booking/{response.json()['bookingid']}",
                headers={"Cookie": f"token={token}"},
            )

    @allure.story("Создание брони")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание брони с depositpaid=false")
    def test_create_booking_deposit_not_paid(self, booking_payload):
        """Создание бронирования с depositpaid=false."""
        booking_payload["depositpaid"] = False

        with allure.step("POST /booking с depositpaid=False"):
            response = requests.post(f"{API_BASE_URL}/booking", json=booking_payload)
            attach_response(response)

        with allure.step("Проверка поля depositpaid"):
            assert response.status_code == 200
            assert response.json()["booking"]["depositpaid"] is False

        with allure.step("Cleanup"):
            token = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS).json()["token"]
            requests.delete(
                f"{API_BASE_URL}/booking/{response.json()['bookingid']}",
                headers={"Cookie": f"token={token}"},
            )

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Создание брони с пустым телом запроса")
    def test_create_booking_empty_body(self):
        """Создание бронирования с пустым телом."""
        with allure.step("POST /booking с пустым JSON"):
            response = requests.post(f"{API_BASE_URL}/booking", json={})
            attach_response(response)

        with allure.step("Проверка допустимого кода ответа"):
            # API может вернуть 500 или 200 с пустыми полями
            assert response.status_code in [200, 400, 500]
