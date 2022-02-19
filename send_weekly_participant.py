import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info


recipients = pd.read_csv('data/weekly/WEB - Weekly- Participant')
recipients = recipients.drop_duplicates('Name')
drive_info = pd.read_csv('certificates/weekly-peserta/result.csv')
drive_info = drive_info.drop_duplicates('2')

merged_df = recipients.merge(drive_info, left_on='Name', right_on='2')


SUBJECT = 'Weekly Class Web Development 2022 Participation'
MESSAGE = open('templates/weekly/participant-email-text').read()

api = GoogleAPI(folder_id='1i9XtuYN4XWvLjeG7Shcfqz8wp8xci5W8',
                client_secret_path='secrets/client_secret.json',
                mailmerge_log_name='weekly-participant')

CERTIFICATE_FOLDER = 'certificates/weekly-peserta/'
import os
for i, row in merged_df.iterrows():
    certificate_path = CERTIFICATE_FOLDER + row['Name'].upper() + '.pdf'
    api.send_certificate(row['Username'], SUBJECT, MESSAGE.replace('[NAME]', row['Name']), certificate_path)
