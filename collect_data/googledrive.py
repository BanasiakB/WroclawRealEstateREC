import os, io
import requests
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import numpy as np
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload


# Pomysł:
# Przechowywanie zdjęć w formacie: ID_MIESZKANIA + '_' + Numer_ZDJ + '.jpg'
# Wtedy pobieranie przez prefix ID_MIESZKANIA + '_'


SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = "1nAdxeZ98GtQKwN8lnidOLFkZobtU54xz"
CREDS_FILE = 'service_account.json'
API_KEY = 'AIzaSyC_1qWSpnANQf9ZcNn9yL5TfhRdwoarApU'
DESTINATION_FOLDER = 'images'
IMG_EXTENTION = '.jpeg'

class UploadError(Exception):
    """Exception raised when an upload to Google Drive fails."""

    def __init__(self, message="Upload to Google Drive failed."):
        self.message = message
        super().__init__(self.message)
        
def authenticate():
    creds = service_account.Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_image(file_path, name):
    service = authenticate()
    file_metadata = {
        'name': f'{name}',
        'parents': [FOLDER_ID]
    }

    service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

def upload_image_to_drive(image_url: str, name: str) -> None:
    service = authenticate()

    response = requests.get(image_url)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to get image from {image_url}. Status code: {response.status_code}")

    file_metadata = {
        'name': f'{name}',
        'parents': [FOLDER_ID]
    }
    media = MediaIoBaseUpload(io.BytesIO(response.content), mimetype='image/jpeg')
    service.files().create(body=file_metadata, media_body=media).execute()


######################## Poniższe mogą się przydać później przy tworzeniu modeli ################
def download_image_from_drive(file_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    photo = service.files().get_media(fileId=f'{FOLDER_ID}\\'+file_id)

def list_images_in_drivefolder() -> list[str]:
    service = authenticate()
    results = service.files().list(q=f"'{FOLDER_ID}' in parents and mimeType='image/jpeg'",
                                   fields="files(name, id)").execute()
    items = results.get('files', [])

    if not items:
        raise ImportError('No image files found.')
    return [item['name'] for item in items]

def list_ids_from_images_in_drivefolder() -> list[str]:
    return [image_name.split('_')[0] for image_name in list_images_in_drivefolder()]

def download_images_from_drive_with_prefix(prefix):
    service = authenticate()

    results = service.files().list(q=f"'{FOLDER_ID}' in parents and mimeType='image/jpeg' and name contains '{prefix}'",
                                   fields="files(name, id)").execute()
    
    items = results.get('files', [])

    if not items:
        print(f'No image files found with prefix "{prefix}".')
    else:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            request = service.files().get_media(fileId=file_id)
            destination_path = os.path.join(DESTINATION_FOLDER, file_name + IMG_EXTENTION)
            with open(destination_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                    
