import allure
import requests

from conftest import API_BASE_URL, attach_response


@allure.epic("Restful Booker API")
@allure.feature("Booking - GetBookingIds")
class TestGetBookingIds:
    """Тесты для получения списка ID бронирований."""

    @allure.story("Получение списка")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Получение всех ID бронирований")
    def test_get_all_booking_ids(self):
        """Получение всех ID бронирований."""
        with allure.step("Отправка GET /booking"):
            response = requests.get(f"{API_BASE_URL}/booking")
            attach_response(response)

        with allure.step("Проверка структуры ответа"):
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert all("bookingid" in item for item in data)

    @allure.story("Фильтрация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Фильтрация бронирований по firstname")
    def test_get_booking_ids_filter_by_firstname(self):
        """Фильтрация по firstname."""
        with allure.step("GET /booking?firstname=Sally"):
            response = requests.get(f"{API_BASE_URL}/booking", params={"firstname": "Sally"})
            attach_response(response)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.story("Фильтрация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Фильтрация бронирований по lastname")
    def test_get_booking_ids_filter_by_lastname(self):
        """Фильтрация по lastname."""
        with allure.step("GET /booking?lastname=Brown"):
            response = requests.get(f"{API_BASE_URL}/booking", params={"lastname": "Brown"})
            attach_response(response)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.story("Фильтрация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Фильтрация бронирований по датам checkin/checkout")
    def test_get_booking_ids_filter_by_dates(self):
        """Фильтрация по датам checkin/checkout."""
        with allure.step("GET /booking с параметрами checkin и checkout"):
            response = requests.get(
                f"{API_BASE_URL}/booking",
                params={"checkin": "2014-01-01", "checkout": "2016-01-01"},
            )
            attach_response(response)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    @allure.story("Фильтрация")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Фильтрация по несуществующему имени возвращает пустой список")
    def test_get_booking_ids_filter_no_match(self):
        """Фильтрация с несуществующим именем — пустой список."""
        with allure.step("GET /booking?firstname=NonExistentName12345"):
            response = requests.get(f"{API_BASE_URL}/booking", params={"firstname": "NonExistentName12345"})
            attach_response(response)

        with allure.step("Проверка пустого списка"):
            assert response.status_code == 200
            assert response.json() == []
