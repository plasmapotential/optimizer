#ioHEATClass.py
#Description:   interface to HEAT for optimizer
#Engineer:      T Looby
#Date:          20220324
import time
import os
import sys

class ioInterface():
    def __init__(self, runMode='docker'):
        """
        initialize interface class object
        """
        import launchHEAT
        #load HEAT environment
        launchHEAT.loadEnviron()

        #load logger
#        global log
#        #initialize logs
#        log = launchHEAT.getLogger()

        return

    def preProcess(self, x):
        """
        takes input parameter x and convert to HEAT input
        """
        #load CAD file
        CAD = self.loadCADfile()
        #process CAD
        CAD.extrudeFace(self.inputName)
        print([x.Label for x in CAD.CADobjs])
        #save new STP file
        CAD.saveSTEP(CAD.STPout, [CAD.CADobjs[-1]])


        if self.inputName == 'Cube':
            self.input = x * 100
        return


    def runModel(self):
        """
        runs HEAT in optimizer loop
        """
        time.sleep(0.01)
        self.output = self.input**2 + 2
        return

    def postProcess(self):
        """
        converts HEAT output to objective function f(x)
        """
        if self.inputName == 'Cube':
            self.f_x = self.output / 100.0
        return

    def loadCADfile(self):
        """
        loads a CAD file and returns HEAT CAD object
        """
        #load CAD module and STP file
        import CADClass
        rootDir = os.environ["rootDir"]
        dataPath = os.environ["dataPath"]
        CAD = CADClass.CAD(rootDir, dataPath)
        CAD.STPfile = self.STPfile
        CAD.STPout = self.STPfile.split('.')[0] + '_new.' + self.STPfile.split('.')[1]
        CAD.permute_mask = False
        CAD.loadSTEP()
        return CAD
