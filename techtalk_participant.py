import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

# Initialize Gooogle API & configure folder id to store certificates remotely
api = GoogleAPI(folder_id='1WJiZmgTL4IPbR1stfES7GCFBPJ3taQA7',
                client_secret_path='secrets/client_secret.json')

# Initialize Gooogle API & configure folder id to store certificates remotely
api = GoogleAPI(folder_id='1WJiZmgTL4IPbR1stfES7GCFBPJ3taQA7',
                client_secret_path='secrets/client_secret.json')

ATTENDANCE_EMAIL_COLUMN = 'Username'
REGISTERED_EMAIL_COLUMN = 'Confirm you email...'

attendance = pd.read_csv('data/Recipients.csv')
registered = pd.read_csv('data/Registered Attendees.csv')

# Filter only attendance who both registered & attended the event
filtered = attendance.merge(registered,
                            left_on=ATTENDANCE_EMAIL_COLUMN,
                            right_on=REGISTERED_EMAIL_COLUMN)

# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/techtalk/CERTIFICATE OF PARTICIPANT.pdf',
                      name=(435, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      output='certificates/techtalk-peserta',
                      qr_logo_path='imgs/dsc_mask.png')

# Setup certificate code
CERTIFICATE_CODE = 'MYML041221PT'
START_CERTIFICATE_NO = 1

print(f'{len(filtered)} certificates will be generated')

result_df = [] 
for i, row in tqdm(filtered.iterrows(), total=len(filtered)):
    certificate_code = create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    certificate_path = generator.generate(row['Full Name'], certificate_code)

    certificate_url = api.upload_certificate_to_drive(certificate_path)
    certificate_info = get_certificate_info(name=row['Full Name'],
                                            code=certificate_code,
                                            type='Participant',
                                            url=certificate_url,
                                            date_published='4 December 2021',
                                            valid_until='Forever')
    result_df.append(certificate_info)
pd.DataFrame(result_df).to_csv('certificates/techtalk-peserta/result.csv')
