from pywps.Process import WPSProcess
import os
import random
import string

# random folder for checking the input of the raster area

random_file1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
random_folder1 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
random_file2 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])
random_folder2 = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])

# Preliminary Settings #
########################

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

	'''
        self.outputImage0=self.addComplexOutput(identifier="output0",title="output image")

        self.outputImage1=self.addComplexOutput(identifier="output1",title="output image")

        self.outputImage2=self.addComplexOutput(identifier="output2",title="output image")
        '''

        self.donecheck = self.addLiteralOutput(identifier='Done',title='Output')

        # self.outputVector=self.addComplexOutput(identifier='vectorout', title='output vector')

    def execute(self):

        original = 'original'

    	# Importing the provided raster and and vector data
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

        output = 5


        ######################################
        ##                                  ##
        ## All the outputs are defined here ##
        ##                                  ##
        ######################################

        #Export vector

        #outputImage = 'output.png'

        #self.cmd(['r.out.gdal','format=PNG','input=%s' % selected_ocean_rast, 'output=%s' % outputImage])

        self.donecheck.setValue(output)

        '''
        #Kept to not lose the information

        #Export vector
        user_out = 'output' + str(loops) + '.geojson'
        #self.cmd(['v.out.ogr','input=%s' % ocean_vector,'format=GeoJSON','output=%s' % user_out])
        self.cmd(['v.out.ogr', 'input=%s' % selected_ocean,'format=GeoJSON','type=area','dsn=%s' % (user_out)])
        self.outputVector.setValue(user_out)


        #Export raster
        output = 'output1.png'
        self.cmd(['r.out.gdal','format=PNG','input=%s' % 'out1', 'output=%s' % (output)])
        self.outputImage1.setValue(output)


            #Do something ??
            self.cmd(['r.mapcalc', '%s = if( %s == 0, (%s * %s), null())' % (selected_ocean_rast, intermediate, interval_input, actual_loop)])

            #Export the vectors and rasters
            outputnames_rast.append(selected_ocean_rast)

            outputnames_vect.append(selected_ocean)

            if os.path.isfile('/tmp/temp.txt'): #This should be a relative path by the way, as several requests will try and read the same file
            	os.remove('/tmp/temp.txt')

            self.cmd(['r.report', 'map=%s' %s selected_ocean_rast, 'units=k', 'output=/tmp/temp.txt'])
            tempTxt = open('/tmp/temp.txt', 'r')

            for row in TempTxt:
            	print row
            	if row[1]== actual_increment[0]:
            		AreaOut=row.split('|')
            		areaList.append(AreaOUt[3]) #This should be explained properly

            tempTxt.close()

            old_loop = actual_loop -1

            if float(areaList[actual_loop)) - float(areaList[old_loop]) > 0.02:

		self.cmd(['v.overlay', 'ainput = %s' % selected_ocean,
            	'binut = old_flood', 'operator=not', 'output=subtructed_flood'])

            	self.cmd(['v.to.db', 'map=subtructed_flood', 'option=area', 'columns=a_value'])

            	self.cmd(['v.extract', 'input=subtracted_flood', 'output=subtracted_flood_extract', 'where=a_value > 1000'])

            	self.cmd(['v.to.rast', 'input=subtracted_flood_extract','output=subtracted_raster','use=cat'])

		self.cmd(['r.mapcalc', '%s=if( isnull(%s), %s, %s') % ('merged', 'subracted_raster', 'old_flood_rast', selected_ocean_rast)])

		self.cmd(['r.neighbors', 'input=merged', 'output=diversity', 'method=diversity'])

		pourpoint='pourpoint_'+str(actual_loop)
		self.cmd(['r.mapcalc', '%s=if(%s == 2, %s, null())' % (pourpoint, 'diversity', 'diversity')])

		self.cmd(['r.to.vect', 'input=%s' % pourpoint, 'output=%s' % pourpoint, 'feature=point'])

		self.cmd(['g.remove', '-f', 'type=raster','pattern=sub*'])
		self.cmd(['g.remove', '-f', 'type=vector','pattern=sub*'])
		self.cmd(['g.remove', '-f', 'type=raster','pattern=merged*'])
		self.cmd(['g.remove', '-f', 'type=raster','pattern=diversity*'])

	    self.cmd(['g.remove', '-f', 'type=vector','pattern=old_flood'])

	    self.cmd(['g.remove', '-f', 'type=raster','pattern=old_flood_rast'])

	    self.cmd(['g.copy', vect = (selected_ocean, 'old_flood'))

	    self.cmd(['g.copy', rast = (selected_ocean_rast, 'old_flood_rast')])

            actual_loop = actual_loop + 1

        ################################
        ##                            ##
        ## Perform watershed analysis ##
        ##                            ##
        ################################

        self.cmd(['g.region','rast=original'])

        self.cmd(['r.fill.dir','input=Xland','elevation=filled','direction=direction']) # Check to see resouliton at later stage, getting D8 resolution error

        self.cmd(['r.watershed','elevation=filled','accumulation=accumulation'])

        #accmax = self.cmd([])

        thresHold = 100000 * 0.01

        self.cmd(['r.watershed','elevation=filled','threshold=%s' % thresHold,'basin=watershed'])

        self.cmd(['r.statistics','base=watershed','cover=accumulation','method=max','output=statoutput'])

        self.cmd(['r.mapcalc','expression=%s = int(%s)' % ('flow_int', 'accumulation')])

        self.cmd(['r.mapcalc','expression=%s = int(%s)' % ('stat_int', 'statouput')])

        self.cmd(['r.mapcalc','expression=%s = if(%s == %s, 10, null())' % ('pour_point', 'flow_int', 'stat_int')])

        #######################
        ##                   ##
        ##      Watershed    ##
        ##                   ##
        #######################

        filled = 'DEM_filled'
        Direction = 'direction'
        Accumulation = 'accumulation'
        label_stat = 'label_stat'
        watershed = 'watershed'
        half_basin = 'half_basin'
        drainage = 'drainage'
        zonal_stat = 'zonal_stat'
        prepour_point = 'prepour_point'
        pour_point = 'pour_point'
        pour_point_vect = 'pour_point_vect'
        basin_perimeter = 'basin_perimeter'
        stream = 'stream'
        focal = 'focal'
        Accumulation_int = 'accumulation_int'
        stat_int = 'stat_int'

        self.cmd(['g.region','rast=original'])
        self.cmd(['r.fill.dir','input=original', 'elevation=%s' % filled, 'direction=%s' % Direction])
        self.cmd(['r.watershed','-4','-m','elevation=filled','accumulation=%s' % Accumulation])

        thresHold = 11000

        self.cmd(['r.watershed','-4','elevation=%s' % filled, 'drainage=%s' % drainage, 'half.basin=%s' % half_basin, 'threshold=%s' % thresHold, 'stream=%s' % stream, "basin=%s" % watershed])
        self.cmd(['r.neighbors', 'input=%s' % watershed, 'output=%s' % focal, 'method=diversity'])
        self.cmd(['r.mapcalc', 'expression=%s=if(%s >= 2, %s, null())' % (basin_perimeter, focal, watershed)])
        self.cmd(['r.mapcalc', 'expression=%s=(int(%s))' % (Accumulation_int, accumulation)]) # WWhy do we convert it to integer? Must write about that
        self.cmd(['r.statistics','base=%s' % basin_perimeter, 'cover=%s' % Accumulation_int, 'method=max', 'output=%s' % label_stat])
        self.cmd(['r.mapcalc', 'expression=%s=@%s' % (zonal_stat, label_stat)])
        self.cmd(['r.mapcalc', 'expression=%s=int(%s)' % (stat_int, zonal_stat)])
        self.cmd(['r.mapcalc', 'expression=%s=if(%s == %s, 10, null())' % (prepour_point, Accumulation_int, stat_int)])
        self.cmd(['r.mapcalc', 'expression=%s=if(%s > 0, %s, null())' % (pour_point, original, prepour_point)])
        self.cmd(['r.to.vect', 'input=%s' % pour_point, 'output=%s' % pour_point_vect, 'feature=point'])

        ##############################
        ##                          ##
        ##        Reproject         ##
        ##                          ##
        ##############################

        epsg_code = 25832

        location_name = "temporary_" + str(epsg_code)

        self.cmd(['g.proj','-c','epsg=%s' % epsg_code, 'location=location_name'])

        self.cmd(['g.mapset','mapset=PERMANENT','location=location_name'])

        self.cmd(['v.proj','input=b_polygon','location=location','mapset=mapset','dbase=gisdb'])

        self.cmd(['v.proj','input=ocean_point','location=location','mapset=mapset','dbase=gisdb'])

        self.cmd(['g.region','vect=b_polygon'])

        self.cmd(['r.proj','-n','input=original','location','mapset=mapset','dbase=gisdb','output=original','memory=800'])


        #############################################
        ##                                         ##
        ## Perform calculation based on projection ##
        ##                                         ##
        #############################################

        actual_loop_proj = 0

        while actual_loop_proj <= loop_no:

                self.cmd(['g.region','rast=original'])

                expressionout_proj = 'expressionout_proj' + str(actual_loop_proj)

                expressionout_land = 'expressionout_land' + str(actual_loop_proj)

                self.cmd(['r.mapcalc','expression=%s=if(%s<=%s, 0, null())'  % (expressionout_proj, original, actual_loop_proj)])

                self.cmd(['r.mapcalc','expression=%s=if(%s > %s, 1, null())' % (expressiounout_land, original, actual_loop_proj)])

                ocean_vector = "ocean_vector" + str(actual_loop_proj)

                self.cmd(['r.to.vect','input=expressionout_proj','output=%s' % ocean_vector,'type=area'])

                self.cmd(['v.select','ainput=ocean_vector','binput=ocean_point','output=selected_ocean','operator=intersects'])

                selected_ocean_rast = "selected_ocean_rast" + str(actual_loop_proj)

                self.cmd(['v.to.rast','input=selected_ocean','output=%s' % selected_ocean_rast,'use=val','value=0'])

                actual_loop_proj = actual_loop_proj + 1
        '''
