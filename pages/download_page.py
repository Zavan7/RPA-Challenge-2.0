import os
import logging
from pathlib import Path
from playwright.sync_api import Page

from config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

class DownloadPage:
    def __init__(self, download_button_selector: str, download_path: Path):
        self.download_button_selector = download_button_selector
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def download_page(self, page: Page):
        '''
        Prepara o ambiente para receber e iniciar o download do arquivo com as informações
        que serão inseridas no formulário. Recebe STR do botão de download, caminho do diretório
        e a PAGE (instância do Playwright).
        '''
        try:
            button = page.locator(self.download_button_selector)

            if not (button.is_visible() and button.is_enabled()):
                logger.error("Botão de download não está visível ou habilitado.")
                return None

            with page.expect_download() as download_info:
                button.click()

            download = download_info.value
            file_path = self.download_path / download.suggested_filename
            download.save_as(file_path)

            logger.info(f"Download concluído: {file_path}")
            return file_path

        except Exception as e:
            logger.exception(f"Erro no download: {e}")
            return None
