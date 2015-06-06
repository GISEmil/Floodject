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
            identifier = "flooding_cost",
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

        # Read rasterarea

        #raster_area = 'raster_area'
        #raster_area_pol = 'raster_area_pol'
        #simplify raster
        #self.cmd(['r.mapcalc', '%s = if(%s <=0, 0, 0)' % (raster_area, original)])
        #self.cmd(['r.to.vect','input=%s' % raster_area,'feature=area','output=%s' % raster_area_pol])
        #self.cmd(['v.to.db', 'map=%s' % raster_area_pol, 'option=area','columns=value'])

        #number = self.cmd(["v.db.select", '-c', 'map=%s' % raster_area_pol, 'col=value'])
        #logging.debug("%s" % number)
        #pp_criteria = (float(number)/1000000)* 0.01
        pp_criteria = 0.02

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

            # Find the reachable flood cells
            costout = 'costout_' + str(actual_loop)
            self.cmd(['r.cost', 'input=%s' % expressionout, 'output=%s' % costout,  'start_points=%s' % ocean_point])

            #Assing the flood level to the flood extent
            selected_ocean_rast = 'selected_ocean_rast_' + str(actual_loop)
            self.cmd(['r.mapcalc', '%s = if( %s >= 0, (%s * %s), null())' % (selected_ocean_rast, costout, interval_input, actual_loop)])

            #Convert all water to vector
            ocean_vector = 'ocean_vector_' + str(actual_loop)
            self.cmd(['r.to.vect','input=%s' % selected_ocean_rast,'feature=area','output=%s' % ocean_vector])

            #Calculate ocean polygon area

            self.cmd(['v.to.db', 'map=%s' % ocean_vector, 'option=area','columns=value'])

            area_select = self.cmd(["v.db.select", '-c', 'map=%s' % ocean_vector, 'col=value'])

            #reading all polygon area
            area_select_split=area_select.split('\n')

            polygon_area=[]

            for i in area_select_split:
            	if not i =='':
            	       polygon_area.append(float(i))

            # Summerizing all polygon area
            area = sum(polygon_area)


            #Collection of all flooded area
            areaList.append(float(area)/1000000)

            old_loop = actual_loop -1


            if float(areaList[actual_loop]) - float(areaList[old_loop]) > pp_criteria:

                firstrun = firstrun + 1

                pourpoint='pourpoint_'+str(actual_loop)

                pourpoint_vect = 'pourpoint_vect_' + str(actual_loop)

                self.cmd(['v.overlay', 'ainput=%s' % ocean_vector, 'binput=old_flood', 'operator=not', 'output=subtructed_flood'])

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

            self.cmd(['g.copy', 'vect=%s,%s' % (ocean_vector, 'old_flood')])

            self.cmd(['g.copy', 'rast=%s,%s' % (selected_ocean_rast, 'old_flood_rast')])

            actual_loop = actual_loop + 1


        self.cmd(['r.mapcalc', '%s = %s - %s' % ('WaterDepth', selected_ocean_rast, original)])

        outputImage = "outputimage.jpg"
        self.cmd(['r.out.gdal','format=JPEG','input=%s' % selected_ocean_rast, 'output=%s' % outputImage])

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
