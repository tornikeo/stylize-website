import os
from flask import Flask, flash, request, redirect, url_for
from flask import request, render_template
import flask
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app import app

from pathlib import Path
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

def image_from_request(name):
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
    # filename = secure_filename(file.filename)
    # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # file.save(path)
    image = Image.open(file)
    return image

from io import BytesIO
from flask import send_file
import matplotlib.pyplot as plt

@app.route('/home')
def home():
    return url_for('/')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            content = image_from_request('content')
            style = image_from_request('style')
            iters = int(request.form['iters'])
            result = app.config['MODEL'](style=style, 
                content=content, 
                iters=iters)
            return download_file(pil_img=result)
        except Exception as ex:
            flash('Something went wrong')
            print(ex.message)
    return render_template('home.html')

def download_file(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
