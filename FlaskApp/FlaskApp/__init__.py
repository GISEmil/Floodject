# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
import os, time, gd
from PIL import Image


UPLOAD_FOLDER = '/var/www/html/FlaskApp/FlaskApp/'
#ALLOWED_EXTENSIONS = set(['tif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['datafile']
		if file:
			timename = time.strftime("%d%m%y%H%M")
			filename = timename + '.tif'
			#filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			png_filename = os.path.join(UPLOAD_FOLDER + timename + '.png')
			tif_im = Image.open(os.path.join(UPLOAD_FOLDER + filename))
			if tif_im.mode != 'RGB':
				tif_im = tif_im.convert('RGB')
			tif_im.save(png_filename)
			#f = open(png_file, 'w')
			#writePng(f)
			
			f.close()
			return redirect(url_for('upload_file', filename=filename))

	return render_template('upload.html')

