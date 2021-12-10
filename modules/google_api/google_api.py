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

        self.gmail = GmailAPI(client_secret_path)


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

    def send_certificate(self, email, subject, message_text, certificate_path):
        self.gmail.send_email(email, subject, message_text, certificate_path)

class GmailAPI:
    def __init__(self, client_secret_path):
        self.service = Create_Service(
            client_secret_path,
            'gmail', 'v1',
            ['https://mail.google.com/'])
        time.sleep(2)

    def send_email(self, email, subject, message_text, certificate_path):
        # writing email
        message = MIMEMultipart()
        message['to'] = email 
        message['subject'] = subject 

        message.attach(MIMEText(message_text))

        with open(certificate_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')

        attachment.add_header('Content-Disposition', 
                              'attachment', 
                              filename=certificate_path.split('/')[-1])
        message.attach(attachment)
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = self.service_gmail.users().messages().send(
                userId='me',
                body={'raw': raw}).execute()
