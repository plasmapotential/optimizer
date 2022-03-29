#ioExampleClass.py
#Description:   example interface for optimizer
#Engineer:      T Looby
#Date:          20220324
import time


class ioInterface():
    def __init__(self):
        """
        initialize interface class object
        """
        return

    def preProcess(self, x):
        """
        takes input parameter x and convert to HEAT input
        """
        if self.inputName == 'height':
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
        if self.inputName == 'height':
            self.f_x = self.output / 100.0
        return
