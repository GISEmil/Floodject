from pywps.Process import WPSProcess
import os
import random
import string


class Testproc(WPSProcess):

    def __init__(self):

        ##
        # Process Initialization
        WPSProcess.__init__(self,
            identifier = "simpleflood",
            title = "Flooding a raster in a simple way",
            abstract = "This process is used to quickly and easily flood a DEM with water",
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

        self.outputVector=self.addComplexOutput(identifier="vector0",title="output vector", asReference=True)

    def execute(self):

    	# Importing the provided raster and and vector data
        original = 'original'
        self.cmd(['r.in.gdal','input=%s' % self.rasterin.getValue(),'output=%s' % original,'-o'])

        ocean_point = 'ocean_point'
        self.cmd(['v.in.ogr','dsn=%s' % self.vectorin.getValue(), 'type=point','output=%s' % ocean_point,'-o','--verbose'])

    	#Extract the land from DEM
        self.cmd(['r.mapcalc', '%s = if(%s != 0, %s, null())' % ('Xland',original,'original')])

        #Set region to the imported raster
        self.cmd(['g.region','rast=%s' % (original)])

        #Do mapcalculation to flood area
        expressionout = 'expressionout'
        self.cmd(['r.mapcalc','%s = if(%s <= %s, 3, null())' % (expressionout, original, '3')])

        #Convert all water to vector
        ocean_vector = 'ocean_vector'
        self.cmd(['r.to.vect','input=%s' % expressionout,'feature=area','output=%s' % ocean_vector])

        #Select only continuous ocean connected to the ocean point
        selected_ocean = 'selected_ocean'
        self.cmd(['v.select', 'ainput=%s' % ocean_vector,'binput=%s' % ocean_point,'output=%s' % selected_ocean,'operator=intersects'])

        #Convert selected ocean to raster, so that we only get water connected to the input point
        selected_ocean_rast = 'selected_ocean_rast'
        self.cmd(['v.to.rast', 'input=%s' % selected_ocean, 'output=%s' % selected_ocean_rast, 'use=val', 'value=0'])

        # Create waterdepths
        self.cmd(['r.mapcalc', '%s = %s - %s' % ('WaterDepth', selected_ocean_rast, original)])

        outputImage = "outputimage.jpg"
        self.cmd(['r.out.gdal','format=JPEG','input=selected_ocean_rast', 'output=%s' % outputImage])

        outputImage1 = "outputimage1.tif"
        self.cmd(['r.out.gdal','format=GTiff','input=WaterDepth', 'output=%s' % outputImage1])

        outputVector1 = "outputvector.geojson"
        self.cmd(['v.out.ogr','format=GeoJSON','type=area','input=%s' % selected_ocean,'dsn=%s' % outputVector1])

        self.outputImage0.setValue(outputImage)

        self.outputImage1.setValue(outputImage1)

        self.outputVector.setValue(outputVector1)
