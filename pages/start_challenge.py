from playwright.sync_api import Page
import time

class StartChallenge:
    def __init__(self, url: str, start_button_selector: str, timeout=4000):
        self.url = url
        self.start_button_selector = start_button_selector
        self.timeout = timeout

    def start_challenge(self, page: Page):
        try:
            page.goto(self.url)

            page.wait_for_selector(self.start_button_selector, timeout=self.timeout)
            button = page.locator(self.start_button_selector)

            if not (button.is_visible() and button.is_enabled()):
                print("Erro ao clicar no botão")
                return False

            button.click()
            print("Botão de Start clicado com sucesso!")
            time.sleep(3)
            return True

        except Exception as e:
            print(f"Botão de start não encontrado: {e}")
            return False
