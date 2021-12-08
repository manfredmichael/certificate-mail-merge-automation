import pandas as pd
from tqdm import tqdm

from certificate_generator.generator import Generator
from certificate_generator import utils


ATTENDANCE_EMAIL_COLUMN = 'Username'
REGISTERED_EMAIL_COLUMN = 'Confirm you email...'

attendance = pd.read_csv('data/Recipients.csv')
registered = pd.read_csv('data/Registered Attendees.csv')

# Filter only attendance who both registered & attended the event
filtered = attendance.merge(registered,
                            left_on=ATTENDANCE_EMAIL_COLUMN,
                            right_on=REGISTERED_EMAIL_COLUMN)

# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/CERTIFICATE OF PARTICIPANT.pdf',
                      name=(435, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      qr_logo_path='imgs/dsc_mask.png')

# Setup certificate code
CERTIFICATE_CODE = 'MYML041221PT'
START_CERTIFICATE_NO = 1

print(f'{len(filtered)} certificates will be generated')

for i, row in tqdm(filtered.iterrows(), total=len(filtered)):
    certificate_code = utils.create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    generator.generate(row['Full Name'], certificate_code)
