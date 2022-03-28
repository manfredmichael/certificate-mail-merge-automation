import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info


recipients = pd.read_csv('data/monthly/Certificate Tech Talk Web Development 2022 (Responses) - Form Responses 1.csv')
recipients = recipients.drop_duplicates('Full Name')
drive_info = pd.read_csv('certificates/techtalk-peserta/result.csv')
drive_info = drive_info.drop_duplicates('2')

merged_df = recipients.merge(drive_info, left_on='Full Name', right_on='2')


SUBJECT = 'Certificate - Tech Talk Web Development 2022'
MESSAGE = open('templates/monthly/participant-email.txt').read()

api = GoogleAPI(folder_id='1h-yvyo_4cBXzVWMfuC-QDh6qxyFnkaso',
                client_secret_path='secrets/client_secret.json',
                mailmerge_log_name='techtalk-peserta')

CERTIFICATE_FOLDER = 'certificates/techtalk-peserta/'
import os
for i, row in merged_df.iterrows():
    certificate_path = CERTIFICATE_FOLDER + row['Full Name'].upper() + '.pdf'
    api.send_certificate(row['Email Address'], SUBJECT, MESSAGE.replace('[NAME]', row['Full Name']), certificate_path)

