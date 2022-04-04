#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modContainer"
__module__ = "modContainer"
__version__ = "0.1"
__bpydoc__ = """
Just the classes that contain all the data
"""

from modBasics import ClsBasics
from Blender import Mathutils
import operator
#import modBasics
#reload(modBasics)

class ClsObject(ClsBasics):
    __doc__ = """
    iOrder = the order in which the items will be listed
    objObect = what ever we are storing
    """
    def __init__(self, iOrder, bBeginning, objObect):
        self.initialiseBasicsClass()
        try:
            self.iOrder = iOrder
            self.objObject = objObject
        except:
            self.errorCode()

        def getOrder(self):
            try:
                return self._iOrder
            except:
                self.errorCode()
        def setOrder(self, value):
            try:
                self._iOrder = value
            except:
                self.errorCode()
        iOrder = property(getOrder, setOrder)

        def getObject(self):
            try:
                return self._objObject
            except:
                self.errorCode()
        def setObject(self, value):
            try:
                self._objObject = value
            except:
                self.errorCode()
        objObject = property(getObject, setObject)

class ClsContainer(ClsBasics):
    __doc__ = """
    a feature is a feature in a  walls of type ='door', 'window', 'divider' or 'end of wall'
    Note: the perpous of a divider is to provide more points to draw vertexs from
    Note: the 'end of wall' type is self explainatory
    """
#    global lstVariables

    def __init__(self):
        __doc__ = """
        This class contains objects
        """
        self.initialiseBasicsClass()
        try:
            self.iPosition = 0
            self.iCounter = 0
            self.lst = []
        except:
            self.errorCode()

    def addItem(self, iOrder, bBeginning, objObject):
        cTemp = ClsObject(iOrder, bBeginning, objObject)
        self.iCounter = self.iCounter + 1

        self.lst.append(cTemp)

    def sort(self):
        try:
            #do the sorting stuff
            self.lst.sort(key=operator.attrgetter('iOrder'))
        except:
            self.errorCode()

    #this property contains
    def getDefaultObject(self):
        return self._objDefaultObject
    def setDefaultObject(self, value):
        self._objDefaultObject = value
    objDefaultObject = property(getDefaultObject, setDefaultObject)

    def getBof(self):
        try:
            if self.iPosition < 0:
                return True
            else:
                return False
        except:
            self.errorCode()
    Bof = property(getBof)

    def getEof(self):
        try:
            if self.iPosition > self.iCounter:
                return True
            else:
                return False
        except:
            self.errorCode()
    Eof = property(getEof)

#    def bof(self):
#        try:
#            if self.iPosition < 0:
#                return True
#            else:
#                return False
#        except:
#            self.errorCode()

#    def eof(self):
#        try:
#            #beginning of file
#            if self.iPosition > self.iCounter:
#                return True
#            else:
#                return False
#        except:
#            self.errorCode()

    def moveFirst(self):
        try:
            #beginning of file
            self.iPosition = 0
        except:
            self.errorCode()
        
    def moveLast(self):
        try:
            #beginning of file
            self.iPosition = self.iCounter
        except:
            self.errorCode()

    def moveNext(self):
        try:
            #beginning of file
            if self.eof() == False:
                self.iPosition = self.iPosition + 1
        except:
            self.errorCode()

    def movePrevious(self):
        try:
            #beginning of file
            if self.bof() == False:
                self.iPosition = self.iPosition - 1
        except:
            self.errorCode()

    def item(self):
        try:
            if self.iPosition >= 0 and self.iPosition <= self.iCounter:
                cTemp = self.lst[self.iPosition]

                return True, cTemp.objObject
            else:
                return False, self.objDefaultObject
        except:
            self.errorCode()

    def noItems(self):
        try:
            return self.iCounter
        except:
            self.errorCode()