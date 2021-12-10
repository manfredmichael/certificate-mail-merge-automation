from .GoogleUtils import Create_Service, read_structural_elements, read_paragraph_element
from googleapiclient.http import MediaFileUpload 
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import time
import base64
import os


class GoogleAPI:
    def __init__(self, folder_id, client_secret_path='secrets/client_secret.json'):
        self.folder_id = folder_id
        self.load_services(client_secret_path)

    def load_services(self, client_secret_path):
        self.service_drive = Create_Service(
            client_secret_path,
            'drive',
            'v3',
            ['https://www.googleapis.com/auth/drive']
        )
        time.sleep(2)

        self.service_gmail = Create_Service(
            client_secret_path,
            'gmail', 'v1',
            ['https://mail.google.com/'])
        time.sleep(2)

    def upload_certificate_to_drive(self, certificate_path):
        media_object = MediaFileUpload(certificate_path, mimetype='application/pdf')
        certificate = self.service_drive.files().create(
            media_body=media_object,
            body={
                'parents': [self.folder_id],
                'name': os.path.basename(certificate_path)
            },
            fields='webViewLink'
        ).execute()
        url = certificate.get('webViewLink')
        return url
