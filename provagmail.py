from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
import json

# Leggi le credenziali dal file JSON
with open('credentials.json', 'r') as f:
    credentials_info = json.load(f)
print(credentials_info)
#prendi solo le credenziali client_id, client_secret, refresh_token
credentials_info = credentials_info['installed']
print(credentials_info)

# Definisci gli scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Crea le credenziali
creds = Credentials.from_authorized_user_info(info=credentials_info, scopes=SCOPES)

# Crea l'oggetto Gmail API
service = build('gmail', 'v1', credentials=creds)

try:
    # Prendi le email dalla tua inbox
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print('Non ci sono messaggi.')
    else:
        print('Ultimi 5 messaggi:')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload['headers']
            for header in headers:
                if header['name'] == 'Subject':
                    subject = header['value']
                if header['name'] == 'From':
                    sender = header['value']
                if header['name'] == 'Date':
                    date = header['value']
            print(f"Da: {sender}\nData: {date}\nOggetto: {subject}\n\n")

except HttpError as error:
    print(f'An error occurred: {error}')