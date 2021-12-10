import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info


recipients = pd.read_csv('data/Recipients.csv')
recipients = recipients.drop_duplicates('Full Name')
drive_info = pd.read_csv('certificates/techtalk-peserta/result.csv')
drive_info = drive_info.drop_duplicates('2')

merged_df = recipients.merge(drive_info, left_on='Full Name', right_on='2')


SUBJECT = 'Certificate - Tech Talk Machine Learning & AI 2021: Deep Dive into Machine Learning'
MESSAGE = "Hello!\n\
Thank you so much for your participation in our Tech Talk Machine Learning & AI 2021. Hopefully, this event can bring good changes for the participants and be a good start for us to meet again in the future. As a reward, heres your E-certificate!\n\
\n\
Best regards,\n\
GDSC UG\n\
Together We Grow <>\
Contact Us!\
\n\
\n\
\n\
Instagram: https://www.instagram.com/gdscug/\n\
Discord: https://dscug.club/discord\n\
Email: dscgunadarma@gmail.com"

api = GoogleAPI(folder_id='1WJiZmgTL4IPbR1stfES7GCFBPJ3taQA7',
                client_secret_path='secrets/client_secret.json',
                mailmerge_log_name='techtalk-peserta')

CERTIFICATE_FOLDER = 'certificates/techtalk-peserta/'
import os
for i, row in merged_df.iterrows():
    certificate_path = CERTIFICATE_FOLDER + row['Full Name'].upper() + '.pdf'
    api.send_certificate(row['Username'], SUBJECT, MESSAGE, certificate_path)

