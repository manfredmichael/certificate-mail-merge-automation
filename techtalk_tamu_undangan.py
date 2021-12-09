import pandas as pd
from tqdm import tqdm

from certificate_generator.generator import Generator
from certificate_generator import utils


# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/techtalk/CERTIFICATE OF PARTICIPANT.pdf',
                      name=(435, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      output='certificates/techtalk-tamu_undangan',
                      qr_logo_path='imgs/dsc_mask.png')


# Load recipients data
recipients = open('data/tamu_undangan.txt').readlines()

# Setup certificate code
CERTIFICATE_CODE = 'MYML041221PT'
START_CERTIFICATE_NO = 107 

print(f'{len(recipients)} certificates will be generated')

result_df = [] 
for i, name in tqdm(enumerate(recipients), total=len(recipients)):
    certificate_code = utils.create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    generator.generate(name, certificate_code)
    result_df.append([name, certificate_code])
pd.DataFrame(result_df).to_csv('certificates/techtalk-tamu_undangan/result.csv')

# TODO:
# - Participant: Add Tamu Undangan


