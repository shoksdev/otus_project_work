import allure
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый класс для всех Page Object — общие методы работы с элементами."""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path=""):
        """Открыть страницу по указанному пути."""
        with allure.step(f"Открыть страницу: {self.base_url}{path}"):
            self.driver.get(f"{self.base_url}{path}")
            return self

    def find(self, locator):
        """Дождаться видимости элемента и вернуть его."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Дождаться появления хотя бы одного элемента и вернуть все."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def find_all_nowait(self, locator):
        """
        Вернуть все элементы без ожидания.
        Возвращает пустой список, если элементов нет.
        Использовать для негативных сценариев, где ожидается пустой результат.
        """
        return self.driver.find_elements(*locator)

    def click(self, locator):
        """Дождаться кликабельности и кликнуть."""
        with allure.step(f"Клик по элементу: {locator}"):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            try:
                element.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)
            return self

    def type_text(self, locator, text):
        """Очистить поле и ввести текст."""
        with allure.step(f"Ввод текста '{text}' в: {locator}"):
            element = self.find(locator)
            element.clear()
            element.send_keys(text)
            return self

    def get_text(self, locator):
        """Получить текст элемента."""
        return self.find(locator).text

    def is_visible(self, locator, timeout=5):
        """Проверить видимость элемента (не бросает исключение)."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to(self, locator):
        """Проскроллить к элементу."""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return self

    def is_any_present(self, locator, timeout=5):
        """
        Проверить, что хотя бы один элемент присутствует в DOM.
        Возвращает True/False, не бросает исключение.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
