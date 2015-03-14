from pywps.Process import WPSProcess
import gdal
import ogr

# Preliminary math #
####################
loop_no = 3

# ( self.maxLevel.getValue() / self.Interval.getValue() )

# Amount of input is fixed, output is dependent on the number of loops.


class Flooding(WPSProcess):

    def __init__(self):

        ##
        # Process Initialization
        WPSProcess.__init__(self,
            identifier = "flooding",
            title = "Flooding",
            abstract = "This process is used to flood a DEM with water",
            version = "1.0",
            grassLocation = '/home/ubuntu/grassdata/WGS_1984',
            statusSupported = True,
            storeSupported = True)

        # Define inputs #
        #################
        self.rasterin=self.addComplexInput(identifier='rasterin',maxmegabites=10000,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])
        #self.maxLevel=self.addLiteralInput(identifier='MaxLevel',title='Max level of water',minOccurs=1, maxOccurs=1)
        #self.interval=self.addLiteralInput(identifier='Interval',title='Interval of flooding',minOccurs=1, maxOccurs=1)
        #self.vectorin = self.addComplexInput(identifier="vectorin",title="Input file")

        #self.folderin = self.addComplexInput(identifier='folderin',title='Vector folder')

        # Define output #
        #################

        self.outputImage=self.addComplexOutput(identifier="output0",title="output image",formats=[{'mimeType':'image/tiff'}])
        self.outputVector=self.addComplexOutput(identifier='vectorout', title='output vector')

    def execute(self):
        import random


    	# Creating variable names for output during the process
        original = 'original' + str(random.randint(1,100))
        ocean_point = 'ocean_point' + str(random.randint(1,100))
    	#ocean_vector = 'ocean_vect' + str(random.randint(1,100))
    	#selected_ocean = 'selected_ocean' + str(random.randint(1,100))

        self.cmd(['g.remove','-f','type=vector','name=OGRGeoJSON'])
        self.cmd(['r.in.gdal','input=%s' % self.rasterin.getValue(),'output=%s' % original,'-o'])
        #self.cmd(['v.external','input=./', 'layer=%s' % self.vectorin.getValue(), 'output=suckit'])
        #postgresql = "PG:host=postgrefun.cyjgeky5dykt.eu-west-1.rds.amazonaws.com dbname=postgrefun user=piratosthegreat password=PqwurxnX1

        vectormap = 'vector' + str(random.randint(1,100))
        self.cmd(['v.edit','map=%s' % vectormap,'tool=create', '--verbose'])

        #inputtxt = "http://52.16.38.28/geojson/goodtimes.txt"
        #self.cmd(['v.in.ascii','input=%s' % inputtxt, 'output=testascii', 'format=point'])
        self.cmd(['v.edit','-n','input=-','map=%s' % vectormap,'tool=add', 'layer=good', '--verbose'],stdin="P 1 1\n 16.436673 38.322712\n 1 20'")
        #self.cmd(['v.in.ogr','input=%s' % self.vectorin.getValue(), 'output=%s' % ocean_point,'-o','-t','--verbose'])

        for loops in range(0, loop_no, 1):
            #Set region
            self.cmd(['g.region','raster=%s' % (original)])

            #Do mapcalculation to flood area
            expressionout = 'out' + str(random.randint(1,100)) + '_' + str(loops)
            self.cmd(['r.mapcalc','expression= %s = if(%s <= 1000, 0, null())' % (expressionout, original)])

            #Convert all water to vector
            ocean_vector = 'ocean_vector_' + str(random.randint(1,100)) + str(loops)
            self.cmd(['r.to.vect','input=%s' % expressionout,'output=%s' % ocean_vector, 'type=area'])

            #Select only continuous ocean
            selected_ocean = 'ocean_select_' + str(random.randint(1,100)) + str(loops)
            self.cmd(['v.select', 'ainput=%s' % ocean_vector,'binput=%s' % vectormap,'output=%s' % selected_ocean,'operator=intersects'])

            ##Export the vectors and rasters

            #Export vector
            user_out = 'vectoroutput' + str(loops) + '.geojson'
            self.cmd(['v.out.ogr','input=%s' % vectormap,'format=GeoJSON','output=%s' % user_out])
            #self.cmd(['v.out.ogr', 'input=%s' % selected_ocean, 'output = %s' % user_out])
            self.outputVector.setValue(user_out)

            #Export raster
            output = 'output' + str(loops) + '.tif'
            self.cmd(['r.out.gdal','input=%s' % expressionout, 'output=%s' % (output)])
            self.outputImage.setValue(output)
