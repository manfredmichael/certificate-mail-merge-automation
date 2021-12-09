import pandas as pd
from tqdm import tqdm

from certificate_generator.generator import Generator
from certificate_generator import utils


# Configure name, certificate code & qrcode positions
generator = Generator(template_filepath='templates/weekly/CERTIFICATE OF COMPLETION - merged.pdf',
                      name=(510, 72),
                      code=(72, 262, 25),
                      qrcode =(60, 340),
                      font='OpenSans-SemiBold.ttf',
                      use_qrcode=True,
                      output='certificates/weekly-completion',
                      qr_logo_path='imgs/dsc_mask.png')


# Load recipients data
recipients = pd.read_csv('data/Weekly21 - Completion')

# Setup certificate code
CERTIFICATE_CODE = 'WYML191121CP'
START_CERTIFICATE_NO = 1

print(f'{len(recipients)} certificates will be generated')

result_df = [] 
for i, row in tqdm(recipients.iterrows(), total=len(recipients)):
    certificate_code = utils.create_code(CERTIFICATE_CODE,
                                         START_CERTIFICATE_NO+i)
    generator.generate(row['Name'], certificate_code)
    result_df.append([row['Username'], row['Name'], certificate_code])
pd.DataFrame(result_df).to_csv('certificates/weekly-completion/result.csv')

# TODO:
# - Participant: Add Tamu Undangan


