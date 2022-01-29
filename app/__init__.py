from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
from pathlib import Path
import torch
import torch.nn as nn
import torch.nn.functional as F
from model import model

UPLOAD_FOLDER = Path('uploads')
GEN_FOLDER = Path('generated')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER.mkdir(exist_ok=True)
MODEL = model.Stylizer()

app = Flask(__name__,)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GEN_FOLDER'] = GEN_FOLDER
app.config['MODEL'] = MODEL

from app import views
