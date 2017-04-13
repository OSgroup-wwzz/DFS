import os
from os import listdir
from os.path import isfile, join

from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
if not os.path.exists('uploads'):
    os.makedirs('uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("ERROR: no selected file")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("ERROR: no selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download'))
    else:
        return render_template('upload.html')


@app.route('/download')
def download():
    return render_template('download.html', filelist=[f for f in listdir('uploads') if isfile(join('uploads', f))])


@app.route('/download_file/<filename>')
def download_file(filename):
    return send_file('uploads/{}'.format(filename))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
