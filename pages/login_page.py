import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации и регистрации."""

    # Форма логина
    LOGIN_EMAIL = (By.CSS_SELECTOR, "[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-qa='login-button']")
    LOGIN_ERROR = (By.CSS_SELECTOR, ".login-form p[style*='color: red']")

    # Форма регистрации
    SIGNUP_NAME = (By.CSS_SELECTOR, "[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "[data-qa='signup-button']")
    SIGNUP_ERROR = (By.CSS_SELECTOR, ".signup-form p[style*='color: red']")

    # Признаки успешного логина
    LOGGED_IN_AS = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")

    @allure.step("Войти с email {email} и паролем {password}")
    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    @allure.step("Зарегистрироваться с именем {name} и email {email}")
    def signup(self, name, email):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)
        return self

    def is_login_error_visible(self):
        return self.is_visible(self.LOGIN_ERROR)

    def is_signup_error_visible(self):
        return self.is_visible(self.SIGNUP_ERROR)

    def is_logged_in(self):
        return self.is_visible(self.LOGGED_IN_AS)
