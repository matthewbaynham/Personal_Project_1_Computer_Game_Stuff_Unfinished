#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modBasics"
__module__ = "modBasics"
__version__ = "0.1"
__bpydoc__ = """
This class contains all the basic elements that I want all my classes to inherent
mostly stuff for error handling and debugging other classes
"""
import sys
import traceback

#import time
#from datetime import datetime, date, time
from datetime import datetime

class ClsBasics():
#    __doc__ = """
#    This class contains all the basic elements that I want all my classes to inherent
#    mostly stuff for error handling and debugging other classes
#    """
#    bIsInitialised = False
    global lstWarnings

    def getClassName(self):
        return self._sClassName
    def setClassName(self, value):
        self._sClassName = value
    sClassName = property(getClassName, setClassName)

    def getClassStep(self):
        return self._sClassStep
    def setClassStep(self, value):
        self._sClassStep = value
    sClassStep = property(getClassStep, setClassStep)

    def getClassSubStep(self):
        return self._sClassSubStep
    def setClassSubStep(self, value):
        self._sClassSubStep = value
    sClassSubStep = property(getClassSubStep, setClassSubStep)

    def getClassUsefulValue(self):
        return self._sClassUsefulValue
    def setClassUsefulValue(self, value):
        self._sClassUsefulValue = value
    sClassUsefulValue = property(getClassUsefulValue, setClassUsefulValue)

    def getClassMessage(self):
        return self._sClassMessage
    def setClassMessage(self, value):
        self._sClassMessage = value
    sClassMessage = property(getClassMessage, setClassMessage)

    def initialiseBasicsClass(self):
#        bIsInitialised = True
        self.sClassName = ""
        self.sClassStep = ""
        self.sClassSubStep = ""
        self.sClassUsefulValue = ""
        self.sClassMessage = ""
        self.lstWarnings = []

    def addWarning(self, txtWarning):
        self.lstWarnings.append(txtWarning)

    def lstCounter(self, lst):
        iCounter = 0
        for x in lst:
            iCounter = iCounter + 1
        return iCounter

    def printWarnings(self):
        if self.lstWarnings is []:
            print "No Warnings"
        else:
            print "Warnings:"
            for txtWarning in self.lstWarnings:
                print "    " + txtWarning

    def errorCode(self):
        dNow = datetime.now()
        tError = sys.exc_info()
        tbError = tError[2]

        print ""
        print "Error: " + dNow.strftime("%Y-%m-%d %H:%M:%S")
        print "Type: " + str(tError[0])
        print "Parameter: " + str(tError[1])
        print "Line No: " + str(traceback.tb_lineno(tbError))

        self.printWarnings()

        print "..."
        print "Class Name = '" + self.sClassName + "'"
        print "Step  = '" + self.sClassStep + "'"
        print "Sub Step = '" + self.sClassSubStep + "'"
        print "Message = '" + self.sClassMessage + "'"
        print "Useful Value = '" + self.sClassUsefulValue + "'"




