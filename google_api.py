from Google import Create_Service, read_structural_elements, read_paragraph_element
import time


class GoogleAPI:
    def __init__(self, docs_id, sheets_id, folder_id, client_secret_path='secrets/client_secret.json'):
        self.service_docs = Create_Service(
            CLIENT_SECRET_FILE,
            'drive',
            'v3',
            ['https://www.googleapis.com/auth/drive']
        )
        time.sleep(2)
        self.service_sheets = Create_Service(
            CLIENT_SECRET_FILE,
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets']
        )
        time.sleep(2)
        self.service_gmail = Create_Service(
            CLIENT_SECRET_FILE,
            'gmail', 'v1',
            ['https://mail.google.com/'])
        time.sleep(2)



