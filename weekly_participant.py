import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/weekly/CERTIFICATE OF PARTICIPATION - WEEK 123.pdf',
                      name=(510, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      output='certificates/weekly-peserta',
                      qr_logo_path='imgs/dsc_mask.png')


# Load recipients data
recipients = pd.read_csv('data/Weekly21 - Participant')

# Setup certificate code
CERTIFICATE_CODE = 'WYML191121PT'
START_CERTIFICATE_NO = 1

print(f'{len(recipients)} certificates will be generated')

result_df = [] 
for i, row in tqdm(recipients.iterrows(), total=len(recipients)):
    certificate_code = create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    generator.generate(row['Name'], certificate_code)
    certificate_info = get_certificate_info(name=row['Name'],
                                            code=certificate_code,
                                            type='Participant',
                                            url='',
                                            date_published='4 December 2021',
                                            valid_until='Forever')
    result_df.append(certificate_info)
pd.DataFrame(result_df).to_csv('certificates/weekly-peserta/result.csv')

# TODO:
# - Participant: Add Tamu Undangan


