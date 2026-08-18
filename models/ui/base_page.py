import allure
from playwright.sync_api import Page

from models.ui.page_action import PageAction
from constants import UI_BASE_URL


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = f"{UI_BASE_URL}/"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.page.get_by_role("link", name="Cinescope").click()
        self.page.wait_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы', из шапки сайта")
    def go_to_all_movies(self):
        self.page.get_by_role("link", name="Все фильмы").click()
        self.page.wait_for_url(f"{self.home_url}movies")
