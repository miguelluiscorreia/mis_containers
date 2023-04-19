from flask import Flask, render_template
import os


app = Flask(__name__)
app.config['UPLOADS_DIR'] = '/uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/health-check')
def health_check():
    result = os.system('curl http://app')
    if result == 0:
        return 'App Up'
    else:
        return 'App Down'


@app.route('/interfaces-status')
def int_status():
    for fpath in os.listdir(app.config['UPLOADS_DIR']):
        tmp_path = os.path.join(app.config['UPLOADS_DIR'], fpath)
        if os.path.isfile(tmp_path):
            with open(tmp_path, 'r') as f:
                with open('/uploads/results_' + fpath, 'w') as fw:
                    lines = f.readlines()
                    for line in lines:
                        result = os.system('ping -c 2 ' + line)
                        if result == 0:
                            fw.write('IP: ' + line + ' Status: UP')
                        else:
                            fw.write('IP: ' + line + ' Status: DOWN')
        return 'Success'
    return 'No files'


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)

