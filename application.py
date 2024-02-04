from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from main import process_video  # Make sure to import your processing function

application = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded video file
        heart_rate = process_video(file_path)
        
        # Cleanup or handle the video file as needed
        
        return jsonify({'heart_rate': heart_rate})

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    application.run(debug=False, port=5000)
