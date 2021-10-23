import certificate_generator 
from google_api_module import GoogleAPI
import pandas as pd
import utils

CERTIFICATE_CODE = 'IFSN[DATE][MONTH][YEAR][TYPE][NO]'
CERT_TYPE = 'PT'
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
        name = record['Name']
        code = utils.create_code(date_time=record['Timestamp'], 
                                 cert_type=CERT_TYPE,
                                 cert_no=i+1,
                                 base=CERTIFICATE_CODE)
        certificate_path = generator['PARTICIPANT'].generate(name, 
                                                             code,
                                                             qr_logo='imgs/dsc_mask.png')
        certificate_url = api.upload_certificate(certificate_path)
        api.add_certificate_log(code=code, 
                                name=name,
                                cert_type='Participation',
                                valid_until='Forever',
                                url=certificate_url,
                                worksheet='sertifikat web')
        print(certificate_url)
        print(certificate_path)
        print(name)

    


if __name__ == '__main__':
    main()

