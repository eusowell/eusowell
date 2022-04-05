from __future__ import print_function

import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import generate


SERVICE_ACCOUNT_FILE = 'signature-corporate.json'
# If modifying these scopes, delete the file token.json.
SCOPES = [' https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.settings.basic'
          ]



def validation_service(user_email):
    # Set the crendentials
    credentials = service_account.Credentials.\
        from_service_account_file(SERVICE_ACCOUNT_FILE, scopes= SCOPES)
    # Delegate the credentials to the user you want to impersonate
    delegated_credentials = credentials.with_subject(user_email)
    service = build('gmail', 'v1', credentials=delegated_credentials)
    return service



def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    with open('data.json', 'r') as fp:
        data = json.load(fp)

    for d in data:
        print(d['primaryEmail'])
        # The user we want to "impersonate"
        u_s_e_r__e_m_a_i_l = d['primaryEmail']


        try:
            # Call the Gmail API
            service = validation_service(user_email=u_s_e_r__e_m_a_i_l)
            primary_alias = None
            aliases = service.users().settings().sendAs().\
                list(userId=u_s_e_r__e_m_a_i_l).execute()
            for alias in aliases.get('sendAs'):
                if alias.get('isPrimary'):
                    primary_alias = alias
                    break
            file = open(generate.gera_html(u_s_e_r__e_m_a_i_l), 'r')
            htmlfile = file.read()
            send_as_configuration = {
                'signature': htmlfile
            }
            service.users().settings().sendAs().\
                patch(userId=u_s_e_r__e_m_a_i_l,
                      sendAsEmail=primary_alias.get('sendAsEmail'),
                      body=send_as_configuration).execute()

            print(f'Updated signature for: {d["name"]["fullName"]}\n')

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
