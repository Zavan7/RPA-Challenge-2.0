import pandas as pd
import logging

from config.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


class ReadFile:
    def __init__(self, path_file):
        self.path_file = path_file

    def read_file(self):
        '''
        Localiza o arquivo salvo na pasta e lê, garantindo que o arquivo esteja salvo na pasta de destino
        Recebe apenas a PASTA do ARQUIVO
        '''
        try:
            df = pd.read_excel(self.path_file)
            logging.info('Arquivo localizado com sucesso')
            return df
        
        except FileNotFoundError:
            logging.error(f'Erro, arquivo não encontrato em {self.path_file}')
            return None
        
        except Exception as e:
            logging.error (f'Erro ao ler file {e}')
            return None