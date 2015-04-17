# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
import os, time

UPLOAD_FOLDER = '/var/www/html/FlaskApp/FlaskApp/'
#ALLOWED_EXTENSIONS = set(['tif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
	return render_template('index')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['datafile']
		if file:
			filename = time.strftime("%d%m%y%H%M")
			#filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('upload_file', filename=filename)))

	return render_template('upload')
