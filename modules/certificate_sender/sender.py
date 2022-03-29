import pandas as pd
from tqdm import tqdm

from modules.certificate_generator.generator import Generator
from modules.certificate_generator import utils
from modules.google_api.google_api import GoogleAPI
from modules.google_api.utils import get_certificate_info

class Sender:
    def __init__(self, folder_id, client_secret_path='secrets/client_secret.json') -> None:
        self.api = GoogleAPI(folder_id=folder_id,
                client_secret_path=client_secret_path)
