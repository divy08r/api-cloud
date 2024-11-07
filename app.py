from flask import Flask, request, jsonify
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
try:
    os.makedirs(app.config['UPLOAD_FOLDER'])
except OSError:
    pass

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # print("Request files:", request.files) 
        file = request.files.get('audio')
        
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            dest = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(dest)
            
            api_url = "https://getpredictions-zwofr6ivcq-et.a.run.app/"
            with open(dest, 'rb') as saved_file:
                files = {'audio': (file.filename, saved_file, 'audio/mpeg')}
                response = requests.post(api_url, files=files)
                response.raise_for_status()  

            os.remove(dest) 

            return jsonify(response.json())  
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
