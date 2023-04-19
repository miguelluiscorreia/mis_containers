from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/uploads/' + filename)
        return 'File type not allowed. Allowed file types are: ' + str(app.config['ALLOWED_EXTENSIONS'])
    return '''
    <!doctype html>
    <title>Upload IPs list</title>
    <h1>Upload file:</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if filename:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return 'If you are looking for the final results of the scan the file should be status_results.txt!'


@app.route('/check-status/<filename>')
def check_status(filename):
    tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.isfile(tmp_path):
        with open(tmp_path, 'r') as f:
            with open('uploads/status_results.txt', 'w') as fw:
                lines = f.readlines()
                for line in lines:
                    result = os.system('curl ' + line)
                    if result == 0:
                        fw.write('Service: ' + line + ' Status: UP')
                    else:
                        fw.write('Service: ' + line + ' Status: DOWN')
    else:
        return 'File does not exist!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)

