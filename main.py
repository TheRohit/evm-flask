from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from functools import wraps
import os
from app import process_video  # Make sure to import your processing function

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and api_key == os.getenv('API_KEY'):
            return f(*args, **kwargs)
        else:
            abort(401, description="Invalid or missing API Key")
    return decorated_function

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@require_api_key
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded video file
        heart_rate = process_video(file_path)
        
        # Cleanup or handle the video file as needed
        
        return jsonify({'heart_rate': heart_rate})

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == "__main__":

    port = int(os.getenv('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
