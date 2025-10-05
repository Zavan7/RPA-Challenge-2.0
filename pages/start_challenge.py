import logging
from playwright.sync_api import Page
from config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)



class StartChallenge:
    def __init__(self, url: str, start_button_selector: str, timeout=4000):
        self.url = url
        self.start_button_selector = start_button_selector
        self.timeout = timeout

    def start_challenge(self, page: Page):
        """
        Inicializa o desafio, inciando o contador do site do desafio, localizando via locator
        Recebe a URL, STR do locator do BOTÃO de START, e um timeout de 4 segundos, aguardando as informações ficarem visíveis
        """
        try:
            page.goto(self.url)

            page.wait_for_selector(self.start_button_selector, timeout=self.timeout)
            button = page.locator(self.start_button_selector)

            if not (button.is_visible() and button.is_enabled()):
                logging.error("Erro ao clicar no botão")
                return False

            button.click()
            logging.info("Botão de Start clicado com sucesso!")
            return True

        except Exception as e:
            logging.error(f"Botão de start não encontrado: {e}")
            return False
