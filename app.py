from flask import Flask, render_template, request
import os
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

notes = []

# Get the connection string from environment variable
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not connection_string:
    logger.error("Error: Connection string not found")

# Initialize the BlobServiceClient with the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Access the 'static' container in Azure Blob Storage
try:
    static_container_client = blob_service_client.get_container_client('static')
    static_container_client.create_container()
except Exception as e:
    logger.error(f"Container 'static' couldn't be created: {e}")

# Access the 'uploads' container for user-uploaded notes
try:
    uploads_container_client = blob_service_client.get_container_client('uploads')
    uploads_container_client.create_container()
except Exception as e:
    logger.error(f"Container 'uploads' couldn't be created: {e}")

# Define the path to the mounted file share
MOUNT_PATH = '/mnt/myfileshare'

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        if note:
            notes.append(note)
            blob_client = uploads_container_client.get_blob_client(f"note_{len(notes)}.txt")
            blob_client.upload_blob(note, overwrite=True)
            save_note_to_file(note)
    return render_template("home.html", notes=notes)

def save_note_to_file(note):
    try:
        os.makedirs(MOUNT_PATH, exist_ok=True)
        with open(os.path.join(MOUNT_PATH, 'notes.txt'), 'a') as f:
            f.write(note + '\n')
    except Exception as e:
        logger.error(f"Error saving note: {e}")

if __name__ == '__main__':
    # For production, use gunicorn instead of Flask's built-in server
    # app.run(debug=True) # Comment this out in production
    pass
