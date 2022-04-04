#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modMisc"
__module__ = "modMisc"
__version__ = "0.1"
__bpydoc__ = """
module that contain some more code
"""

from Blender import NMesh, Mathutils
import math
from modBasics import ClsBasics
from modDataObjects import ClsFeature, ClsVertex, ClsFace, ClsFeatureVariable
import operator
import numbers

class ClsMisc(ClsBasics):
    def getVertexFromList(self, lst, iId):
        try:
            bIsFound = False
            for x in lst:
                if x.iId == iId:
                    bIsFound = True
                    return bIsFound, x
            if bIsFound == False:
                cTempVertex = ClsVertex(0, 0, 0)
                return bIsFound, cTempVertex
        except:
            self.errorCode()

    def countItemsInList(self, lst):
        try:
            iCounter = 0
            for x in lst:
                iCounter = iCounter + 1
            return iCounter
        except:
            self.errorCode()
            return 0

    def isStringNumber(self, sStr):
        try:
            sTemp = sStr

            if sTemp.find("-") == 0:
                if sTemp.find("-", 1) == -1:
                    #begins with a "-" but no other "-"
                    bIsOk = True
                else:
                    #begins with a "-" but also has other "-"
                    bIsOk = False
            else:
                if sTemp.find("-") == -1:
                    #does not begin with "-" and does not contain any "-"
                    bIsOk = True
                else:
                    #does not begin with "-", but does contain more "-"
                    bIsOk = False
                        
            if bIsOk == False:
                return False
            else:
                sTemp = sTemp.replace("0", "")
                sTemp = sTemp.replace("1", "")
                sTemp = sTemp.replace("2", "")
                sTemp = sTemp.replace("3", "")
                sTemp = sTemp.replace("4", "")
                sTemp = sTemp.replace("5", "")
                sTemp = sTemp.replace("6", "")
                sTemp = sTemp.replace("7", "")
                sTemp = sTemp.replace("8", "")
                sTemp = sTemp.replace("9", "")

                if sTemp == "" or sTemp == "." or sTemp == "-" or sTemp == "-.":
                    return True
                else:
                    return False
        except:
            self.errorCode()
            return False