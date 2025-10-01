from playwright.sync_api import sync_playwright
import time

class OlhaNoisAquideNovo():
    def __init__(self, link):
        self.link = link
        

    def testando (self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(self.link)
            time.sleep(5)
            page.close()



url = 'https://rpachallenge.com/?lang=EN'
oia = OlhaNoisAquideNovo(url)
oia.testando()