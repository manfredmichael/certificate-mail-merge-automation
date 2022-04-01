import os
from tqdm import tqdm
import pandas as pd
from colorama import Fore, Style

from modules.certificate_generator.generator import Generator
from modules.certificate_generator.utils import create_code
from modules.certificate_generator import utils
from modules.certificate_sender import errors 
from modules.certificate_sender.utils import remove_class
import os

from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

class Sender:
    def __init__(self, folder_id, client_secret_path='secrets/client_secret.json') -> None:
        pass
        self.api = GoogleAPI(folder_id=folder_id,
                client_secret_path=client_secret_path)
        self.data_templates = self.get_data_templates() 
        
    def send_all(self, confirm_mode=True):
        for folder_name, data_template in self.data_templates.items():
            self.send(folder_name, data_template, confirm_mode)

    def send(self, folder_name, data_template, confirm_mode):
        self.api.set_gmaiL_logger(folder_name)

        data_path = os.path.join('data', folder_name) 
        certificate_output_path = os.path.join('certificates', folder_name) 

        subject, content = self.parse_message(os.path.join(data_path, data_template['message']))

        # Load recipients data
        recipients = pd.read_csv(os.path.join(data_path, data_template['recipient']))
        recipients['Name'] = recipients['Name'].apply(remove_class)

        for i, row in recipients.iterrows():
            if i >=5 and confirm_mode:
                confirm_mode = self.confirm_to_continue()

            certificate_path = os.path.join(certificate_output_path, row['Name'].upper() + '.pdf')
            self.api.send_certificate(row['Email'], subject, content.replace('[NAME]', row['Name'].strip()), certificate_path)

    def confirm_to_continue(self):
        print(Fore.YELLOW+ 'Some emails have been sent. Before we continue, please confirm there was not any mistake (y/N):' + Style.RESET_ALL, end='')
        confirm = input().lower() == 'y'
        if not confirm:
            exit()
        return False    # return confirm_mode as false
    
    def parse_message(self, filepath):
        message = open(filepath).readlines()
        subject = list(filter(lambda x: x.split(':')[0] == 'SUBJECT', message))
        content = list(filter(lambda x: x.split(':')[0] != 'SUBJECT', message))
        if len(subject)==0:
            subject = 'Certificate'
        else:
            subject = subject[0].replace('SUBJECT:', '').strip()

        content = ''.join(content)
        return subject, content 

    def generate_all(self):
        for folder_name, data_template in self.data_templates.items():
            self.generate(folder_name, data_template)

    def generate(self, folder_name, data_template):
        data_path = os.path.join('data', folder_name) 
        certificate_output_path = os.path.join('certificates', folder_name) 

        if not os.path.isdir(certificate_output_path):
            os.makedirs(certificate_output_path)

        # Configure name, certificate code & qrcode positions
        generator = Generator(template_filepath=os.path.join(data_path, data_template['certificate']),
                              name=(510, 72),
                              code=(72, 262, 25),
                              qrcode =(60, 340),
                              font='OpenSans-SemiBold.ttf',
                              use_qrcode=True,
                              # qr_logo_path='imgs/dsc_mask.png'),
                              output=os.path.join('certificates', folder_name))

        # Load recipients data
        recipients = pd.read_csv(os.path.join(data_path, data_template['recipient']))
        recipients['Name'] = recipients['Name'].apply(remove_class)

        result_df = []
        for i, row in tqdm(recipients.iterrows(), total=len(recipients)):
            certificate_code = create_code(data_template['code'], i)
            certificate_path = generator.generate(row['Name'], certificate_code)
            certificate_url = self.api.upload_certificate_to_drive(certificate_path, data_template['folder_id'])
            certificate_info = get_certificate_info(name=row['Name'],
                                            code=certificate_code,
                                            url=certificate_url,
                                            valid_until='Forever')
            result_df.append(certificate_info)
        pd.DataFrame(result_df).to_csv(os.path.join(certificate_output_path, 'result.csv'))

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
        code = list(filter(lambda x: os.path.splitext(x)[1] == '.code', component_filenames))
        certificate = list(filter(lambda x: os.path.splitext(x)[1] == '.pdf', component_filenames))
        if len(certificate) == 0:
            certificate = list(filter(lambda x: os.path.splitext(x)[1] == '.png', component_filenames))

        components = {
            'recipient': recipients,
            'message': message,
            'certificate': certificate,
            'code': code,
            'folder_id': [self.api.create_folder(folder_name)]
        }

        # check if required components are valid
        components = self.validate_components(folder_name, components)
        return components

    def validate_components(self, folder_name, components):
        for component_name, value in components.items():
            if len(value) > 1:
                raise errors.DuplicateComponent(folder_name, component_name) 
            if len(value) == 0:
                raise errors.RequiredComponentNotExist(folder_name, component_name) 

        components = {
            'recipient': components['recipient'][0],
            'message': components['message'][0],
            'certificate': components['certificate'][0],
            'code': os.path.splitext(components['code'][0])[0],
            'folder_id': components['folder_id'][0]
        }
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
