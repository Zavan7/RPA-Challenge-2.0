from playwright.sync_api import sync_playwright
from pages.start_challenge import StartChallenge
from pages.download_page import DownloadPage
from pathlib import Path

url = "https://rpachallenge.com/?lang=EN"
start_button_selector = "body > app-root > div.body.row1.scroll-y > app-rpa1 > div > div.instructions.col.s3.m3.l3.uiColorSecondary > div:nth-child(7) > button"
download_button_selector = "body > app-root > div.body.row1.scroll-y > app-rpa1 > div > div.instructions.col.s3.m3.l3.uiColorSecondary > div:nth-child(7) > a"

DOWNLOAD_PATH = Path(__file__).parent / "downloads"

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # inicia o desafio
        start = StartChallenge(url, start_button_selector)
        if start.start_challenge(page):
            # faz o download
            downloader = DownloadPage(download_button_selector, DOWNLOAD_PATH)
            downloader.download_page(page)

        browser.close()
