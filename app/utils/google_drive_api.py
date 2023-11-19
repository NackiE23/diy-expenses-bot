import io
import random

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config import SERVICE_ACCOUNT_FILE, SCOPES


def authenticate():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)


def list_files(service, folder_name):
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    return results.get('files', [])


drive_service = authenticate()
wallpaper_directory_id = list_files(drive_service, "обои")[0]["id"]


def get_random_subdirectory(service, parent_folder_id):
    results = service.files().list(
        q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()

    subdirectories = results.get('files', [])
    return random.choice(subdirectories)['id'] if subdirectories else None


def get_random_image(service, subdirectory_id):
    results = service.files().list(
        q=f"'{subdirectory_id}' in parents and mimeType='image/jpeg'",
        fields="files(id, name)"
    ).execute()

    images = results.get('files', [])
    return random.choice(images) if images else None


def download_image_bytes(service, file_id):
    request = service.files().get_media(fileId=file_id)
    image_bytes = io.BytesIO()
    downloader = MediaIoBaseDownload(image_bytes, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    image_bytes.seek(0)  # Move the cursor to the beginning of the bytes buffer
    return image_bytes


def get_random_google_drive_image():
    random_subdirectory_id = get_random_subdirectory(drive_service, wallpaper_directory_id)
    random_image = get_random_image(drive_service, random_subdirectory_id)
    return download_image_bytes(drive_service, random_image['id']), random_image['name']
