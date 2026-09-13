import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    """Страница обратной связи."""

    GET_IN_TOUCH_HEADER = (By.XPATH, "//h2[contains(text(),'Get In Touch')]")
    NAME_INPUT = (By.CSS_SELECTOR, "[data-qa='name']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-qa='email']")
    SUBJECT_INPUT = (By.CSS_SELECTOR, "[data-qa='subject']")
    MESSAGE_INPUT = (By.CSS_SELECTOR, "[data-qa='message']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "[data-qa='submit-button']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".status.alert-success")

    @allure.step("Проверить, что страница Contact Us загрузилась")
    def is_loaded(self):
        return self.is_visible(self.GET_IN_TOUCH_HEADER)

    @allure.step("Заполнить форму обратной связи")
    def fill_form(self, name, email, subject, message):
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.SUBJECT_INPUT, subject)
        self.type_text(self.MESSAGE_INPUT, message)
        return self

    @allure.step("Отправить форму (с принятием alert)")
    def submit(self):
        self.click(self.SUBMIT_BUTTON)
        # Обработка JavaScript alert
        try:
            self.driver.switch_to.alert.accept()
        except Exception:
            pass
        return self

    def is_success_message_visible(self):
        return self.is_visible(self.SUCCESS_MESSAGE)
