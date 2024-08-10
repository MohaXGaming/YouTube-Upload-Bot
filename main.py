import os
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http

# Path to the file you want to upload
video_file = "mondays.mp4"

# Scopes required for the API
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

# Authentication and initialization
try:
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", scopes)
    credentials = flow.run_local_server(port=8080)
except Exception as e:
    print(f"Error during authentication: {e}")
    exit()

try:
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    # Metadata for the video
    request_body = {
        "snippet": {
            "title": "Monday Monkey Lives For The Weekend, Sir",
            "description": "Monday Monkey Lives For The Weekend, Sir. Not Affiliated with Fox, Hulu or Disney!",
            "tags": ["futurama"],
            "categoryId": "24"  # Category ID for 'Entertainment'
        },
        "status": {
            "privacyStatus": "public",  # Set to "private" or "unlisted" as needed
        }
    }

    # Uploading the video
    media = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload complete: https://www.youtube.com/watch?v={response['id']}")
except googleapiclient.errors.HttpError as e:
    print(f"An error occurred: {e}")
