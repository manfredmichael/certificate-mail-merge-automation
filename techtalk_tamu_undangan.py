import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

# Initialize Gooogle API & configure folder id to store certificates remotely
api = GoogleAPI(folder_id='1gf1zE_pvJf2AgC52rrKQkgN8kWhPC36Z',
                client_secret_path='secrets/client_secret.json')

# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/monthly/CERTIFICATE OF PARTICIPANT_TTD.pdf',
                      name=(435, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      output='certificates/techtalk-tamu_undangan',
                      qr_logo_path='imgs/dsc_mask.png')


# Load recipients data
recipients = open('data/monthly/tamu_undangan.txt').readlines()

# Setup certificate code
CERTIFICATE_CODE = 'MYWDL190222PT'
START_CERTIFICATE_NO = 83 

print(f'{len(recipients)} certificates will be generated')

result_df = [] 
for i, name in tqdm(enumerate(recipients), total=len(recipients)):
    certificate_code = create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    certificate_path = generator.generate(name, certificate_code)

    certificate_url = api.upload_certificate_to_drive(certificate_path)
    certificate_info = get_certificate_info(name=name,
                                            code=certificate_code,
                                            type='Tamu Undangan',
                                            url=certificate_url,
                                            date_published='20 February 2022',
                                            valid_until='Forever')
    result_df.append(certificate_info)
pd.DataFrame(result_df).to_csv('certificates/techtalk-tamu_undangan/result.csv')
