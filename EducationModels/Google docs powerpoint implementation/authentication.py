import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/presentations']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file('C:\\Users\\david\\Desktop\\AlgoCo\\Private Education Models\\EdukaiPrivateModels\\credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)  # This will open a web page for authentication
    service = build('slides', 'v1', credentials=creds)
    return service