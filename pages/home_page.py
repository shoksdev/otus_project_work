import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    """Главная страница и навигация."""

    # Навигация
    LOGO = (By.CSS_SELECTOR, "img[alt='Website for automation practice']")
    NAV_SIGNUP_LOGIN = (By.CSS_SELECTOR, "a[href='/login']")
    NAV_PRODUCTS = (By.CSS_SELECTOR, "a[href='/products']")
    NAV_CART = (By.CSS_SELECTOR, "a[href='/view_cart']")
    NAV_CONTACT_US = (By.CSS_SELECTOR, "a[href='/contact_us']")
    NAV_TEST_CASES = (By.CSS_SELECTOR, "a[href='/test_cases']")

    # Контент главной
    SLIDER = (By.CSS_SELECTOR, "#slider-carousel")
    FEATURED_ITEMS = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    SUBSCRIPTION_HEADER = (By.XPATH, "//h2[contains(text(),'Subscription')]")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BUTTON = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.CSS_SELECTOR, ".alert-success")

    @allure.step("Проверить, что главная загрузилась")
    def is_loaded(self):
        return self.is_visible(self.LOGO) and self.is_visible(self.SLIDER)

    @allure.step("Перейти в Signup / Login")
    def go_to_login(self):
        self.click(self.NAV_SIGNUP_LOGIN)
        from pages.login_page import LoginPage

        return LoginPage(self.driver, self.base_url)

    @allure.step("Перейти в Products")
    def go_to_products(self):
        self.click(self.NAV_PRODUCTS)
        from pages.products_page import ProductsPage

        return ProductsPage(self.driver, self.base_url)

    @allure.step("Перейти в Cart")
    def go_to_cart(self):
        self.click(self.NAV_CART)
        from pages.cart_page import CartPage

        return CartPage(self.driver, self.base_url)

    @allure.step("Перейти в Contact Us")
    def go_to_contact(self):
        self.click(self.NAV_CONTACT_US)
        from pages.contact_page import ContactPage

        return ContactPage(self.driver, self.base_url)

    @allure.step("Получить количество товаров в 'Featured'")
    def get_featured_count(self):
        return len(self.find_all(self.FEATURED_ITEMS))

    @allure.step("Подписаться на рассылку: {email}")
    def subscribe(self, email):
        self.scroll_to(self.SUBSCRIPTION_HEADER)
        self.type_text(self.SUBSCRIPTION_EMAIL, email)
        self.click(self.SUBSCRIPTION_BUTTON)
        return self

    def is_subscription_success(self):
        return self.is_visible(self.SUBSCRIPTION_SUCCESS)
