from pywps.Process import WPSProcess

class Geotiff2PNG(WPSProcess):

    def __init__(self):

        ##
        # Process initialization
        WPSProcess.__init__(self,
            identifier = "geotiff2png",
            title="Geotiff to PNG conversion",
            version = "1.0",
            grassLocation = 'WGS_1984',
            storeSupported = True,
            statusSupported = True)


        self.inputImage=self.addComplexInput(identifier='input',maxmegabites=100,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])
        self.outputImage=self.addComplexOutput(identifier="output",title="output image",formats=[{'mimeType':'image/png'}])


    def execute(self):        
	self.cmd(["r.in.gdal","input=%s" % self.inputImage.getValue(),'output=inputImage','-o'])
        #r.gdal may import things as RBG bands, if so they need to regroupped
        try:
            self.cmd(['g.region',"rast=inputImage"])
        except:
            self.cmd(['g.region',"rast=inputImage.green"])
            self.cmd(["r.composite","red=inputImage.red","green=inputImage.green","blue=inputImage.blue","output=inputImage"])
        self.cmd(["r.out.png","input=inputImage","output=animage.png"])
        self.outputImage.setValue("animage.png")
