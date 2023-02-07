import os
import uuid
from flask import Flask, request, jsonify, send_file
from PIL import Image
from flask_cors import CORS
import platform

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    # load_dotenv()
    return jsonify({"status" : "running"})

@app.route("/loadenv")
def loadenv():
    # load_dotenv()
    return jsonify({"status" : "running"})



def compress_image(image_path, output_path, percentage):
    original_image = Image.open(image_path)
    width, height = original_image.size
    new_width = int(width * (percentage / 100))
    new_height = int(height * (percentage / 100))
    compressed_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
    compressed_image.save(output_path, optimize=True)
    return new_width, new_height

@app.route("/compress", methods=["POST"])
def compress():
    ROOT_IMAGE_PATH = "images"
    ROOT_COMPRESSED_PATH = "compressed_images"
    DOWNLOAD_URL = "http://localhost:5000"
    system_name = platform.system()
    if system_name == "Linux":
        ROOT_IMAGE_PATH="/var/www/html/images"
        ROOT_COMPRESSED_PATH="/var/www/html/compressed_images"
        DOWNLOAD_URL="https://toolsapi.lctopc.com"
    else:
        pass
        
    image = request.files.get("image")
    percentage = int(request.form.get("percentage"))
    unique_filename = str(uuid.uuid4()) + "_" + image.filename
    image_path = os.path.join(ROOT_IMAGE_PATH, unique_filename)
    image.save(image_path)
    output_filename = f"compressed_{unique_filename}"
    output_path = os.path.join(ROOT_COMPRESSED_PATH, output_filename)
    newwidth, newheight = compress_image(image_path, output_path, percentage)
    size = os.path.getsize(os.path.join(ROOT_COMPRESSED_PATH, output_filename))
    download_link = f"{DOWNLOAD_URL}/download/{output_filename}"
    return jsonify({"download_link": download_link, "info" : size})

@app.route("/download/<filename>")
def download(filename):
    ROOT_IMAGE_PATH = "images"
    ROOT_COMPRESSED_PATH = "compressed_images"
    DOWNLOAD_URL = "http://localhost:5000"
    system_name = platform.system()
    if system_name == "Linux":
        ROOT_IMAGE_PATH="/var/www/html/images"
        ROOT_COMPRESSED_PATH="/var/www/html/compressed_images"
        DOWNLOAD_URL="https://toolsapi.lctopc.com"
    else:
        pass
    return send_file(os.path.join(ROOT_COMPRESSED_PATH, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
