from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Specifica gli ambiti richiesti
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Crea il flusso di autorizzazione
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)

# Autorizza l'accesso all'account Google dell'utente
creds = flow.run_local_server(port=0)

# Crea un'istanza del client Gmail API
service = build('gmail', 'v1', credentials=creds)

# Esegui la richiesta per ottenere le email della casella di posta in arrivo
results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
messages = results.get('messages', [])

# Se ci sono email nella casella di posta in arrivo, restituisci il link dell'ultima email
if messages:
    message_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    link = message['payload']['headers'][24]['value']
    print('Link ultima email:', link)
else:
    print('Nessuna email trovata.')