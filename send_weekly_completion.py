import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info


recipients = pd.read_csv('data/Weekly21 - Completion')
recipients = recipients.drop_duplicates('Name')
drive_info = pd.read_csv('certificates/weekly-completion/result.csv')
drive_info = drive_info.drop_duplicates('2')

merged_df = recipients.merge(drive_info, left_on='Name', right_on='2')


SUBJECT = 'Completed Submission: Recommendation System with Tensorflow - Weekly Class Machine Learning/AI 2021'
MESSAGE = "Hello!\n\
Thank you for completing your recommendation system submission! If you recieve this email, you have participated in all 3 weeks of ML & AI Weekly Class and Submitted your github & heroku link. \
We are so delighted to reward your effort with this Completion Certificate!\n\
\n\
Best regards,\n\
GDSC UG\n\
Together We Grow <>"

api = GoogleAPI(folder_id='1WJiZmgTL4IPbR1stfES7GCFBPJ3taQA7',
                client_secret_path='secrets/client_secret.json',
                mailmerge_log_name='weekly-completion')

CERTIFICATE_FOLDER = 'certificates/weekly-completion/'
import os
for i, row in merged_df.iterrows():
    certificate_path = CERTIFICATE_FOLDER + row['Name'].upper() + '.pdf'
    api.send_certificate(row['Username'], SUBJECT, MESSAGE, certificate_path)
