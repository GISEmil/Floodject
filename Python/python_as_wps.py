from pywps.Process import WPSProcess

class Flooding(WPSProcess):

    def __init__(self):

        ##
        # Process Initialization
        WPSProcess.__init__(self,
            identifier = "flooding",
            title = "Flooding",
            abstract = "This process is used to flood a DEM with water",
            version = '1.0',
            grassLocation = "WGS_1984",
            statusSupported = True,
            storeSupported = True)

        # Define inputs here
        self.inputImage=self.addComplexInput(identifier='input',maxmegabites=100,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])
        self.outputImage=self.addComplexOutput(identifier="output",title="output image",formats=[{'mimeType':'image/tiff'}])
        self.maxLevel=self.addLiteralInput(identifier='MaxLevel',minOccurs=1, maxOccurs=1)
        self.interval=self.addLiteralInput(identifier='Interval',minOccurs=1, maxOccurs=1)

    def execute(self):
	    loop_no = 3 # ( self.maxLevel.getValue() / self.Interval.getValue() )

        # Ocean Input, creating a temporary point to define the identification of water.
		# y_ocean = 38.322712

		# x_ocean = 16.436673

		# create_point(x_ocean, y_ocean)

        # Set the number of loops performed so far to 0.

		actual_loop = 0

		# Creating variable names for output during the process
		original = 'original' + str(random.randint(1,100))
		ocean_point = 'ocean_point' + str(random.randint(1,100))
		#ocean_vector = 'ocean_vect' + str(random.randint(1,100))
		#selected_ocean = 'selected_ocean' + str(random.randint(1,100))

		self.cmd(['v.in.ogr',  '-o', input='test.geojson', output=ocean_point])

		self.cmd(['r.in.gdal', flags='', input ='NEWTIF.tif', output=original])

		while actual_loop < loop_no:

			self.cmd(['g.region', rast=original])

			expressionout = 'out' + str(random.randint(1,100)) + '_' + str(actual_loop)

			self.cmd(['r.mapcalc', expression= '%s = if(%s <= %s, 0, null())' % (expressionout, original, actual_loop)])

			ocean_vector = 'ocean_vector_' + str(random.randint(1,100)) + str(actual_loop)

			self.cmd(['r.to.vect', input = expressionout, output = ocean_vector, type = 'area'])

			selected_ocean = 'ocean_select_' + str(random.randint(1,100)) + str(actual_loop)

			self.cmd(['v.select', ainput=ocean_vector, binput=ocean_point, output=selected_ocean, operator='intersects'])

			user_out = expressionout + '_' + str(actual_loop)

			#self.cmd(['r.out.gdal', input=expressionout, output = user_out)

			#self.cmd(['v.out.ogr', input=selected_ocean, output = selected_ocean)

			#self.cmd(['v.out.ogr', input=ocean_vector, output = ocean_vector)

			actual_loop = actual_loop + 1

		#Run cleanup
		#cleanup_data()
