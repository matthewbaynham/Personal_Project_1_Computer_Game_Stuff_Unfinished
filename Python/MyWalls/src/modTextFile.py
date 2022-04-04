#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modTextFile"
__module__ = "modTextFile"
__version__ = "0.1"
__bpydoc__ = """
Just the classes that contain all the data
"""

from string import lower
from modBasics import ClsBasics
from Blender import Mathutils
import operator
#import modBasics
#reload(modBasics)
#import fileIO
import curses.ascii
import datetime
import string
import numbers
import StringIO
import modWall
from modBuilding import ClsBuilding
from modDataObjects import ClsFeature, ClsVertex, ClsFace, ClsFeatureVariable
from modMisc import ClsMisc

class ClsTextFile(ClsBasics, ClsMisc):
    __doc__ = """
    iOrder = the order in which the items will be listed
    objObect = what ever we are storing
    """
    def __init__(self, sPath):
        self.initialiseBasicsClass()
        try:
            self.file = open(sPath, "r")
            self.fVersionNo = 0.0
            self.sName = ""
            self.sNotes = ""
            self.sDateCreated = ""
            self.cBuilding = ClsBuilding("")
#            self.lstWalls = []

        except:
            self.errorCode()
        
    def __del__(self):
        try:
            self.file.close()
        except:
            self.errorCode()

    def readData(self):
        try:
            self.lstWalls = []
            sLine = "start"
            sError = ""
            iLineNo = 0

            while not (sLine is None or sLine == ""):
                sLine = self.file.readline()
                sLine = sLine.lower()
                iLineNo = iLineNo + 1

                sTab = chr(curses.ascii.TAB)

                lstElements = sLine.split(sTab)

                iElementCount = self.countItemsInList(lstElements)

                if not iElementCount == 0:
                    if lstElements[0] == "header":
                        for sElement in lstElements:
                            lstComponents = sElement.split("=")
                            iComponentsCounter = self.countItemsInList(lstComponents)

                            if iComponentsCounter == 1:
                                if lstComponents[0] == "version no":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        self.fVersionNo = float(lstComponents[1])
                                    else:
                                        sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": version no is not numeric"
                                elif lstComponents[0] == "name":
                                    self.sName = str(lstComponents[1])
                                    self.cBuilding.sBuildingName = str(lstComponents[1])
                                elif lstComponents[0]== "notes":
                                    self.sNotes = str(lstComponents[1])
                    elif lstElements[0] == "create wall":
                        #Create a wall

                        sName = ""
                        fDefaultHeight = 0.0
                        fThickness = 0.0
                        fLength = 0.0
                        fRotationVertical = 0.0

                        for sElement in lstElements:
                            lstComponents = sElement.split("=")
                            iComponentsCounter = self.countItemsInList(lstComponents)

                            if iComponentsCounter == 2:
                                if lstComponents[0] == "thickness":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fThickness = float(lstComponents[1])
                                    else:
                                        sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": thickness is not numeric"
                                elif lstComponents[0] == "length":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fLength = float(lstComponents[1])
                                    else:
                                        sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": lenght is not numeric"
                                elif lstComponents[0] == "default height":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fDefaultHeight = float(lstComponents[1])
                                    else:
                                        sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": default height is not numeric"
                                elif lstComponents[0] == "name":
                                    sName = str(lstComponents[1])
                                elif lstComponents[0] == "offset":
                                    lstCoordinates = lstComponents[1].split(",")
                                    iCoordinatesCounter = self.countItemsInList(lstCoordinates)

                                    if not iCoordinatesCounter == 3:
                                        bIsOkCoordinates = False
                                        sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": wrong number of Coordinates in the offset, " + str(iCoordinatesCounter) + "given."
                                    else:
                                        bIsOkCoordinates = True

                                        for sChr in [" ", "(", ")", "{", "}", "[", "]", "+"]:
                                            lstCoordinates[0] = lstCoordinates[0].strip(sChr)
                                            lstCoordinates[1] = lstCoordinates[1].strip(sChr)
                                            lstCoordinates[2] = lstCoordinates[2].strip(sChr)

                                        for sTempCoordinate in lstCoordinates:
                                            if not self.isStringNumber(sTempCoordinate):
                                                bIsOkCoordinates = False
                                                sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Not all of the coordinates in the offset are numeric. '" + sTempCoordinate + "'"
                                elif lstComponents[0] == "vertical rotation":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fRotationVertical = float(lstComponents[1])


                        bIsMissingVarible = False
                        if sName == "":
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": missing varible 'name' in wall"
                            bIsMissingVarible = True
                        if fThickness == 0.0:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": missing varible 'thickness' in wall '" + sName + "'"
                            bIsMissingVarible = True
                        if fLength == 0.0:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": missing varible 'length' in wall '" + sName + "'"
                            bIsMissingVarible = True

                        if bIsMissingVarible == False:
                            print "Adding wall"
                            iNextWallId = self.cBuilding.getMaxWallId() + 1
                            self.cBuilding.addWall(iNextWallId, sName, fDefaultHeight, fThickness, fLength, fRotationVertical, lstCoordinates)

                        else:
                            print "missing variables for wall"

                    elif lstElements[0] == "add feature":
                        #add a feature
                        #extra varibles can be included at this point and we can assign them to the feature id
                        #or the varibles can be added later
                        lstVaribles = []

                        bIsFoundName = False
                        bIsFoundWallName = False
                        bIsFoundType = False
                        bIsFoundSubType = False
                        bIsFoundPosHor = False

                        sWallName = ""
                        sName = ""
                        sType = ""
                        sSubType = ""
                        fPosHor = 0.0
                        fPosVert = 0.0
                        fHeight =0.0
                        fWidth = 0.0

                        #first loop through the elements lookig for the compulsary ones
                        for sElement in lstElements:
                            lstComponents = sElement.split("=")
                            iComponentsCounter = self.countItemsInList(lstComponents)

                            if iComponentsCounter == 2:
                                if lstComponents[0] == "name":
                                    sName = str(lstComponents[1])
                                    bIsFoundName = True
                                elif lstComponents[0]== "wall name":
                                    sWallName = str(lstComponents[1])
                                    bIsFoundWallName = True
                                elif lstComponents[0]== "type":
                                    sType = str(lstComponents[1])
                                    bIsFoundType = True
                                elif lstComponents[0]== "sub type":
                                    sSubType = str(lstComponents[1])
                                    bIsFoundSubType = True
                                elif lstComponents[0]== "position horizontally":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fPosHor = float(lstComponents[1])
                                        bIsFoundPosHor = True
                                elif lstComponents[0]== "position vertically":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fPosVert = float(lstComponents[1])
                                elif lstComponents[0]== "height":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fHeight = float(lstComponents[1])
                                elif lstComponents[0]== "width":
                                    if self.isStringNumber(lstComponents[1]) == True:
                                        fWidth = float(lstComponents[1])

                        if bIsFoundName == False:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Missing 'name' in 'add feature'"
                        elif bIsFoundWallName == False:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Missing 'wall name' in 'add feature'"
                        elif bIsFoundType == False:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Missing 'type' in 'add feature'"
                        elif bIsFoundSubType == False and not sType == "divider":
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Missing 'sub type' in 'add feature'"
                        elif bIsFoundPosHor == False:
                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": Missing 'position horizontally' in 'add feature'"
                        else:

                            self.cBuilding.addWallFeature(sWallName, sName, sType, sSubType, fPosHor, fPosVert, fHeight, fWidth)

                            #second loop through the elements looking for the optional elements eg variables
                            for sElement in lstElements:
                                lstComponents = sElement.split("=")
                                iComponentsCounter = self.countItemsInList(lstComponents)

                                if iComponentsCounter == 2:
                                    if lstComponents[0] in ["doorway height", "doorway width", "doorway height of arch centre", "window frame height", \
                                                                "window frame width", "window height", "window width"]:
                                        if self.isStringNumber(lstComponents[1]) == True:
                                            print "Assigning Float variable: " + lstComponents[0]
                                            self.cBuilding.assignWallFeatureVariable(sWallName, sName, lstComponents[0], "float", float(lstComponents[1]))
                                        else:
                                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": " + lstComponents[0] + " not numeric"
                                    elif lstComponents[0] in ["doorway lintol extra vertexes", "extra vertexes", "window lintol extra vertexes horizontal", \
                                                                "window lintol extra vertexes vertical"]:
                                        if self.isStringNumber(lstComponents[1]) == True:
                                            print "Assigning Int variable: " + lstComponents[0]
                                            self.cBuilding.assignWallFeatureVariable(sWallName, sName, lstComponents[0], "int", int(lstComponents[1]))
                                        else:
                                            sError = sError + chr(curses.ascii.CR) + chr(curses.ascii.LF) + "Line No " + str(iLineNo) + ": " + lstComponents[0] + " not numeric"
                                    else:
                                        print "unknown variable '" + lstComponents[0] + "'"
                                else:
                                    print "Element must only have one equals sign '" + sElement + "'"

            if not sError == "":
                bHasError = True
                print "Errors in Text file:" + sError
            else:
                bHasError = False

            return bHasError, self.cBuilding
            self.file.close()
        except:
            self.errorCode()
            self.file.close()
            bHasError = True
            return bHasError, None

