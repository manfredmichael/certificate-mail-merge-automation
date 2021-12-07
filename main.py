import pandas as pd

from certificate_generator.generator import Generator
from certificate_generator import utils


attendance = pd.read_csv('data/Recipients.csv')
registered = pd.read_csv('data/Registered Attendees.csv')

print(attendance.columns)
print(registered.columns)

email_attendance = attendance['Username']
email_registered = registered['Confirm you email...']

print(email_attendance.iloc[:3])
print(email_registered.iloc[:3])

generator = Generator(template_filepath='templates/CERTIFICATE OF PARTICIPANT.pdf',
                      use_qrcode=True, qr_logo_path='imgs/dsc_mask.png')

CERTIFICATE_CODE = 'MYML041221'
for i, row in attendance.sample(5).iterrows():
    generator.generate(row['Full Name'], utils.create_code(CERTIFICATE_CODE, i+1))

# TODO:
# demonstrate certificate generation
# - Participant: Filter participants who both registered and attended the event 
# - Participant: Add Tamu Undangan


