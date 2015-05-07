from pywps.Process import WPSProcess
import os
import random
import string

class Testproc(WPSProcess):

    def __init__(self):

        ##
        # Process Initialization
        WPSProcess.__init__(self,
            identifier = "testproc",
            title = "Testproc for server!",
            abstract = "This process is used to flood a DEM with water",
            version = "1.0",
            #grassLocation = None,
            grassLocation = True,
            statusSupported = True,
            storeSupported = True)

        # Define inputs #
        #################

        self.rasterin=self.addComplexInput(identifier='rasterin',maxmegabites=10000,title="input image",minOccurs=1,maxOccurs=1,formats = [{'mimeType': 'image/tiff'}, {'mimeType': 'image/geotiff'}, {'mimeType': 'application/geotiff'}, {'mimeType': 'application/x-geotiff'}])

        self.vectorin = self.addComplexInput(identifier="vectorin",title="Input point",formats = [{"mimeType":"application/json","encoding":"utf-8","schema":None}])

        # Define output #
        #################

        self.outputImage0=self.addComplexOutput(identifier="output0",title="output image")

        self.outputImage1=self.addComplexOutput(identifier="output1",title="output image")

        self.outputVector=self.addComplexOutput(identifier='vectorout', title='output vector')

        # self.donecheck = self.addLiteralOutput(identifier='Done',title='Output')

        # self.outputVector=self.addComplexOutput(identifier='vectorout', title='output vector')

    def execute(self):

        self.outputImage0.setValue(self.rasterin.getValue())

        self.outputImage1.setValue(self.rasterin.getValue())

        self.outputVector.setValue(self.vectorin.getValue())
