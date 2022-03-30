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

    def get_data_templates(self):
        template_folders = self.get_data_templates_folders()
        data_templates = {}
        for folder_name in template_folders:
            data_templates[folder_name] = self.get_data_template_components(folder_name)
        return data_templates
            

    def get_data_template_components(self, folder_name):
        data_path = os.path.join('data', folder_name)
        component_filenames = os.listdir(data_path)

        # filter components by extension
        recipients = list(filter(lambda x: os.path.splitext(x)[1] == '.csv', component_filenames))
        message = list(filter(lambda x: os.path.splitext(x)[1] == '.txt', component_filenames))
        certificate = list(filter(lambda x: os.path.splitext(x)[1] == '.pdf', component_filenames))
        if len(certificate) == 0:
            certificate = list(filter(lambda x: os.path.splitext(x)[1] == '.png', component_filenames))

        components = {
            'recipient': recipients,
            'message': message,
            'certificate': certificate,
        }

        # check if required components are valid
        components = self.validate_components(folder_name, components)
        return components

            

    def get_data_templates_folders(self):
        data_templates = os.listdir('data')
        data_templates = list(filter(lambda x: x[0]!='.', data_templates))
        return data_templates

#     def setup_certificate_folders(self):
#         for folder_name in os.listdir('data'):
#             data_path = os.path.join('data', folder_name)
#             if os.path.isdir(data_path):
#                 print(os.listdir(data_path))
