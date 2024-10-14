from flask import Flask, render_template, request
import os
from azure.storage.blob import BlobServiceClient

app = Flask(__name__, static_url_path='/static')

notes = []

# Get the connection string from environment variables
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Initialize the BlobServiceClient with the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Access the 'static' container in Azure Blob Storage
static_container_client = blob_service_client.get_container_client('static')

# Access the 'uploads' container for user-uploaded notes
uploads_container_client = blob_service_client.get_container_client('uploads')

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        if note:
            # Append the note to the local list
            notes.append(note)

            # Save the note to Blob Storage in the 'uploads' container
            blob_client = uploads_container_client.get_blob_client(f"note_{len(notes)}.txt")  # Use the note index as part of the filename
            blob_client.upload_blob(note, overwrite=True)  # Upload the note content as a blob

    return render_template("home.html", notes=notes)

if __name__ == '__main__':
    app.run(debug=True)
