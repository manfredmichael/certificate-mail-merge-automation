import os
from tqdm import tqdm
import pandas as pd

from modules.certificate_generator.generator import Generator
from modules.certificate_generator import utils
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

class Sender:
    def __init__(self, folder_id, client_secret_path='secrets/client_secret.json') -> None:
        # self.api = GoogleAPI(folder_id=folder_id,
        #         client_secret_path=client_secret_path)
        self.setup_certificate_folders()

    def generate_certificate(self):
        generator = Generator(template_filepath='templates/monthly/CERTIFICATE OF SPEAKER_TTD.pdf',
                              name=(435, 72),
                              code=(72, 262, 25),
                              qrcode =(60, 340),
                              font='OpenSans-SemiBold.ttf',
                              use_qrcode=True,
                              output='certificates/techtalk-speaker',
                              qr_logo_path='imgs/dsc_mask.png')

    def setup_certificate_folders(self):
        for folder_name in os.listdir('data'):
            data_path = os.path.join('data', folder_name)
            if os.path.isdir(data_path):
                print(os.listdir(data_path))
