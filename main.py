import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

from pages.download_page import DownloadPage
from pages.start_challenge import StartChallenge
from pages.read_file import ReadFile
from pages.form_filer import FormFiller, FinalInfo

from config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

url = "https://rpachallenge.com/?lang=EN"
start_button_selector = "body > app-root > div.body.row1.scroll-y > app-rpa1 > div > div.instructions.col.s3.m3.l3.uiColorSecondary > div:nth-child(7) > button"
download_button_selector = "body > app-root > div.body.row1.scroll-y > app-rpa1 > div > div.instructions.col.s3.m3.l3.uiColorSecondary > div:nth-child(7) > a"

DOWNLOAD_PATH = Path(__file__).parent / "downloads"


if __name__ == "__main__":
    automation_info = {
        'start': None,
        'finish': None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        automation_info['start'] = datetime.now()

        # inicia o desafio
        start = StartChallenge(url, start_button_selector)
        if start.start_challenge(page):
            # faz o download
            downloader = DownloadPage(download_button_selector, DOWNLOAD_PATH)
            downloaded_file = downloader.download_page(page)

            # lê o arquivo Excel
            if downloaded_file:
                leitor = ReadFile(downloaded_file)
                df = leitor.read_file()

                if df is not None:
                    # preenche o formulário
                    filler = FormFiller(page)
                    filler.fill_form(df)
                    
        # captura resultado final no site
        final_info_locator = 'body > app-root > div.body.row1.scroll-y > app-rpa1 > div > div.congratulations.col.s8.m8.l8 > div.message2'
        final_info = FinalInfo(final_info_locator, page)
        resultado = final_info.final_info()
        if resultado:
            automation_info['site_result'] = resultado
            logger.info(f"🏁 Resultado final exibido no site: {resultado}")

        automation_info['finish'] = datetime.now()
        browser.close()

        logging.info(f"🕒 Automação iniciada em: {automation_info['start']}")
        logging.info(f"✅ Automação finalizada em: {automation_info['finish']}")
