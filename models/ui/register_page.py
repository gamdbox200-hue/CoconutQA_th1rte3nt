from playwright.sync_api import Page

from models.ui.base_page import BasePage


class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"

        self.full_name_input = "[data-qa-id='register_full_name_input']"
        self.email_input = "[data-qa-id='register_email_input']"
        self.password_input = "[data-qa-id='register_password_input']"
        self.repeat_password_input = "[data-qa-id='register_password_repeat_input']"
        self.register_button = "[data-qa-id='register_submit_button']"
        self.sign_button = "a[href='/login' and text()='Войти']"

    def open(self):
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, confirm_password)
        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_alert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")
