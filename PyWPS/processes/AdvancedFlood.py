from pywps.Process import WPSProcess
import os
import random
import string

import json

from osgeo import ogr
import os

import logging


# Preliminary Settings #
########################

# random folder for checking the input of the raster area

random_file1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
random_folder1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])

# Amount of input is fixed, output is dependent on the number of loops.

#Define empty lists for later use
outputnames_vect=[]
outputnames_rast=[]
areaList=[]


#Some variables can't be empty when initiating the script

pourpoint_vect = ""

#Max level of flood
maxlevel_input = 3

#Flood increment
interval_input = 0.01

#Total amount of loops
loop_no = int((maxlevel_input/interval_input))

class Flooding(WPSProcess):

    def __init__(self):

        ##
        # Process Initialization
        WPSProcess.__init__(self,
            identifier = "flooding",
            title = "Flooding",
            abstract = "This process is used to flood a DEM with water",
            version = "1.0",
            grassLocation = "/home/ubuntu/grassdata/WGS_1984",
            statusSupported = True,
            storeSupported = True)

        # Define inputs #
        #################

        self.rasterin=self.addComplexInput(identifier='rasterin',maxmegabites=10000,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])

        self.vectorin = self.addComplexInput(identifier="vectorin",title="Input point",formats = [{"mimeType":"text/json","encoding":"utf-8","schema":None}])

        # Define output #
        #################

        self.outputImage0=self.addComplexOutput(identifier="output0",title="output image", asReference=True)

        self.outputImage1=self.addComplexOutput(identifier="output1",title="output image", asReference=True)

        self.outputVector=self.addComplexOutput(identifier="output2",title="output vector", asReference=True)

    def execute(self):

        original = 'original'

        firstvector = ""
        firstrun = 0

        pourpoint_vect = 'pourpoint_vect_'

    	# Importing the provided raster and and vector data
        self.cmd(['r.in.gdal','input=%s' % self.rasterin.getValue(),'output=%s' % original,'-o'])
        ocean_point = 'ocean_point'
        self.cmd(['v.in.ogr','dsn=%s' % self.vectorin.getValue(), 'type=point','output=%s' % ocean_point,'-o'])

        ##############################
        ##                          ##
        ## Flood the DEM with water ##
        ##                          ##
        ##############################

        actual_loop = 0

        while actual_loop <= loop_no:

            #Set region to the imported raster
            self.cmd(['g.region','rast=%s' % (original)])

            #Do mapcalculation to flood area
            expressionout = 'expressionout_' + str(actual_loop)

            self.cmd(['r.mapcalc','%s = if(%s <= (%s * %s), 1, null())' % (expressionout, original, interval_input,str(actual_loop))])

            #Convert all water to vector
            ocean_vector = 'ocean_vector_' + str(actual_loop)
            self.cmd(['r.to.vect','input=%s' % expressionout,'feature=area','output=%s' % ocean_vector])

            #Select only continuous ocean connected to the ocean point
            selected_ocean = 'selected_ocean_' + str(actual_loop)
            self.cmd(['v.select', 'ainput=%s' % ocean_vector,'binput=%s' % ocean_point,'output=%s' % selected_ocean,'operator=intersects'])

            #Convert selected ocean to raster
            selected_ocean_rast = 'selected_ocean_rast_' + str(actual_loop) # ??
            intermediate = 'intermediate_' + str(actual_loop)
            self.cmd(['v.to.rast', 'input=%s' % selected_ocean, 'output=%s' % intermediate, 'use=val', 'value=0'])

            #Do something ??
            self.cmd(['r.mapcalc', '%s = if( %s == 0, (%s * %s), null())' % (selected_ocean_rast, intermediate, interval_input, actual_loop)])

	        #Export the vectors and rasters
            outputnames_rast.append(selected_ocean_rast)

            outputnames_vect.append(selected_ocean)

            self.cmd(['v.to.db', 'map=%s' % selected_ocean, 'option=area','columns=value'])

            area = self.cmd(["v.db.select", '-c', 'map=%s' % selected_ocean, 'col=value'])

            logging.debug("%s" % area)

            logging.debug("%f" % float(area))

            areaList.append(float(area)/1000000)

            logging.debug("%s" % areaList)

            old_loop = actual_loop -1


            if float(areaList[actual_loop]) - float(areaList[old_loop]) > 0.02:

                firstrun = firstrun + 1

                pourpoint='pourpoint_'+str(actual_loop)

                pourpoint_vect = 'pourpoint_vect_' + str(actual_loop)

                self.cmd(['v.overlay', 'ainput=%s' % selected_ocean, 'binput=old_flood', 'operator=not', 'output=subtructed_flood'])

                self.cmd(['v.to.db', 'map=subtructed_flood', 'option=area', 'columns=a_value'])

                self.cmd(['v.extract', 'input=subtructed_flood', 'output=subtracted_flood_extract', 'where=a_value > 1000'])

                self.cmd(['v.to.rast', 'input=subtracted_flood_extract','output=subtracted_raster','use=cat'])

                self.cmd(['r.mapcalc', '%s=if( isnull(%s), %s, %s)' % ('merged', 'subtracted_raster', 'old_flood_rast', selected_ocean_rast)])

                self.cmd(['r.neighbors', 'input=merged', 'output=diversity', 'method=diversity'])

                self.cmd(['r.mapcalc', '%s=if(%s == 2, 3 - %s, null())' % (pourpoint, 'diversity', original)])

                self.cmd(['r.to.vect', 'input=%s' % pourpoint, 'output=%s' % pourpoint_vect, 'feature=point'])

                if firstrun == 1:
                    firstvector = pourpoint_vect
                else:
                    self.cmd(['v.patch','--overwrite','-a','input=%s' % pourpoint_vect, 'output=%s' % firstvector])

                #self.cmd(['g.remove', '-f', 'rast=sub*'])

                #self.cmd(['g.remove', '-f', 'vect=sub*'])

                #self.cmd(['g.remove', '-f', 'rast=merged*'])

                #self.cmd(['g.remove', '-f', 'rast=diversity*'])

            self.cmd(['g.remove', '-f', 'vect=old_flood'])

            self.cmd(['g.remove', '-f', 'rast=old_flood_rast'])

            self.cmd(['g.copy', 'vect=%s,%s' % (selected_ocean, 'old_flood')])

            self.cmd(['g.copy', 'rast=%s,%s' % (selected_ocean_rast, 'old_flood_rast')])

            actual_loop = actual_loop + 1


        self.cmd(['r.mapcalc', '%s = %s - %s' % ('WaterDepth', selected_ocean_rast, original)])

        outputImage = "outputimage.jpg"
        self.cmd(['r.out.gdal','format=JPEG','input=%s' % intermediate, 'output=%s' % outputImage])

        outputImage1 = "outputimage1.tif"
        self.cmd(['r.out.gdal','format=GTiff','input=%s' % 'WaterDepth', 'output=%s' % outputImage1])

        outputVector1 = "outputvector.geojson"
        self.cmd(['v.out.ogr','format=GeoJSON','type=point','input=%s' % firstvector,'dsn=%s' % outputVector1])

        self.outputImage0.setValue(outputImage)

        self.outputImage1.setValue(outputImage1)

        self.outputVector.setValue(outputVector1)


        ######################################
        ##                                  ##
        ## All the outputs are defined here ##
        ##                                  ##
        ######################################
