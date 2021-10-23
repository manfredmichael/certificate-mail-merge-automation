import certificate_generator 
from google_api_module import GoogleAPI
import pandas as pd
from datetime import datetime

CERTIFICATE_CODE = 'IFSN[DATE][MONTH][YEAR][TYPE][NO]'
FONT = 'OpenSans-SemiBold.ttf'

generator ={
    'COMITTEE':certificate_generator.Generator("templates/CERTIFICATE OF COMITTEE.pdf", font=FONT),
    'PARTICIPANT':certificate_generator.Generator("templates/CERTIFICATE OF PARTICIPANT.pdf", font=FONT),
    'SPEAKER':certificate_generator.Generator("templates/CERTIFICATE OF SPEAKER.pdf", font=FONT)
}

api = GoogleAPI(docs_id='',
                sheets_id='1jvYAJhFDJ1Kgo1hbb5jrYfnyUOykx9gg6VwgfsOM3LM',
                folder_id='1UjC4TfKLCwMYxPRckqN_I0b6BUaERLJe')
api.load_services('secrets/client_secret.json')



def main():
    registration = api.get_responses('data bervy')
    feedback = api.get_responses('feedback')

    # filter attendees who filled both forms
    filtered_response = feedback.merge(registration, 
                                       left_on='Email address',
                                       right_on='confirm your email')
    filtered_response['Timestamp'] = pd.to_datetime(filtered_response['Timestamp'])


    for i, record in filtered_response.head(1).iterrows():
        code = create_code(record['Timestamp'], 'PT',i+1)
        name = record['Name']
        certificate_path = generator['PARTICIPANT'].generate(name, code, qr_logo='imgs/dsc_mask.png')
        api.upload_certificate(certificate_path)
        print(certificate_path)
        print(name)

# create certificate code
def create_code(date_time, cert_type, no):
    dd = date_time.strftime('%d')
    mm = date_time.strftime('%m')
    yy = date_time.strftime('%y')
    code = CERTIFICATE_CODE.replace('[DATE]', dd)\
                           .replace('[MONTH]', mm)\
                           .replace('[YEAR]', yy)\
                           .replace('[TYPE]', cert_type)\
                           .replace('[NO]', str(no).zfill(3))\

    return code
    


if __name__ == '__main__':
    main()

