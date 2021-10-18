import os
import datetime
import time
import io
from googleapiclient.http import MediaIoBaseUpload
from Google import Create_Service, read_structural_elements, read_paragraph_element
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np

SEND_LIMIT = None# limit email send for testing
send_ctr = 0

EMAIL_SENT_LIST_FILE = 'already_sent.txt'
LOGGING_FILE = 'logging.txt'
CLIENT_SECRET_FILE = 'secrets/client_secret.json'

API_SERVICE_NAME = 'docs'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.send']

"""
Step 1. Create Google API Service Instances
"""
# Google Docs instance
service_docs = Create_Service(
    CLIENT_SECRET_FILE,
    'docs', 'v1',
    ['https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive']
)
time.sleep(2)

# Google Drive instance
service_drive = Create_Service(
    CLIENT_SECRET_FILE,
    'drive',
    'v3',
    ['https://www.googleapis.com/auth/drive']
)
time.sleep(2)

# Google Sheets instance
service_sheets = Create_Service(
    CLIENT_SECRET_FILE,
    'sheets',
    'v4',
    ['https://www.googleapis.com/auth/spreadsheets']
)
time.sleep(2)

service_gmail = Create_Service(
    CLIENT_SECRET_FILE,
    'gmail', 'v1',
    ['https://mail.google.com/'])
time.sleep(2)


template_document_id = '1lW9I8NRkXKcMveIeQGvvEshugbo-NaMqvEQ_xp052jQ'
google_sheets_id = '11tWWn8wuZP_lxBMBPoMaJFb2pnKasfq9iyJY52mRlBg'
folder_id = '1d-OKTs7vf-yruJq1JA89z0IC4eWo5vxR' # None --> save in the parent folder

responses = {}


def mapping(merge_field, value=''):
    json_representation = {
        'replaceAllText': {
            'replaceText': value,
            'containsText': {
                'matchCase': 'true',
                'text': '{{{{{0}}}}}'.format(merge_field)
            }
        }
    }
    return json_representation

def get_referral_code(referral_codes, email):
    for code in referral_codes:
        if code[2] == email:
            return code[4]
    return None

def error_sending(formulation, email):
    for code in formulation:
        if code[1] == email:
            return code[11][:5] == 'Error'
    return None


while True:
    """
    Step 2. Load Records from Google Sheets
    """
    worksheet_name = 'Member Regist'
    responses['sheets'] = service_sheets.spreadsheets().values().get(
        spreadsheetId=google_sheets_id,
        range=worksheet_name,
        majorDimension='ROWS',
    ).execute()

    worksheet_name = 'Referral Users'
    responses['referral_codes'] = service_sheets.spreadsheets().values().get(
        spreadsheetId=google_sheets_id,
        range=worksheet_name,
        majorDimension='ROWS',
    ).execute()

    worksheet_name = 'Formulation'
    responses['formulation'] = service_sheets.spreadsheets().values().get(
        spreadsheetId=google_sheets_id,
        range=worksheet_name,
        majorDimension='ROWS',
    ).execute()

    columns = responses['sheets']['values'][0]
    records = responses['sheets']['values'][1:]
    referral_codes = responses['referral_codes']['values'][1:]
    send_status = responses['formulation']['values'][1:]

    for i in range(10):
        print('Sending in {} seconds '.format(10-i), end='\r', flush=True)
        time.sleep(1)
    print(' '.join([' ' for i in range(20)]), end='\r', flush=True)

    """
    Step 3. Iterate Each Record and Perform Mail Merge
    """
    with open(EMAIL_SENT_LIST_FILE, 'r') as f:
        already_sent_emails = [email.replace('\n','').strip() for email in f.readlines()]
    for record in records:
        try:
            email_address = record[1]
            nama = record[2]
        except:   # when the form is empty, just skip it 
            continue

        if email_address in already_sent_emails:
            # print('{} already sent, skipping..'.format(record[2]))
            continue
        # Copy template doc file as new doc file
        if not error_sending(send_status, email_address):
            continue

        print('Processing record {0}...'.format(email_address))

        referral_code = get_referral_code(referral_codes, email_address)
        if referral_code is None:
            print('referral code not found from {}'.format(email_address))
            continue

        responses['docs'] = service_docs.documents().get(
            documentId=template_document_id,
        ).execute()
        doc_content = responses['docs'].get('body').get('content')

        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = email_address
        mimeMessage['subject'] = '[GDSUC UG] Member 2021 Welcome'

        emailMsg = read_structural_elements(doc_content).replace('{{REFERRAL_CODE}}', referral_code) \
                                                        .replace('{{EMAIL_ADDRESS}}', email_address) \
                                                        .replace('{{NAMA_LENGKAP}}', nama)
        mimeMessage.attach(MIMEText(emailMsg, 'html'))

        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        try:
            message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
            print('Email sent to {} successfully!'.format(email_address))

            with open(LOGGING_FILE, 'a+') as f:
                f.write('sent to {} - {} on {}\n'.format(nama, email_address, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

            with open(EMAIL_SENT_LIST_FILE, 'a+') as f:
                f.write(email_address+'\n')


            send_ctr += 1
            if SEND_LIMIT:
                if send_ctr >= SEND_LIMIT:
                    exit()
        except Exception as e:
            print('Failed to sent email to {}'.format(email_address))
            print(e)

            with open(LOGGING_FILE, 'a+') as f:
                f.write('[ERROR] Failed to send to {} - {} on {}\n    - Reason: {}'.format(nama, email_address, datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), e))

            continue
        # print(emailMsg)
        print()



    time.sleep(240)
    print()

print('Mail Merge Complete.')
