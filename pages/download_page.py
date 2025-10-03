import os
from pathlib import Path
from playwright.sync_api import Page

class DownloadPage:
    def __init__(self, download_button_selector: str, download_path: Path):
        self.download_button_selector = download_button_selector
        self.download_path = download_path
        os.makedirs(self.download_path, exist_ok=True)

    def download_page(self, page: Page):
        try:
            button = page.locator(self.download_button_selector)

            if not (button.is_visible() and button.is_enabled()):
                print("Erro ao clicar no botão de download")
                return None

            with page.expect_download() as download_info:
                button.click()

            download = download_info.value
            file_path = self.download_path / download.suggested_filename
            download.save_as(file_path)

            print(f"Download concluído: {file_path}")
            return file_path

        except Exception as e:
            print(f"Erro no download: {e}")
            return None
