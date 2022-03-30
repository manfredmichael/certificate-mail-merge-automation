import os
from tqdm import tqdm
import pandas as pd

from modules.certificate_generator.generator import Generator
from modules.certificate_generator import utils
from modules.certificate_sender import errors 
import os

from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

class Sender:
    def __init__(self, folder_id, client_secret_path='secrets/client_secret.json') -> None:
        pass
        # self.api = GoogleAPI(folder_id=folder_id,
        #         client_secret_path=client_secret_path)

    def generate_all(self):
        data_templates = self.get_data_templates() 
        print(data_templates)

#     def setup_certificate_folders(self):
#         for folder_name in os.listdir('data'):
#             data_path = os.path.join('data', folder_name)
#             if os.path.isdir(data_path):
#                 print(os.listdir(data_path))
