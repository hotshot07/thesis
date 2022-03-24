import os
from flask import Flask, request
from werkzeug.utils import secure_filename

FILE_FOLDER = './received_csv_files'

app = Flask(__name__)
app.config['FILE_FOLDER'] = FILE_FOLDER

@app.route('/file', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['uploaded_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['FILE_FOLDER'], filename))
    return 'file-received'

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000)