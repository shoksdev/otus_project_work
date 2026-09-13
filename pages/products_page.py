import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Страница со списком товаров."""

    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCH_RESULTS_TITLE = (By.XPATH, "//h2[contains(text(),'Searched Products')]")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    FIRST_VIEW_PRODUCT = (By.CSS_SELECTOR, ".choose a[href*='/product_details/1']")

    @allure.step("Найти товар: {keyword}")
    def search_product(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        return self

    def is_search_results_visible(self):
        return self.is_visible(self.SEARCH_RESULTS_TITLE)

    @allure.step("Получить количество найденных товаров")
    def get_result_count(self, timeout=5):
        """
        Получить количество найденных товаров.
        Если ни одного товара не появилось за timeout — вернуть 0.
        """
        if self.is_any_present(self.PRODUCT_ITEMS, timeout=timeout):
            return len(self.find_all_nowait(self.PRODUCT_ITEMS))
        return 0

    @allure.step("Получить список названий товаров")
    def get_product_names(self):
        elements = self.find_all(self.PRODUCT_NAMES)
        return [el.text.strip() for el in elements]
