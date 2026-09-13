import os

import allure
import pytest
import requests
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

API_BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
API_USERNAME = os.getenv("USERNAME", "admin")
API_PASSWORD = os.getenv("PASSWORD", "password123")
UI_BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_AUTH_CREDENTIALS = {"username": API_USERNAME, "password": API_PASSWORD}
SELENOID_URL = os.getenv("SELENOID_URL")


@pytest.fixture(scope="session")
@allure.title("Получение токена авторизации")
def auth_token():
    """Получение токена авторизации для тестовой сессии."""
    with allure.step("POST /auth с валидными учётными данными"):
        response = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS)
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_headers(auth_token):
    """Заголовки с токеном авторизации."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_token}",
    }


@pytest.fixture
def basic_auth_headers():
    """Заголовки с Basic Auth."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM=",
    }


@pytest.fixture
def booking_payload():
    """Стандартный payload для создания бронирования."""
    return {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-10"},
        "additionalneeds": "Breakfast",
    }


def attach_response(response):
    """Прикрепляет детали HTTP-ответа к Allure-отчёту."""
    allure.attach(
        f"{response.request.method} {response.request.url}",
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(
        str(response.status_code),
        name="Status Code",
        attachment_type=allure.attachment_type.TEXT,
    )
    allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)


@pytest.fixture
def created_booking(booking_payload):
    """Создание бронирования и возврат его ID и данных."""
    with allure.step("Создание тестового бронирования (setup)"):
        response = requests.post(f"{API_BASE_URL}/booking", json=booking_payload)
        assert response.status_code == 200
        data = response.json()
        booking_id = data["bookingid"]
        allure.attach(
            str(booking_id),
            name="Created Booking ID",
            attachment_type=allure.attachment_type.TEXT,
        )

    yield booking_id, data["booking"]

    with allure.step("Удаление тестового бронирования (cleanup)"):
        try:
            token_resp = requests.post(f"{API_BASE_URL}/auth", json=API_AUTH_CREDENTIALS)
            token = token_resp.json().get("token")
            requests.delete(
                f"{API_BASE_URL}/booking/{booking_id}",
                headers={"Cookie": f"token={token}"},
            )
        except Exception:
            pass


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def _build_chrome_options():
    """Общие опции для локального и удалённого запуска."""
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-allow-origins=*")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Selenoid-специфичные capabilities
    options.set_capability("selenoid:options", {
        "enableVNC": True,          # смотреть браузер в Selenoid UI
        "enableVideo": True,        # запись видео
        "videoName": "test.mp4",
        "screenResolution": "1920x1080x24",
        "sessionTimeout": "5m",
    })
    return options


@pytest.fixture(scope="function")
def driver(request):
    """
    Драйвер: локальный Chrome или Remote через Selenoid.
    Переключение — переменной окружения SELENOID_URL.
    """
    options = _build_chrome_options()

    if SELENOID_URL:
        # === Запуск через Selenoid ===
        allure.step(f"Запуск через Selenoid: {SELENOID_URL}")
        driver = webdriver.Remote(
            command_executor=SELENOID_URL,
            options=options
        )
    else:
        # === Локальный Chrome (headless) ===
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(5)
    request.cls.driver = driver

    yield driver

    # Скриншот при падении — работает в обоих режимах
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        with allure.step("Скриншот при падении"):
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG
            )

    driver.quit()


@pytest.fixture(scope="function")
def base_url():
    return UI_BASE_URL


@pytest.fixture
def faker_instance():
    return Faker()
