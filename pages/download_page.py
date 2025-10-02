import os

class DownloadPage:
    def __init__ (self, download_button: str, download_path: str):
        self.download_button = download_button
        self.download_path = download_path

    def download_page(self):
        try:
            ...

        except Exception as e:
            return  f' Butão não encontrato: {e}'