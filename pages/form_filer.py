import logging
import pandas as pd

from playwright.sync_api import Page

from config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

class FormFiller:
    """Classe responsável por preencher o formulário no site."""

    def __init__(self, page: Page):
        self.page = page

    def fill_form(self, df: pd.DataFrame):
        # Normaliza nomes das colunas
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():
            try:
                # Extrai os valores
                campo_first_name = row['First Name']
                campo_last_name = row['Last Name']
                campo_company = row['Company Name']
                campo_role = row['Role in Company']
                campo_address = row['Address']
                campo_email = row['Email']
                campo_phone = row['Phone Number']

                # Preenche com espera
                self.page.wait_for_selector('[ng-reflect-name="labelFirstName"]')
                self.page.fill('[ng-reflect-name="labelFirstName"]', campo_first_name)
                self.page.fill('[ng-reflect-name="labelLastName"]', campo_last_name)
                self.page.fill('[ng-reflect-name="labelCompanyName"]', campo_company)
                self.page.fill('[ng-reflect-name="labelRole"]', campo_role)
                self.page.fill('[ng-reflect-name="labelAddress"]', campo_address)
                self.page.fill('[ng-reflect-name="labelEmail"]', campo_email)
                self.page.fill('[ng-reflect-name="labelPhone"]', str(campo_phone))

                # Clica no botão de enviar
                self.page.locator("form input[type='submit']").click()

                self.page.wait_for_timeout(500)

            except Exception as e:
                logging.error(f"⚠️ Erro ao preencher linha: {e}")

class FinalInfo:
    def __init__(self, locator_info: str, page: Page):
        self.locator_info = locator_info
        self.page = page

    def final_info(self):
        try:
            info_final = self.page.locator(self.locator_info)

            if info_final.count() == 0:
                logger.warning('Nenhum elemento localizado para informações finais')
                return None
            
            value = info_final.inner_text()
            logger.info(f"Resultado final capturado no site: {value}")
            return value

        except Exception as e:
            logger.exception("Erro ao capturar informações finais da automação")
            return None