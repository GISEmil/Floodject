from pywps.Process import WPSProcess
import os
import random
import string


# Preliminary Settings #
########################

# random folder for checking the input of the raster area

random_file1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
random_folder1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
random_file2 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
random_folder2 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])

# Amount of input is fixed, output is dependent on the number of loops.

#Define empty lists for later use

areaList=[]

#Some variables can't be empty when initiating the script

pourpoint_vect = ""

#Max level of flood
maxlevel_input = 3

#Flood increment
interval_input = 3

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
            #grassLocation = None,
            grassLocation = True,
            statusSupported = True,
            storeSupported = True)

        # Define inputs #
        #################

        self.rasterin=self.addComplexInput(identifier='rasterin',maxmegabites=10000,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])

        self.vectorin = self.addComplexInput(identifier="vectorin",title="Input point")

        # Define output #
        #################

        self.outputImage0=self.addComplexOutput(identifier="output0",title="output image", asReference=True)

        self.outputImage1=self.addComplexOutput(identifier="output1",title="output image", asReference=True)

        self.outputVector1=self.addComplexOutput(identifier="outputVector1",title="output vector", asReference=True)


    def execute(self):

    	# Importing the provided raster and and vector data
        original = 'original'
        self.cmd(['r.in.gdal','input=%s' % self.rasterin.getValue(),'output=%s' % original,'-o'])

        if os.path.isfile('/tmp/%s/%s' % (random_folder1, random_file1): #This should be a relative path by the way, as several requests will try and read the same file

	    self.cmd(['r.report', 'map=%s' % selected_ocean_rast, 'units=k', 'output=%s' % (random_file])

        actual_increment = str(actual_loop*interval_input)

  	    tempTxt = open('temp.txt', 'r')

        for row in tempTxt:
        	if row[1]== actual_increment[0]:
        		AreaOut=row.split('|')
        		areaList.append(AreaOut[3]) #This should be explained properly
        tempTxt.close()

        ocean_point = 'ocean_point'
        self.cmd(['v.in.ogr','dsn=%s' % self.vectorin.getValue(), 'type=point','output=%s' % ocean_point,'-o','--verbose'])

        #Convert entire raster to values of 0
        self.cmd(['r.mapcalc','%s = if( %s <=0, 0, 0)' % ('b_area',original)])

	    #Converting the original tif into a bounding box
        self.cmd(['r.to.vect','input=b_area','output=b_polygon','feature = area'])

	    #Extract the land from DEM
        self.cmd(['r.mapcalc', '%s = if(%s != 0, %s, null())' % ('Xland',original,'original')])

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

            if os.path.isfile('/tmp/temp.txt'): #This should be a relative path by the way, as several requests will try and read the same file
            	os.remove('/tmp/temp.txt')

    	    self.cmd(['r.report', 'map=%s' % selected_ocean_rast, 'units=k', 'output=temp.txt'])

            actual_increment = str(actual_loop*interval_input)

      	    tempTxt = open('temp.txt', 'r')

            for row in tempTxt:
            	if row[1]== actual_increment[0]:
            		AreaOut=row.split('|')
            		areaList.append(AreaOut[3]) #This should be explained properly
            tempTxt.close()

            old_loop = actual_loop -1

            ###########################################
            #                                         #
            # Check to see if we have a critical area #
            #                                         #
            ###########################################

            if float(areaList[actual_loop]) - float(areaList[old_loop]) > 0.02:

        		self.cmd(['v.overlay', 'ainput = %s' % selected_ocean,
                    	'binut = old_flood', 'operator=not', 'output=subtructed_flood'])

            	self.cmd(['v.to.db', 'map=subtructed_flood', 'option=area', 'columns=a_value'])

            	self.cmd(['v.extract', 'input=subtracted_flood', 'output=subtracted_flood_extract', 'where=a_value > 1000'])

            	self.cmd(['v.to.rast', 'input=subtracted_flood_extract','output=subtracted_raster','use=cat'])

        		self.cmd(['r.mapcalc', '%s=if( isnull(%s), %s, %s)' % ('merged', 'subracted_raster', 'old_flood_rast', selected_ocean_rast)])

        		self.cmd(['r.neighbors', 'input=merged', 'output=diversity', 'method=diversity'])

        		pourpoint='pourpoint_'+str(actual_loop)
        		pourpoint_vect = 'pourpoint_vect_' + str(actual_loop)

        		self.cmd(['r.mapcalc', '%s=if(%s == 2, %s, null())' % (pourpoint, 'diversity', 'diversity')])

        		self.cmd(['r.to.vect', 'input=%s' % pourpoint, 'output=%s' % pourpoint_vect, 'feature=point'])

        		self.cmd(['g.remove', '-f', 'rast=sub*'])
        		self.cmd(['g.remove', '-f', 'vect=sub*'])
        		self.cmd(['g.remove', '-f', 'rast=merged*'])
        		self.cmd(['g.remove', '-f', 'rast=diversity*'])

        	    self.cmd(['g.remove', '-f', 'vect=old_flood'])

        	    self.cmd(['g.remove', '-f', 'rast=old_flood_rast'])

        	    self.cmd(['g.copy', 'vect = %s, %s' % (selected_ocean, 'old_flood')])

        	    self.cmd(['g.copy', 'rast = %s, %s' % (selected_ocean_rast, 'old_flood_rast')])

            actual_loop = actual_loop + 1

        # Create waterdepths
        self.cmd(['r.mapcalc', '%s = %s - %s' % ('WaterDepth', selected_ocean_rast, original)])



        ######################################
        ##                                  ##
        ## All the outputs are defined here ##
        ##                                  ##
        ######################################

        outputImage = "outputimage.jpg"
        self.cmd(['r.out.gdal','format=JPEG','input=WaterDepth', 'output=%s' % outputImage])

        outputImage1 = "outputimage1.tif"
        self.cmd(['r.out.gdal','format=GTiff','input=WaterDepth', 'output=%s' % outputImage1])

        outputVector1 = "pourpoints.geojson"
        self.cmd(['v.out.ogr','format=GeoJSON','type=line','input=%s' % pourpoint_vect,'dsn=%s' % outputVector1])
