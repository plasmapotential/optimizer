#optimizerClass.py
#Description:   optimizes an objective function (forward model)
#Engineer:      T Looby
#Date:          20220324
import time
from scipy.optimize import minimize_scalar
import pandas as pd
import numpy as np
import sys

class optimizer():
    def __init__(self, optimizerFile):
        """
        initialize class object

        this class is used to optimize some scalar function, f(x),
        where x is the input parameter.  The algorithm finds the
        minimum of f(x) between the bounds defined by user

        inputNames is a list of input variable names

        lowBound is a list of lower bounds, indexed to
        match inputNames

        upBound is a list of upper bounds, undexed to
        match inputNames

        This class was witten to be general.  The function f(x) is designed to
        be evaluated in a separate interface class, which is assigned to the
        self.IO object in the runOptimizerLoop() method.  By making f(x) a
        separate class that is imported into this one, it enables modularity.
        A user can simply create an interface class for any f(x), so long as that
        class contains a few functions (preProcess, runModel, postProcess).
        This is particularly useful when a user wants to use a third party
        code as f(x).  The interface class preprocesses the parameterized variables
        so that they are formatted as inputs to the third party code, runs the
        code, and then postprocesses the code output into a scalar objective
        function, f(x).  Each code that a user wants to optimize would therefore have
        a separate interface class (python script).

        For example, if a user wants to use the code HEAT as f(x), where x
        is some variable in the CAD (ie a PFC height), then a ioHEATClass.py
        script is created with an ioHEAT() class.  In this class, a preProcess()
        method takes the x (PFC height) and turns it into a HEAT input (new CAD
        geometry), runs the HEAT model with the runModel() method and generates
        output (heat flux profiles), then using postProcess() calculates some
        quantity to be used in the objective function (ie peak q" on PFC).  This
        quantity is the variable to be optimized, f(x).

        """
        self.readOptimizerFile(optimizerFile)
        return

    def readOptimizerFile(self, file):
        """
        reads an optimizer input file, which is in the format:
        """
        data = pd.read_csv(file, sep=',', comment='#', skipinitialspace=True)
        self.modelNames = np.unique(data['modelName'].values)
        self.inputNames = []
        self.lowBounds = []
        self.upBounds = []
        self.extraFiles = []
        for model in self.modelNames:
            self.inputNames.append(data[data['modelName']==model]["inputName"].values)
            self.lowBounds.append(data[data['modelName']==model]["lowBound"].values)
            self.upBounds.append(data[data['modelName']==model]["upBound"].values)
            self.extraFiles.append(data[data['modelName']==model]["file"].values)

        return

    def runOptimizerLoop(self):
        """
        iteratively finds an optimum for an objective
        function, f(x)

        returns x corresponding to optimum point

        self.IO should be initialized with forward model
        self.IO should contain three methods:
        self.IO.preProcess()
        self.IO.runModel()
        self.IO.postProcess()
        """
        #loop through forward models defined in input file
        for i in range(len(self.modelNames)):
            modelName = self.modelNames[i]
            #initialize interface to forward model
            #initialize interface to forward model
            if modelName == 'Example':
                print("\nRunning Example CASE forward model")
                import interfaces.ioExampleClass as interface
                self.IO = interface.ioInterface()
            elif modelName == 'HEAT':
                print("\nRunning HEAT forward model")
                import interfaces.ioHEATClass as interface
                self.IO = interface.ioInterface()
            #elif there were other forward models, they would be included here
            #and initizlized under the self.IO object
            #for example, FreeGS could be another optimization variable

            #optimize each variables independently
            for j in range(len(self.inputNames[i])):
                print("Optimizing variable: "+self.inputNames[i][j])
                self.IO.inputName = self.inputNames[i][j]
                bkt = (self.lowBounds[i][j], self.upBounds[i][j])
                res = minimize_scalar(self.runForwardModel, method='bounded', bounds=bkt)
                print(res.x)
        return

    def runForwardModel(self, x):
        """
        runs a forward model

        self.IO should be set up with an interface to a specific code or function

        x is input parameter
        f_x is objective function evaluated at x, f(x)
        """
        self.IO.preProcess(x)
        self.IO.runModel()
        self.IO.postProcess()
        return self.IO.f_x



if __name__ == "__main__":
    t0 = time.time()
    #append HEATpath to PYTHONPATH envvar
    HEATpath = '/home/tom/source/HEAT/github/source'
    sys.path.append(HEATpath)
    optimizerFile = 'optimizerInputHEAT.dat'
    opt = optimizer(optimizerFile)
    opt.runOptimizerLoop()

    print("Time Elapsed [s]: {:f}".format(time.time() - t0))
