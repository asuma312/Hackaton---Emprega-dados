import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

class GoogleSheetsSDK:
    """
    SDK para acesso ao Google Sheets usando credenciais de um arquivo JSON.
    """

    def __init__(self, credentials_path='credentials_sheets.json'):
        """
        Inicializa o SDK carregando as credenciais e criando o serviço.

        :param credentials_path: Caminho para o arquivo de credenciais JSON.
        """
        self.credentials_path = credentials_path
        self.service = self._create_service()

    def _create_service(self):
        """
        Cria o serviço da API do Google Sheets utilizando as credenciais.

        :return: Objeto de serviço para acesso à API.
        """
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, scopes=scopes
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service

    def baixar_sheet(self, spreadsheet_id, sheet_name, csv_name, skiprows=0, hard_coded_columns:list=None):
        """
        Baixa toda a aba especificada de uma planilha.

        :param spreadsheet_id: ID da planilha do Google Sheets.
        :param sheet_name: Nome da aba (sheet) a ser baixada.
        :return: Lista de listas com os valores contidos na aba.
        """
        range_name = sheet_name
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name
        ).execute()
        values = result.get('values', [])
        if len(values) == 0:
            return
        colunas = values[skiprows]
        if hard_coded_columns:
            colunas = hard_coded_columns
        linhas = values[skiprows+1:]
        df = pd.DataFrame(linhas, columns=colunas)
        df.to_csv(f'{csv_name}', index=False, sep=';', encoding='utf-8-sig')

        return csv_name


if __name__ == '__main__':
    credentials_path = os.path.join(
        os.path.dirname(__file__),
        'test'
    )
    SPREADSHEET_ID = '1FXqYw-1ynGcMiE7wcAswZewzgL6x-WDH49T4W1QVEN8'
    SHEET_NAME = 'DEVOLUÇÕES / GARANTIA'
    csv_name = 'devolucoes_garantia'


    sdk = GoogleSheetsSDK(credentials_path='credentials_sheets.json')
    dados = sdk.baixar_sheet(SPREADSHEET_ID, SHEET_NAME, csv_name)