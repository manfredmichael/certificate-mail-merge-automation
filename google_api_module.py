from Google import Create_Service, read_structural_elements, read_paragraph_element
from googleapiclient.http import MediaFileUpload 
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pandas as pd
import time
import base64


class GoogleAPI:
    def __init__(self, docs_id, sheets_id, folder_id):
        self.docs_id = docs_id
        self.sheets_id = sheets_id
        self.folder_id = folder_id

    def load_services(self, client_secret_path='secrets/client_secret.json'):
        self.service_drive = Create_Service(
            client_secret_path,
            'drive',
            'v3',
            ['https://www.googleapis.com/auth/drive']
        )
        time.sleep(2)
        self.service_docs = Create_Service(
            client_secret_path,
            'docs',
            'v1',
            ['https://www.googleapis.com/auth/documents']
        )
        time.sleep(2)
        self.service_sheets = Create_Service(
            client_secret_path,
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets']
        )
        time.sleep(2)
        self.service_gmail = Create_Service(
            client_secret_path,
            'gmail', 'v1',
            ['https://mail.google.com/'])
        time.sleep(2)

    def get_responses(self, worksheet='Main'):
        records = self.service_sheets.spreadsheets().values().get(
            spreadsheetId=self.sheets_id,
            range=worksheet,
            majorDimension='ROWS',
        ).execute()
        columns = records['values'][0]
        records = records['values'][1:]
        responses = pd.DataFrame(records, columns=columns)
        return responses

    def add_certificate_log(self, code, name, cert_type, valid_until, url, worksheet):
        values = [
            code,
            datetime.now().strftime('%d %B %Y'),
            name,
            cert_type,
            valid_until,
            url]
        values = [values]
        self.service_sheets.spreadsheets().values().append(
          spreadsheetId=self.sheets_id,
          range=worksheet,
          body={
              "majorDimension": "ROWS",
              "values": values
          },
          valueInputOption="USER_ENTERED"
        ).execute()

    def upload_certificate(self, certificate_path):
        media_object = MediaFileUpload(certificate_path, mimetype='application/pdf')
        certificate = self.service_drive.files().create(
            media_body=media_object,
            body={
                'parents': [self.folder_id],
                'name': '{}'.format(certificate_path.split('/')[-1])
            },
            fields='webViewLink'
        ).execute()
        url = certificate.get('webViewLink')
        return url

    def send_certificate(self, email, subject, message_text, certificate_path):
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
