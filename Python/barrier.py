#!/usr/bin/env python

import os
import sys
import subprocess
import numpy
import osgeo
import time
from osgeo import ogr

# Linux
grass7bin_lin = 'grass70'

# add your path to grassdata (the GRASS GIS database) directory
gisbase = '/usr/lib/grass70'

gisdb = os.path.join(os.path.expanduser("~"), "grassdata")

# specify (existing) location and mapset, program has to run once to set these up
location = "newLocation"
mapset   = "PERMANENT"

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

gsetup.init(gisbase, gisdb, location, mapset)

inp_name = 'barrier.geojson'
coll_name = 'barrier'
coll_type = 'double precision'
barr_height = 3

gscript.run_command('g.remove', flags = 'f', type = 'vect', pattern = '*')
gscript.run_command('g.remove', flags = 'f', type = 'rast', pattern = '*')

gscript.run_command('v.in.ogr', flags = 'o', input = inp_name, type = 'line', output = 'barr_layer2')

gscript.run_command('g.region', vect = 'barr_layer2')

gscript.run_command('v.info', flags ='c', map = 'barr_layer2')

#remember to change the var=3 to the users choice
gscript.run_command('v.to.rast', input = 'barr_layer2', type = 'line', output = 'barr_raster', use='val', value = barr_height)

gscript.run_command('r.info', map = 'barr_raster')

gscript.run_command('r.mapcalc', expression='edges_1_1 = if(barr_raster[-1,-1]==barr_raster, barr_raster, null())')
gscript.run_command('r.mapcalc', expression='edges_11 = if(barr_raster[-1,1]==barr_raster, barr_raster, null())')
gscript.run_command('r.mapcalc', expression='edges1_1 = if(barr_raster[1,-1]==barr_raster, barr_raster, null())')
gscript.run_command('r.mapcalc', expression='edges11 = if(barr_raster[1,1]==barr_raster, barr_raster, null())')

gscript.run_command('r.patch', input=['edges_1_1','edges_11','edges1_1','edges11'], output = 'merged')

#gscript.run_command('r.mapcalc', expression='merged_left1 = if(merged[1,-1] == %s, merged[1,0] == %s, null())' %(barr_height,barr_height))

#gscript.run_command('r.mapcalc', expression='merged_right1 = if(merged[1,1] == %s, merged[1,0] == %s, null())' %(barr_height,barr_height))

gscript.run_command('r.mapcalc', expression='merged_ext = merged[1,0]')

gscript.run_command('r.patch', input=['merged_ext', 'merged'], output = 'merged_new')

gscript.run_command('r.mapcalc', expression='merged_minus = if(merged_new == merged_new[-1,-1] , merged_new, null())')

gscript.run_command('r.mapcalc', expression='merged_minus2 = if(merged_new == merged_new[1,-1] , merged_new, null())')

#gscript.run_command('r.mapcalc', expression='merged_left2 = if(merged[1,-1] && merged[1,-1] == %s, merged[1,0] == %s, null())' %(barr_height,barr_height))

#gscript.run_command('r.mapcalc', expression='merged_right2 = if(merged[-1,-1] ==%s && merged[1,1] == %s, merged[1,0] == %s, null())' %(barr_height,barr_height,barr_height))


#gscript.run_command('r.grow', input = 'barr_raster', output = 'corr_barrier')

#gscript.run_command('r.info', map = 'corr_barrier')
