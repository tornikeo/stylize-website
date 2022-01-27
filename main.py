from flask import Flask
from flask import request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from model_and_weights.Eval import Stylizer


UPLOAD_FOLDER = Path('uploads')
GEN_FOLDER = Path('generated')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GEN_FOLDER'] = GEN_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = Stylizer()

def save_file_from_request(name):
    # check if the post request has the file part
    # if 'file' not in request.files:
    #     flash('No file part')
    #     return redirect(request.url)
    file = request.files[name]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    # if file.filename == '':
    #     flash('No selected file')
    #     return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return path
 
import matplotlib.pyplot as plt

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # content_path = 'uploads/chicago.jpg'#save_file_from_request('content')
        # style_path = 'uploads/starry.jpg'#save_file_from_request('style')

        content_path = save_file_from_request('content')
        style_path = save_file_from_request('style')
        iters = int(request.form['iters'])
        result_array = model(style_path=style_path,
             content_path=content_path,  iters=iters)
        filename = 'result.jpg'
        result_path = os.path.join(app.config['GEN_FOLDER'], filename)
        plt.imsave(result_path,(result_array * 255).astype('uint8'))
        return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=content>
        <input type=file name=style>
        <input type="range" id="iters" name="iters" min="1" max="4" value="1">
        <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/generated/<name>')
def download_file(name):
    return send_from_directory(app.config["GEN_FOLDER"], name)
