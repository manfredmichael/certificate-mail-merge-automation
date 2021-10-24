import certificate_generator 
from google_api_module import GoogleAPI
import pandas as pd
import utils
import os
import json
import time


EMAIL_TEMPLATE_PATH = 'data/email.txt'
EMAIL_SUBJECT = 'GDSC UG INFO SESSION 2021 CERTIFICATE'

CERTIFICATE_CODE = 'IFSN[DATE][MONTH][YEAR][TYPE][NO]'
CERT_TYPE_CODE = 'PT'
CERT_TYPE = 'Participation'
FONT = 'OpenSans-SemiBold.ttf'

SEND_EVERY = 5 # seconds

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
    for i in range(SEND_EVERY):
        print('Sending in {} seconds '.format(SEND_EVERY-i), end='\r', flush=True)
        time.sleep(1)
    print(' '.join([' ' for i in range(20)]), end='\r', flush=True)

    while True:
        if not os.path.isfile('data/state.json'):
            with open('data/state.json','w') as f:
                f.write(json.dumps({'EMAIL_SENT':[], 'CURRENT_CERT_NO':1}, indent=2))

        with open('data/state.json','r') as f:
            state = json.load(f)

        with open(EMAIL_TEMPLATE_PATH, 'r') as f:
            email_template = '\n'.join(f.readlines())

        registration = api.get_responses('data bervy')
        feedback = api.get_responses('feedback')

        # filter attendees who filled both forms
        filtered_response = feedback.merge(registration, 
                                           left_on='Email address',
                                           right_on='confirm your email')
        filtered_response['Timestamp'] = pd.to_datetime(filtered_response['Timestamp'])

        for i, record in filtered_response.head(1).iterrows():
            email = record['Email address']
            name = record['Name']
            if email in state['EMAIL_SENT']:
                continue

            i = state['CURRENT_CERT_NO']

            code = utils.create_code(date_time=record['Timestamp'], 
                                     cert_type=CERT_TYPE_CODE,
                                     cert_no=i+1,
                                     base=CERTIFICATE_CODE)
            certificate_path = generator['PARTICIPANT'].generate(name, 
                                                                 code,
                                                                 qr_logo='imgs/dsc_mask.png')
            certificate_url = api.upload_certificate(certificate_path)
            api.add_certificate_log(code=code, 
                                    name=name,
                                    cert_type=CERT_TYPE,
                                    valid_until='Forever',
                                    url=certificate_url,
                                    worksheet='sertifikat web')


            # writing email
            print('Sending to {}'.format(name))
            try:
                message_text = email_template.replace('[NAME]', name)
                api.send_certificate(email=email,
                                     subject=EMAIL_SUBJECT,
                                     message_text=message_text,
                                     certificate_path=certificate_path)
                utils.add_email_log(email)
                state['EMAIL_SENT'].append(email)
                state['CURRENT_CERT_NO'] += 1
            except Exception as e:
                print('An error occurred: {}'.format(e))


        with open('data/state.json','w') as f:
            f.write(json.dumps(state, indent=2))


if __name__ == '__main__':
    main()

