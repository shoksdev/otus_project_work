import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины."""

    CART_TABLE = (By.ID, "cart_info_table")
    CART_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    EMPTY_CART = (By.XPATH, "//b[contains(text(),'Cart is empty')]")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".cart_description h4 a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".cart_price p")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, ".cart_quantity button")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".btn.check_out")

    @allure.step("Получить количество товаров в корзине")
    def get_item_count(self):
        if self.is_visible(self.EMPTY_CART, timeout=3):
            return 0
        return len(self.find_all(self.CART_ROWS))

    @allure.step("Получить названия товаров в корзине")
    def get_product_names(self):
        elements = self.find_all(self.PRODUCT_NAMES)
        return [el.text.strip() for el in elements]

    def is_cart_empty(self):
        return self.is_visible(self.EMPTY_CART)
