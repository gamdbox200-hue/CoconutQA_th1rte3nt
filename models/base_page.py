import allure
from playwright.sync_api import Page

from models.page_action import PageAction


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.page.get_by_role("link", name="Cinescope").click()
        self.page.wait_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы', из шапки сайта")
    def go_to_all_movies(self):
        self.page.get_by_role("link", name="Все фильмы").click()
        self.page.wait_for_url(f"{self.home_url}movies")
