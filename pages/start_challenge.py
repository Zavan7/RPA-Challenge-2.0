from playwright.sync_api import sync_playwright
import time

class StartChallenge:
    '''
    Classe inicializa a navegação no site, recebendo os parametros URL e BOTÃO DE START.
    Abre o site, localiza via locator, o botão de start, iniciando o timer do desafio.
    '''

    def __init__ (self, url: str, start_button: str):
        self.url = url
        self.start_button = start_button

    def start_challenge(self):
        try:
            with sync_playwright() as p:

                browser = p.chromium.launch(headless=False)
                page = browser.new_page
                page.goto(self.url)

                self.start_button.click()

        except Exception as e:
            return f'Butão de start não encontrato: {e}'