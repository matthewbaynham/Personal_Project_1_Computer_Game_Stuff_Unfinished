#!BPY

__author__ = "Matthew Baynham"
__date__ = "$08-May-2009 12:34:49$"
__name__ = "modBuilding"
__module__ = "modBuilding"
__version__ = "0.1"
__bpydoc__ = """
To Do
=====
1)  Colour and Texture

2)  square Doors
    i)  Check doors can handle extra vertexes on the sides of the doorway

3)  arch doors
    i) create arch door with double curve

4)  tops of walls and ends of the wall,
    i)  add a property to  feature to define if the the top of end if cunnecting side A and side B
    ii) if the feature has this property set then connect the top and side

5)  windows
    i)  arched (round top sqare bottom)
"""

from Blender import NMesh, Mathutils
import math
from modBasics import ClsBasics
from modDataObjects import ClsFeature, ClsVertex, ClsFace, ClsFeatureVariable
import operator
from modMisc import ClsMisc
from modMaths import ClsMaths
import modWall
from modWall import ClsWall

class ClsBuilding(ClsBasics, ClsMaths, ClsMisc):
    #some code just to see if I can write a class
#    global lstFeatures, lstFeatureVariables, lstHorMark
    #lstHorMark = a list of floats relating to vertexes that need to be added to every feature to make a horizontal line

    def __init__(self, sName):
        __doc__ = """
        This Class is going to be a structure such as a biulding, boat, etc.
        It is going to contain Walls, floors, ceils, stairs, etc.
        """
        self.initialiseBasicsClass()
        try:
            self.lstFeatures = []
            self.lstFeatureVariables = []
            self.lstHorMark = []
            self.lstWalls = []
            self.lstFloorCeilSections = []
            self.lstStairs = []
            self.sBuildingName = sName
        except:
            self.errorCode()

    def getName(self):
        return self._sName
    def setName(self, value):
        self._sName = value
    sBuildingName = property(getName, setName)

    def addWall(self, iWallId, sName, fDefaultHeight, fThickness, fLength, fRotationVertical, lstCoordinates):
        try:
            print "adding wall"
            bIsFound = False
            for cTemp in self.lstWalls:
                if cTemp.sName == sName:
                    bIsFound = True
            
            if bIsFound == True:
                print "Error: can't add wall we already have a wall in the building with that same name '" + sName + "'"
            else:
                cWall = None
                cWall = modWall.ClsWall(iWallId, sName, fDefaultHeight, fThickness, fLength)

                if self.countItemsInList(lstCoordinates) == 3:
                    vOffset = Mathutils.Vector(float(lstCoordinates[0]), float(lstCoordinates[1]), float(lstCoordinates[2]))
                    cWall.vOffset = vOffset
                else:
                    print "wrong number of co-ordinates in wall definition"

                cWall.fRotationalVertical = fRotationVertical
#                cWall.iId = iWallId

                print "adding wall 2"
                self.lstWalls.append(cWall)
        except:
            self.errorCode()

    def addWallFeature(self, sWallName, sFeatureName, sType, sSubType, fPosHor, fPosVert, fHeight, fWidth):
        try:
            bIsFound = False
            for cTemp in self.lstWalls:
                if cTemp.sName == sWallName:
#                    iWallId = cTemp.iId
#                    cTemp.addFeature(iWallId, sFeatureName, sType, sSubType, fPosHor, fPosVert, fHeight, fWidth)
                    cTemp.addFeature(sFeatureName, sType, sSubType, fPosHor, fPosVert, fHeight, fWidth)
                    bIsFound = True

            if bIsFound == False:
                print "Can't add feature to wall, wall name unknown '" + sWallName + "'"
        except:
            self.errorCode()

    def assignWallFeatureVariable(self, sWallName, sFeatureName, sVariableName, sVariableType, VariableAmount):
        try:
            bIsOk = True
            bIsFound = False
            for cWall in self.lstWalls:
                if cWall.sName == sWallName:
                    bIsOk, iFeatureId = cWall.getFeatureId(sFeatureName)
                    cWall.addFeatureVariables(iFeatureId, sVariableName, sVariableType, VariableAmount)
                    bIsFound = True
                    print "adding Feature variable: Wall Name: '" + sWallName + "' Feature name: '" + sFeatureName + "' Feature ID: " + str(iFeatureId)
            if bIsFound == False:
                print "Couldn't add Feature Variable, check feature exists"
            if bIsOk == False:
                print "Problems adding Feature Variable.  bIsOk flag raised"
        except:
            self.errorCode()


    def buildBuilding(self):
        try:
            lstVert = NMesh.GetRaw()
            lstClsVert = []
            iVertexCounter = 0

            for cWall in self.lstWalls:
                print "Wall ID " + str(cWall.iId)
                iVertexCounter, lstVert, lstClsVert = cWall.buildWall(iVertexCounter, lstVert, lstClsVert)

            objMyBox = NMesh.PutRaw(lstVert)

            print "Vertexes Counter: " + str(self.countItemsInList(lstClsVert))
        except:
            self.errorCode()

    def getMaxWallId(self):
        try:
            iMaxId = 0
            for cWall in self.lstWalls:
                if cWall.iId > iMaxId:
                    iMaxId = cWall.iId
            return iMaxId
        except:
            self.errorCode()
    fId = property(getMaxWallId)


#    def assignWallVariable(self, sWallName):
#        try:
#            bIsFound = False
#            for cWall in self.lstWalls:
#                if cWall.sName == sWallName:
#
#            cWall =
#            self.lstWalls.append(cWall)
#        except:
#            self.errorCode()
