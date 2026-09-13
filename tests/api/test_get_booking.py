import allure
import requests

from conftest import API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - GetBooking")
class TestGetBooking:
    """Тесты для получения конкретного бронирования."""

    @allure.story("Получение по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение бронирования по ID в формате JSON")
    def test_get_booking_by_id_json(self, created_booking):
        """Получение бронирования по ID в формате JSON."""
        booking_id, booking_data = created_booking

        with allure.step(f"GET /booking/{booking_id} с Accept: application/json"):
            response = requests.get(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={"Accept": "application/json"},
            )
            attach_response(response)

        with allure.step("Проверка полей ответа"):
            assert response.status_code == 200
            data = response.json()
            assert data["firstname"] == booking_data["firstname"]
            assert data["lastname"] == booking_data["lastname"]
            assert data["totalprice"] == booking_data["totalprice"]

    @allure.story("Получение по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение бронирования по ID в формате XML")
    def test_get_booking_by_id_xml(self, created_booking):
        """Получение бронирования по ID в формате XML."""
        booking_id, _ = created_booking

        with allure.step(f"GET /booking/{booking_id} с Accept: application/xml"):
            response = requests.get(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={"Accept": "application/xml"},
            )
            attach_response(response)

        with allure.step("Проверка XML-структуры"):
            assert response.status_code == 200
            assert "<?xml" in response.text or "<booking>" in response.text

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение бронирования с несуществующим ID")
    def test_get_booking_invalid_id(self):
        """Получение бронирования с несуществующим ID."""
        with allure.step("GET /booking/99999999"):
            response = requests.get(f"{API_BASE_URL}/booking/99999999")
            attach_response(response)

        with allure.step("Проверка 404"):
            assert response.status_code == 404

    @allure.story("Получение по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Проверка структуры ответа бронирования")
    def test_get_booking_response_structure(self, created_booking):
        """Проверка структуры ответа бронирования."""
        booking_id, _ = created_booking

        with allure.step(f"GET /booking/{booking_id}"):
            response = requests.get(f"{API_BASE_URL}/booking/{booking_id}")
            attach_response(response)

        with allure.step("Проверка наличия обязательных полей"):
            assert response.status_code == 200
            data = response.json()
            required_fields = [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates",
            ]
            for field in required_fields:
                assert field in data, f"Отсутствует поле: {field}"
            assert "checkin" in data["bookingdates"]
            assert "checkout" in data["bookingdates"]
