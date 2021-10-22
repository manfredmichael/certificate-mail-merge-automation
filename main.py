import certificate_generator 
from google_api_module import GoogleAPI
import pandas as pd

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
    # filter attendees who filled both forms
    registration = api.get_responses('data bervy')
    feedback = api.get_responses('feedback')
    filtered_response = feedback.merge(registration, 
                                       left_on='Email address',
                                       right_on='confirm your email')
    print(filtered_response)
    


if __name__ == '__main__':
    main()

