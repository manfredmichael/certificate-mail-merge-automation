# import certificate_generator 
from google_api_module import GoogleAPI
import pandas as pd
import utils
import os
import json
import time


EMAIL_SUBJECT = 'Google DSC Universitas Gunadarma Presents'

SEND_EVERY = 5 # seconds

api = GoogleAPI(docs_id='13efuqWFc9Y2OE7795zgl35fu2ZM9hF-kH9iuvHqlBlM',
                sheets_id='11tWWn8wuZP_lxBMBPoMaJFb2pnKasfq9iyJY52mRlBg',
                folder_id='')
api.load_services('secrets/client_secret.json')



def main():
    while True:
        if not os.path.isfile('data/state.json'):
            with open('data/state.json','w') as f:
                f.write(json.dumps({'EMAIL_SENT':[]}, indent=2))

        with open('data/state.json','r') as f:
            state = json.load(f)

        # with open(EMAIL_TEMPLATE_PATH, 'r') as f:
        #     email_template = '\n'.join(f.readlines())

        member_regist = api.get_responses('Member Regist')

        # no filter is applied
        filtered_response = member_regist.copy().iloc[100:101]
        print(filtered_response.shape)
        print(filtered_response.head())

        for i, record in filtered_response.iterrows():
            email = record['Email address']
            name = record['Nama Lengkap']
            if email in state['EMAIL_SENT']:
                continue

            # writing email
            print('Sending to {}: '.format(name), end='')
            # try:
                # api.send_certificate(email=email,
                #                      subject=EMAIL_SUBJECT,
                #                      message_text=message_text,
                #                      certificate_path=certificate_path)
            # api.send_templated_email(email=email,
            #                          subject=EMAIL_SUBJECT)

            print('Success')
            utils.add_email_log(email)
            state['EMAIL_SENT'].append(email)
            # except Exception as e:
                # print('An error occurred: {}'.format(e))

        with open('data/state.json','w') as f:
            f.write(json.dumps(state, indent=2))

        utils.wait(SEND_EVERY)


if __name__ == '__main__':
    main()

