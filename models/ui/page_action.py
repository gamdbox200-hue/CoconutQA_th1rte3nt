import time
import allure
from playwright.sync_api import Page, Error as PlaywrightError


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        for attempt in range(3):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                return
            except PlaywrightError:
                if attempt == 2:
                    raise
                time.sleep(3)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения с текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            notification_locator.wait_for(state="hidden")
            assert not notification_locator.is_visible(), "Уведомление не исчезло"
