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
import logging
import json
from colorama import Fore, Style


class GoogleAPI:
    def __init__(self, folder_id, mailmerge_log_name=None, client_secret_path='secrets/client_secret.json'):
        self.folder_id = folder_id
        self.load_services(client_secret_path)

        if mailmerge_log_name:
            self.gmail_logger = GmailLogger(mailmerge_log_name)    # To prevent sending email more than once

    def set_gmaiL_logger(self, mailmerge_log_name):
        self.gmail_logger = GmailLogger(mailmerge_log_name)    # To prevent sending email more than once

    def load_services(self, client_secret_path):
        self.service_drive = Create_Service(
            client_secret_path,
            'drive',
            'v3',
            ['https://www.googleapis.com/auth/drive']
        )
        time.sleep(2)

        self.gmail = GmailAPI(client_secret_path)

    def create_folder(self, folder_name):
        file_metadata = {
            'name': folder_name,
            'parents': [self.folder_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service_drive.files().create(body=file_metadata,
                                    fields='id').execute()
        return file.get('id')

    def upload_certificate_to_drive(self, certificate_path, folder_id):
        media_object = MediaFileUpload(certificate_path, mimetype='application/pdf')
        certificate = self.service_drive.files().create(
            media_body=media_object,
            body={
                'parents': [folder_id],
                'name': os.path.basename(certificate_path)
            },
            fields='webViewLink'
        ).execute()
        url = certificate.get('webViewLink')
        return url

    def send_certificate(self, email, subject, message_text, certificate_path):
        if not self.gmail_logger.is_sent(email):
            try:
                print(f'Email is being sent to {email}: ', end='')
                self.gmail.send_email(email, subject, message_text, certificate_path)
                self.gmail_logger.add_log(email)
                print(Fore.GREEN + 'Succesful!' + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + str(e) + Style.RESET_ALL)
            finally:
                self.gmail_logger.save_log()



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
        message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw}).execute()

class GmailLogger:
    def __init__(self, name):
        self.name = name
        self.create_log_file()
        self.log = self.load_current_log()

    def create_log_file(self):
        if not os.path.isfile(f'logs/{self.name}.json'):
            with open(f'logs/{self.name}.json','w') as f:
                f.write(json.dumps({'EMAIL_SENT':[], 'CURRENT_CERT_NO':1}, indent=2))

    def load_current_log(self):
        with open(f'logs/{self.name}.json','r') as f:
            return json.load(f)

    def is_sent(self, email):
        return email in self.log['EMAIL_SENT']

    def add_log(self, email):
        self.log['EMAIL_SENT'].append(email)
        self.log['CURRENT_CERT_NO'] += 1

    def save_log(self): 
        with open(f'logs/{self.name}.json','w') as f:
            f.write(json.dumps(self.log, indent=2))
    

