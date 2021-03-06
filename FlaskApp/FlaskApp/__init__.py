# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
import os, time, gd
import PIL
from PIL import Image
from osgeo import gdal

UPLOAD_FOLDER = '/var/www/html/FlaskApp/FlaskApp/static/images'
ALLOWED_EXTENSIONS = set(['tif'])

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
		if allowed_file(file.filename):
			timename = time.strftime("%d%m%y%H%M")
			filename = timename + '.tif'
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			# Convert image to jpeg for show to user
			src_ds = gdal.Open( os.path.join(app.config['UPLOAD_FOLDER'], filename) )
			formatimage = "PNG"
			driver = gdal.GetDriverByName( formatimage )

			fileName, fileExtension = os.path.splitext(filename)

			finalloca = '/var/www/html/FlaskApp/FlaskApp/static/images/' + str(fileName) + '.png'

			dst_ds = driver.CreateCopy( finalloca, src_ds, 0)

			#im = Image.open('/var/www/html/FlaskApp/FlaskApp/' + filename)
			#im.save('test.jpeg')

			#img = '/var/www/html/FlaskApp/FlaskApp/' + filename


			#img = Image.open('/var/www/html/FlaskApp/FlaskApp/' + filename)
			#img.save('output.jpg',"JPEG")

			#png_filename = os.path.join(UPLOAD_FOLDER + timename + '.png')
			#tif_im = Image.open(os.path.join(UPLOAD_FOLDER + filename))
			#if tif_im.mode != 'RGB':
			#	tif_im = tif_im.convert('RGB')
			#tif_im.save(png_filename)
			#f = open(png_file, 'w')
			#writePng(f)

			# Get the corners

			ds = gdal.Open(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			width = ds.RasterXSize
			height = ds.RasterYSize
			gt = ds.GetGeoTransform()
			minx = gt[0]
			miny = gt[3] + width*gt[4] +height*gt[5]
			maxx = gt[0] + width*gt[1] + height*gt[2]
			maxy = gt[3]

			# We need minx,miny & maxx, maxy
			southwest = str(minx) + "," + str(miny)
			northeast = str(maxx) + "," + str(maxy)
			#f.close()
			return redirect(url_for('upload_file',filename=filename,minx=minx,miny=miny,maxx=maxx,maxy=maxy))
	return render_template('upload.html')

@app.route('/ajax')

@app.route('/files')
def dir_listing(req_path):
    BASE_DIR = '/var/www/html/FlaskApp/FlaskApp/images'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('images.html', files=files)



def perform_analysis():
	return render_template('request.html')
