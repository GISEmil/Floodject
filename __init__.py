#!/usr/bin/env python

import os
import sys
import subprocess
import numpy
import osgeo
from osgeo import ogr

# Linux
grass7bin_lin = 'grass70'

# add your path to grassdata (the GRASS GIS database) directory
gisbase = '/usr/lib/grass70'

gisdb = os.path.join(os.path.expanduser("~"), "grassdata")

# specify (existing) location and mapset, program has to run once to set these up
location = "WGS_1984"
mapset   = "test"

#gisbase = 'C:\Program Files (x86)\GRASS GIS 6.4.5svn' # query GRASS 7 itself for its GISBASE
gisbase = '/usr/lib/grass70'

# Set GISBASE environment variable
os.environ['GISBASE'] = gisbase
# the following not needed with trunk
os.environ['PATH'] += os.pathsep + os.path.join(gisbase, 'extrabin')

# define GRASS-Python environment
gpydir = os.path.join(gisbase, "etc", "python")
sys.path.append(gpydir)

# Set GISDBASE environment variable
os.environ['GISDBASE'] = gisdb

# import GRASS Python bindings (see also pygrass)
import grass.script as gscript
import grass.script.setup as gsetup
import random
from grass.script import raster as grassR
from osgeo import ogr


def main():




		#ask for flood info
		maxlevel_input = float(input("Please enter the maximum desired water level in meters: "))
		interval_input = float(input("Please enter the desired flood intervals in meters: "))

		loop_no = int(maxlevel_input/interval_input)

		#print "With the selected maximum water level of %s and flood level increment of %s, the number of loops is %s " % (maxlevel_input,  interval_input, loop_no)

		#ask for coordinates of the ocean point
		#x_ocean = float(input("Please provide with the X coordinate of the ocean point: "))
		#y_ocean = float(input("Please provide with the Y coordinate of the ocean point: "))

		y_ocean = 38.322712

		x_ocean = 16.436673

		actual_loop = 0

		create_point(x_ocean, y_ocean)

		print "You have chosen a point with the following coordinates: X %s, Y %s" % (x_ocean, y_ocean)

		gsetup.init(gisbase, gisdb, location, mapset)

		#Consider adding time and date to name + maybe random integer
		original = 'original' + str(random.randint(1,100))
		ocean_point = 'ocean_point' + str(random.randint(1,100))
		#ocean_vector = 'ocean_vect' + str(random.randint(1,100))
		#selected_ocean = 'selected_ocean' + str(random.randint(1,100))

		gscript.run_command('v.in.ogr',  flags='o', input='test.geojson', output=ocean_point)

		gscript.run_command('r.in.gdal', flags='', input = 'NEWTIF.tif', output=original)

		print "Import done"

		while actual_loop < loop_no:

			gscript.run_command('g.region', rast=original)

			expressionout = 'out' + str(random.randint(1,100)) + '_' + str(actual_loop)

			gscript.run_command('r.mapcalc', expression= '%s = if(%s <= %s, 0, null())' % (expressionout, original, actual_loop))

			print "Mapcalc done"

			ocean_vector = 'ocean_vector_' + str(random.randint(1,100)) + str(actual_loop)

			gscript.run_command('r.to.vect', input = expressionout, output = ocean_vector, type = 'area')

			print "Vector conversion done"

			selected_ocean = 'ocean_select_' + str(random.randint(1,100)) + str(actual_loop)

			gscript.run_command('v.select', ainput=ocean_vector, binput=ocean_point, output=selected_ocean, operator='intersects')

			print "select done"

			user_out = expressionout + '_' + str(actual_loop)

			#gscript.run_command('r.out.gdal', input=expressionout, output = user_out)

			#gscript.run_command('v.out.ogr', input=selected_ocean, output = selected_ocean)

			#gscript.run_command('v.out.ogr', input=ocean_vector, output = ocean_vector)

			actual_loop = actual_loop + 1

		print "Here we are"

		#Run cleanup
		cleanup_data()

def create_point(x_ocean, y_ocean):
	try:
		point = ogr.Geometry(ogr.wkbPoint)
		point.AddPoint(x_ocean, y_ocean)

		print '%d, %d' % (point.GetX(), point.GetY())

		#geojson = point.ExportToJson()
		#print geojson
	
		# Create the output Driver
		outDriver = ogr.GetDriverByName('GeoJSON')

		# Create the output GeoJSON
		outDataSource = outDriver.CreateDataSource('test.geojson')
		outLayer = outDataSource.CreateLayer('test.geojson', geom_type=ogr.wkbPoint )

		# Get the output Layer's Feature Definition
		featureDefn = outLayer.GetLayerDefn()

		# create a new feature
		outFeature = ogr.Feature(featureDefn)

		# Set new geometry
		outFeature.SetGeometry(point)

		# Add new feature to output Layer
		outLayer.CreateFeature(outFeature)
	except:
		"Cannot create point"

def cleanup_data():
	try:
		gscript.run_command('g.remove', flags='f', type = 'raster', pattern='out*')

		gscript.run_command('g.remove', flags='f', type = 'raster', pattern='original*')

		gscript.run_command('g.remove', flags='f', type = 'vector', pattern='ocean*')

		gscript.run_command('g.remove', flags='f', type = 'vector', pattern='select*')

		print "Cleanup done"

	except:
		print "Cleanup could not be performed"

if __name__ == "__main__":
	main()
