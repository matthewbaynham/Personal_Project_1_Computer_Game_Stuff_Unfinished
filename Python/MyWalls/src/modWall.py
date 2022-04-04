#!BPY

__author__ = "Matthew Baynham"
__date__ = "$08-May-2009 12:34:49$"
__name__ = "modWall"
__module__ = "modWall"
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

class ClsWall(ClsBasics, ClsMaths, ClsMisc):
    #some code just to see if I can write a class
#    global lstFeatures, lstFeatureVariables, lstHorMark
    #lstHorMark = a list of floats relating to vertexes that need to be added to every feature to make a horizontal line
#    lstFeatures = {}

    __slots__ = ['lstFeatures', 'lstFeatureVariables', 'lstHorMark', 'iId', 'sName', 'fDefaultHeight', 'fThinkness', 'fLength', 'vOffset', 'fRotationalVertical']

    def __init__(self, iWallId, psName, pfDefaultHeight, pfThickness, pfLength):
        __doc__ = """
        Documentation
        """
        self.initialiseBasicsClass()
        try:
            self.sClassName = "ClsWall"
            self.iId = iWallId

            self.sName = psName
            self.fDefaultHeight = pfDefaultHeight
            self.fThinkness = pfThickness
            self.fLength = pfLength
            self.vOffset = Mathutils.Vector(0.0, 0.0, 0.0)
            self.fRotationalVertical = 0

            cFeatureFirst = ClsFeature("bow", "divider", "end of wall", 0, 0, pfDefaultHeight, 0)
            cFeatureFirst.iId = 1
            cFeatureFirst.iWallId = iWallId
            cFeatureLast = ClsFeature("eow", "divider", "end of wall", pfLength, 0, pfDefaultHeight, 0)
            cFeatureLast.iId = 2
            cFeatureLast.iWallId = iWallId
            self.lstFeatures = [cFeatureFirst, cFeatureLast]
            self.lstFeatureVariables = []
            self.lstHorMark = []
        except:
            self.errorCode()

    def getName(self):
        return self._sName
    sName = property(getName)

    def getOffset(self):
        return self._vOffset
    def setOffset(self, value):
        self._vOffset = value
    vOffset = property(getOffset, setOffset)

    def getDefaultHeight(self):
        return self._fDefaultHeight
    def setDefaultHeight(self, value):
        self._fDefaultHeight = float(value)
    fDefaultHeight = property(getDefaultHeight, setDefaultHeight)

    def getThinkness(self):
        return self._fThinkness
    def setThinkness(self, value):
        self._fThinkness = float(value)
    fThinkness = property(getThinkness, setThinkness)

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = value
#        try:
#            self._iId = value
#            #set the id for the wall and for all of the features which have a wallId = -1
#            for cFeature in self.lstFeatures:
#                if cFeature.iWallId == -1:
#                    cFeature.iWallId = value
#        except:
#            self.errorCode()
    iId = property(getId, setId)

    def getLength(self):
        return self._fLength
    def setLength(self, value):
        self._fLength = float(value)
        self.featureMove("eow", value)
    fLength = property(getLength, setLength)

    def getRotationVertical(self):
        return self._fRotationVertical
    def setRotationVertical(self, value):
        self._fRotationVertical = value
    fRotationalVertical = property(getRotationVertical, setRotationVertical)

    def nextUnusedId(self):
        try:
            bIsFound = 'false'
            iId = 0
            while bIsFound == 'true' or iId == 0:
                iId = iId + 1
                bIsFound = 'false'
                for tempFeature in self.lstFeatures:
                    if tempFeature.iId == iId:
                        bIsFound = 'true'
            return iId
        except:
            self.errorCode()

    def addFeature(self, psName, psType, psSubType, pfPosHor, pfPosVert, pfHeight, pfWidth):
        try:
            nextId = self.nextUnusedId()
            tempFeature = ClsFeature(psName, psType, psSubType, pfPosHor, pfPosVert, pfHeight, pfWidth)
            tempFeature.iId = nextId
            tempFeature.iWallId = self.iId
            self.lstFeatures.append(tempFeature)
            return nextId
        except:
            self.errorCode()

    def getMaxVariableId(self):
        try:
            iMax = 0
            for cTemp in self.lstFeatureVariables:
                if cTemp.iId > iMax:
                    iMax = cTemp.iId
            return iMax
        except:
            self.errorCode()

    def isInFeatureVariablesLst(self, iFeatureId, iVariableId=None, sVariableName=None, sVariableType=None):
        try:
            bIsFound = False
            for cTempVariable in self.lstFeatureVariables:
                if cTempVariable.iFeatureId == iFeatureId and (cTempVariable.iId == iVariableId or iVariableId is None) and (cTempVariable.sName == sVariableName or sVariableName is None) and (cTempVariable.sType == sVariableType or sVariableType is None):
                    bIsFound = True
            return bIsFound
        except:
            self.errorCode()
            return False

    def isInFeatureLst(self, iFeatureId):
        try:
            bIsFound = False
            for cTempFeature in self.lstFeatures:
                if cTempFeature.iId == iFeatureId:
                    bIsFound = True
            return bIsFound
        except:
            self.errorCode()
            return False

    def addFeatureVariables(self, iFeatureId, sVariableName, sVariableType, VariableAmount):
        __doc__ = """
        1st returned variable = is error
        2nd returned variable = variable ID
        """
        try:
            if self.isInFeatureLst(iFeatureId) == True:
                if self.isInFeatureVariablesLst(iFeatureId, sVariableName, sVariableType) == True:
                    self.addWarning("We already have this variable")
                    return True, -1
                else:
                    iIdMax = self.getMaxVariableId()
                    cTempVariable = ClsFeatureVariable(iFeatureId, sVariableName, sVariableType, VariableAmount)
                    cTempVariable.iId = iIdMax + 1
                    self.lstFeatureVariables.append(cTempVariable)
                    return False, cTempVariable.iId
            else:
                self.addWarning("Feature ID not Found " + str(iFeatureId))
                return True, -1
        except:
            self.errorCode()
            return True, -1

    def editFeatureVariables(self, iFeatureId, VariableAmount, iVariableId=None, sVariableName=None, sVariableType=None):
        try:
            bIsFound = False
            for cTempVariable in self.lstFeatureVariables:
                if cTempVariable.iFeatureId == iFeatureId and (cTempVariable.sName == sVariableName or sVariableName is None) and (cTempVariable.sType == sVariableType or sVariableType is None):
                    cTempVariable.Amount = VariableAmount
                    bIsFound = True
            if bIsFound == False:
                self.addWarning("Couldn't find variable when trying to edit it")
        except:
            self.errorCode()

    def getFeatureVariables(self, iFeatureId, iVariableId=None, sVariableName=None, sVariableType=None):
        try:
            bIsFound = False
            for cTempVariable in self.lstFeatureVariables:
                print "Variable Name: '" + cTempVariable.sName + "'"
                if cTempVariable.iFeatureId == iFeatureId and (cTempVariable.iId == iVariableId or iVariableId is None) and (cTempVariable.sName == sVariableName or sVariableName is None) and (cTempVariable.sType == sVariableType or sVariableType is None):
                    bIsFound = True
                    return True, cTempVariable.Amount
            if bIsFound == False:
                print "Couldn't find variable when trying to get the amount" + sVariableName
                self.addWarning("Couldn't find variable when trying to get the amount")
                return False, None
        except:
            self.errorCode()
            return False, None

    def getFeatureId(self, sName):
        try:
            bIsFound = False
            for cFeature in self.lstFeatures:
                if cFeature.sName == sName:
                    bIsFound = True
                    return True, cFeature.iId
            if bIsFound == False:
                self.addWarning("Couldn't find Feature")
                return False, -1
        except:
            self.errorCode()
            return False, None

    def featureMoveHor(self, psName, pfNewPosHor):
        try:
            for tempFeature in self.lstFeatures:
                if tempFeature.Name == psName:
                    tempFeature.fPosHor = pfNewPosHor
        except:
            self.errorCode()

    def featureMoveVert(self, psName, pfNewPosVert):
        try:
            for tempFeature in self.lstFeatures:
                if tempFeature.Name == psName:
                    tempFeature.fPosVert = pfNewPosVert
        except:
            self.errorCode()

    def featureMove(self, psName, pfNewPosHor, pfNewPosVert):
        try:
            for tempFeature in self.lstFeatures:
                if tempFeature.Name == psName:
                    tempFeature.fPosHor = pfNewPosHor
                    tempFeature.fPosVert = pfNewPosVert
        except:
            self.errorCode()

    def featureDelete(self, iId):
        try:
            for tempFeature in self.lstFeatures:
                if tempFeature.iId == iId:
                    self.lstFeatures.remove(tempFeature)
        except:
            self.errorCode()

#    def checkDividers(self):
#        __doc__ = """
#        at least every other feature has to be a "divider" or a "end of wall"
#        you can have consecutive dividers but you can not have any other consecutive feature
#        all other features will be mapped to dividers
#        """
#        try:
#            self.sortFeatures()
#            previousFeature = self.lstFeatures(0)
#            for tempFeature in self.lstFeatures:
#                if not (previousFeature.sType == "divider"  and tempFeature.sType == "divider"):
#                    #problem: there are two features next to eachother where neither one is a divider or a end of wall
#                    #we need to add a divider half way between then and then sort the lstFeatures and recheck
#                    self.addFeature("", "divider", ((previousFeature.fPosHor + tempFeature.fPosHor) / 2), 0, 0, 0)
#        except:
#            self.errorCode()

    def sortFeatures(self):
        __doc__ = """
        the sort method will not owrk on this list because there is no way of
        defining the key to be a property of the class that is stored in the list
        """
        try:
            self.lstFeatures.sort(key=operator.attrgetter('fPosHor'))
        except:
            self.errorCode()

    def getFeatureHeight(self, cFeature):
        try:
            #if the feature has a none zero Height then return that
            #if the feature has a zero Height loop though the list of features
            #    to find the lossest feature in each direction which has a none zero Height
            #    calculate to Height that the current feature needs to line up with the Heights of the other features
            self.sClassStep = "getFeatureHeight"

            fLowerHeight = 0
            fLowerPos = 0
            fUpperHeight = 0
            fUpperPos = 0
            if cFeature.fHeight == 0:
                for cTempFeature in self.lstFeatures:
                    if not cTempFeature.fHeight == 0:
                        if cTempFeature.fPosHor < cFeature.fPosHor:
                            if cTempFeature.fPosHor > fLowerPos:
                                fLowerPos = cTempFeature.fPosHor
                                fLowerHeight = cTempFeature.fHeight
                        elif cTempFeature.fPosHor > cFeature.fPosHor:
                            if cTempFeature.fPosHor < fLowerPos or fLowerPos == 0:
                                fUpperPos = cTempFeature.fPosHor
                                fUpperHeight = cTempFeature.fHeight
                if fLowerPos == fUpperPos:
                    self.sClassMessage = "getFeaturePosition just went wrong the lower and upper features which have specified Heights are the same position in the wall"
                    return 0
                else:
                    return fLowerHeight + (cFeature.fPosHor - fLowerPos) * (fLowerHeight - fUpperHeight) / (fLowerPos - fUpperPos)
            else:
                return cFeature.fHeight
        except:
            self.errorCode()

    def lowestVertexInList(self, lst, fMinHeight, sSide):
        __doc__ = """
        returns boolean true = vertex is found
        returns the actual vertex
        """
        try:
            #find any vertex above min Height
            #find lowest vertex
            bIsFoundVertexAboveMin = False
            for cVertex in lst:
                if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight:
                    cTempVertex = cVertex
                    bIsFoundVertexAboveMin = True

            if bIsFoundVertexAboveMin == True:
                for cVertex in lst:
                    if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight and cVertex.fZ < cTempVertex.fZ:
                        cTempVertex = cVertex
                return True, cTempVertex
            else:
                cNoneVertex = ClsVertex(0, 0, 0)
                return False, cNoneVertex
        except:
            self.errorCode()

    def lowestVertexInTwoLists(self, lstOne, lstTwo, fMinHeight, lstExceptions, sSide):
        __doc__ = """
        returns boolean true = vertex is found
        returns the actual vertex
        """
        try:
            #find any vertex above min Height
            #find lowest vertex
            bIsFoundVertexAboveMin = False

            for cVertex in lstOne:
                if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight and not self.isInVertexLst(lstExceptions, cVertex.iId):
                    cTempVertex = cVertex
                    bIsFoundVertexAboveMin = True

            for cVertex in lstTwo:
                if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight and not self.isInVertexLst(lstExceptions, cVertex.iId):
                    cTempVertex = cVertex
                    bIsFoundVertexAboveMin = True

            if bIsFoundVertexAboveMin == True:
                for cVertex in lstOne:
                    if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight and cVertex.fZ < cTempVertex.fZ and not self.isInVertexLst(lstExceptions, cVertex.iId):
                        cTempVertex = cVertex
                for cVertex in lstTwo:
                    if cVertex.sSide == sSide and cVertex.fZ >= fMinHeight and cVertex.fZ < cTempVertex.fZ and not self.isInVertexLst(lstExceptions, cVertex.iId):
                        cTempVertex = cVertex
                return True, cTempVertex
            else:
                cNoneVertex = ClsVertex(0, 0, 0)
                return False, cNoneVertex
        except:
            self.errorCode()

    def isInVertexLst(self, lstVertex, iId):
        __doc__ = """
        Checks to see a vertex is in the list of vertexes from the ID
        """
        try:
            bIsFound = False
            for cVert in lstVertex:
                if cVert.iId == iId:
                    bIsFound = True
            return bIsFound
        except:
            self.errorCode()

    def addVertexesDivider(self, cFeature, iVertexCounter, lstVert, lstClsVert):
        try:
            if not self.iId == cFeature.iWallId:
                print "Different Id's: Divider"

            self.sClassSubStep = "Divider"
            self.sClassUsefulValue = "Feature ID " + str(cFeature.iId)

            self.sClassMessage = "bottom of the divider, side a"
            #bottom of the divider, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            self.sClassMessage = "top of the divider, side a"
            #top of the divider, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            self.sClassMessage = "bottom of the divider, side b"
            #bottom of the divider, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            self.sClassMessage = "top of the divider, side b"
            #top of the divider, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            bIsFound, iVertexNo = self.getFeatureVariables(cFeature.iId, sVariableName="extra vertexes")

            iCounter = 0
            if bIsFound == True:
                while iCounter < iVertexNo:
                    iCounter = iCounter + 1

                    self.sClassMessage = "Extra vertex, side a"
                    #top of the divider, side a
                    cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fHeight * iCounter / (iVertexNo + 1))
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "middle"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    self.sClassMessage = "Extra Vertex, side b"
                    #top of the divider, side b
                    cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fHeight * iCounter / (iVertexNo + 1))
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "middle"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

            if not self.lstHorMark is []:
                for fHeight in self.lstHorMark:
                    self.sClassMessage = "Extra vertex, side a"
                    #top of the divider, side a
                    cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "middle"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    self.sClassMessage = "Extra Vertex, side b"
                    #top of the divider, side b
                    cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "middle"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)


            return iVertexCounter
        except:
            self.errorCode()
            return iVertexCounter

    def addVertexesDoor(self, cFeature, iVertexCounter, lstVert, lstClsVert):
        try:
            if not self.iId == cFeature.iWallId:
                print "Different Id's: door"
            
            cVertexLintolFirstAEnd = None
            cVertexLintolFirstAStart = None
            cVertexLintolFirstATop = None
            cVertexLintolFirstBEnd = None
            cVertexLintolFirstBStart = None
            cVertexLintolFirstBTop = None
            
            cVertexLintolLastAEnd = None
            cVertexLintolLastAStart = None
            cVertexLintolLastATop = None
            cVertexLintolLastBEnd = None
            cVertexLintolLastBStart = None
            cVertexLintolLastBTop = None

            cVertexTopFeatureA = None
            cVertexTopFeatureB = None

            lstDoorwayVertexesSideAStart = None
            lstDoorwayVertexesSideBStart = None
            lstDoorwayVertexesSideAEnd = None
            lstDoorwayVertexesSideBEnd = None
            lstDoorwayVertexesSideATop = None
            lstDoorwayVertexesSideBTop = None

            lstDoorwayVertexesSideAStart = []
            lstDoorwayVertexesSideBStart = []
            lstDoorwayVertexesSideAEnd = []
            lstDoorwayVertexesSideBEnd = []
            lstDoorwayVertexesSideATop = []
            lstDoorwayVertexesSideBTop = []

            self.sClassSubStep = "Door"
            #Note: "top of the feature" means the top of the wall and NOT the top of the doorway
            self.sClassMessage = "top of the feature, side a"
            #top of the feature, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureA = cTempVertex

            self.sClassMessage = "top of the feature, side b"
            #top of the feature, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)

            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureB = cTempVertex

            bIsFoundDoorwayWidth, fDoorwayWidth = self.getFeatureVariables(cFeature.iId, sVariableName="doorway width")
            bIsFoundDoorwayHeight, fDoorwayHeight = self.getFeatureVariables(cFeature.iId, sVariableName="doorway height")
            bIsFoundLintolExtraVertexes, fLintolExtraVertexes = self.getFeatureVariables(cFeature.iId, sVariableName="doorway lintol extra vertexes")

            if bIsFoundDoorwayWidth == False:
                print "Need to have a width for this door"

            if bIsFoundDoorwayHeight == False:
                print "Need to have a height for this door"

            if bIsFoundDoorwayWidth == True and bIsFoundDoorwayHeight == True:
                self.sClassMessage = "bottom of the doorway, side 'a' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                lstDoorwayVertexesSideAStart.append(cTempVertex)

                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                cVertexLintolFirstAStart = cTempVertex

                self.sClassMessage = "bottom of the doorway, side 'a' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                lstDoorwayVertexesSideAEnd.append(cTempVertex)

                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                cVertexLintolFirstAEnd = cTempVertex

                self.sClassMessage = "bottom of the doorway, side 'b' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                lstDoorwayVertexesSideBStart.append(cTempVertex)

                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                cVertexLintolFirstBStart = cTempVertex

                self.sClassMessage = "bottom of the doorway, side 'b' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                lstDoorwayVertexesSideBEnd.append(cTempVertex)

                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                cVertexLintolFirstBEnd = cTempVertex

                if cFeature.sSubType == "square":
                    self.sClassMessage = "top of the doorway, side 'a' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fDoorwayHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "start"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    lstDoorwayVertexesSideAStart.append(cTempVertex)
                    lstDoorwayVertexesSideATop.append(cTempVertex)

                    cVertexLintolLastAStart = cTempVertex
                    cVertexLintolFirstATop = cTempVertex

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    self.sClassMessage = "top of the doorway, side 'a' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fDoorwayHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "end"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    lstDoorwayVertexesSideAEnd.append(cTempVertex)
                    lstDoorwayVertexesSideATop.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    cVertexLintolLastAEnd = cTempVertex
                    cVertexLintolLastATop = cTempVertex

                    self.sClassMessage = "top of the doorway, side 'b' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fDoorwayHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "start"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    lstDoorwayVertexesSideBStart.append(cTempVertex)
                    lstDoorwayVertexesSideBTop.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    cVertexLintolLastBStart = cTempVertex
                    cVertexLintolFirstBTop = cTempVertex

                    self.sClassMessage = "top of the doorway, side 'b' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + fDoorwayHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "end"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    lstDoorwayVertexesSideBEnd.append(cTempVertex)
                    lstDoorwayVertexesSideBTop.append(cTempVertex)

                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    cVertexLintolLastBEnd = cTempVertex
                    cVertexLintolLastBTop = cTempVertex

                    if bIsFoundLintolExtraVertexes == True:
                        iLintolVertexCounter = 0

                        iVertexFirstAId = cVertexLintolFirstATop.iId
                        iVertexFirstBId = cVertexLintolFirstBTop.iId

                        while iLintolVertexCounter < fLintolExtraVertexes:
                            iLintolVertexCounter = iLintolVertexCounter + 1

                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol, side A"
                            cTempVertex = ClsVertex(cVertexLintolFirstATop.fX + iLintolVertexCounter * (cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) / (fLintolExtraVertexes + 1),
                                cVertexLintolFirstATop.fY + iLintolVertexCounter * (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY) / (fLintolExtraVertexes + 1),
                                self.vOffset.z + fDoorwayHeight)
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            lstDoorwayVertexesSideATop.append(cTempVertex)

                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            iVertexSecondAId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol, side B"
                            cTempVertex = ClsVertex(cVertexLintolFirstBTop.fX + iLintolVertexCounter * (cVertexLintolLastBTop.fX - cVertexLintolFirstBTop.fX) / (fLintolExtraVertexes + 1),
                                cVertexLintolFirstBTop.fY + iLintolVertexCounter * (cVertexLintolLastBTop.fY - cVertexLintolFirstBTop.fY) / (fLintolExtraVertexes + 1),
                                self.vOffset.z + fDoorwayHeight)
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            lstDoorwayVertexesSideBTop.append(cTempVertex)

                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            iVertexSecondBId = cTempVertex.iId

                            #####################################################################################################################
                            #   Still need to create all the faces with these extra vertexes in the lintol and down the side of the door frame  #
                            #####################################################################################################################

                            #Side A: above door
                            cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexFirstAId, iVertexSecondAId])
                            cTempFace.iId = cFeature.faceMaxId() + 1

                            cFeature.addFace(cTempFace)

                            #Side B: above door
                            cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexFirstBId, iVertexSecondBId])
                            cTempFace.iId = cFeature.faceMaxId() + 1

                            cFeature.addFace(cTempFace)

                            iVertexFirstAId = iVertexSecondAId
                            iVertexFirstBId = iVertexSecondBId

                        #Side A: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexSecondAId, cVertexLintolLastATop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)

                        #Side B: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexSecondBId, cVertexLintolLastBTop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)
                    else:
                        #No extra vertexes in the lintol
                        #Side A: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, cVertexLintolFirstATop.iId, cVertexLintolLastATop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)

                        #Side B: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, cVertexLintolFirstBTop.iId, cVertexLintolLastBTop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)

                    bIsFirstVariablesSet = True

                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideATop, lstDoorwayVertexesSideBTop, "flat", True, cVertexLintolFirstATop.iId, cVertexLintolLastATop.iId, cVertexLintolFirstBTop.iId, cVertexLintolLastBTop.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideAStart, lstDoorwayVertexesSideBStart, "flat", True, cVertexLintolFirstAStart.iId, cVertexLintolLastAStart.iId, cVertexLintolFirstBStart.iId, cVertexLintolLastBStart.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideAEnd, lstDoorwayVertexesSideBEnd, "flat", True, cVertexLintolFirstAEnd.iId, cVertexLintolLastAEnd.iId, cVertexLintolFirstBEnd.iId, cVertexLintolLastBEnd.iId)
#############################################################################
###                                                                       ###
###                          Single  arch                                 ###
###                                                                       ###
#############################################################################
                elif cFeature.sSubType == "single arch":
#                    bIsFoundLintolExtraVertexes, fLintolExtraVertexes = self.getFeatureVariables(cFeature.iId, iVariableId=None, sVariableName=None, sVariableType="doorway lintol extra vertexes")
                    bIsFoundHeightOfArchCentre, fHeightOfArchCentre = self.getFeatureVariables(cFeature.iId, sVariableName="doorway height of arch centre")

                    if bIsFoundHeightOfArchCentre == False:
                        print "Can't find variable 'doorway height of arch centre'"

                    if fDoorwayHeight - fHeightOfArchCentre == fDoorwayWidth / 2:
                        fRadius = fDoorwayWidth / 2
                        fMaxAngle = math.pi / 2
                    if fDoorwayHeight - fHeightOfArchCentre > fDoorwayWidth / 2:
                        fRadius = fDoorwayHeight - fHeightOfArchCentre
#                        fMaxAngle = math.atan(2 * fDoorwayWidth / fRadius)
                        fMaxAngle = math.asin((fDoorwayWidth / 2 ) / fRadius)
                    else:
                        self.addWarning("Arch was to low")
                        fRadius = fDoorwayWidth / 2
                        fMaxAngle = math.pi / 2

                    if bIsFoundLintolExtraVertexes == False:
                        self.addWarning("Trying to make and arch without extra vertexes, it's all going to be sqare.")
                    else:
                        fAngle = -1 * fMaxAngle
                        fAngleIncreaments = 2 * fMaxAngle / (fLintolExtraVertexes + 1)

                        self.sClassMessage = "top of the doorway, side 'a' of wall, 'start' side of doorway"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fMaxAngle)))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        lstDoorwayVertexesSideAStart.append(cTempVertex)
                        lstDoorwayVertexesSideATop.append(cTempVertex)

                        cVertexLintolLastAStart = cTempVertex
                        cVertexLintolFirstATop = cTempVertex

                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        self.sClassMessage = "top of the doorway, side 'b' of wall, 'start' side of doorway"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fMaxAngle)))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        lstDoorwayVertexesSideBStart.append(cTempVertex)
                        lstDoorwayVertexesSideBTop.append(cTempVertex)

                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        cVertexLintolLastBStart = cTempVertex
                        cVertexLintolFirstBTop = cTempVertex

                        self.sClassMessage = "top of the doorway, side 'a' of wall, 'end' side of doorway"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fMaxAngle)))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        lstDoorwayVertexesSideAEnd.append(cTempVertex)
                        lstDoorwayVertexesSideATop.append(cTempVertex)

                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        cVertexLintolLastAEnd = cTempVertex
                        cVertexLintolLastATop = cTempVertex

                        self.sClassMessage = "top of the doorway, side 'b' of wall, 'end' side of doorway"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fDoorwayWidth / 2) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fDoorwayWidth / 2) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fMaxAngle)))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        lstDoorwayVertexesSideBEnd.append(cTempVertex)
                        lstDoorwayVertexesSideBTop.append(cTempVertex)

                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        cVertexLintolLastBEnd = cTempVertex
                        cVertexLintolLastBTop = cTempVertex

                        iLintolVertexCounter = 0

                        iVertexFirstAId = cVertexLintolFirstATop.iId
                        iVertexFirstBId = cVertexLintolFirstBTop.iId

                        fCompondentX = (cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) / math.sqrt((cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) * (cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) + (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY) * (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY))
                        fCompondentY = (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY) / math.sqrt((cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) * (cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) + (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY) * (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY))

                        while iLintolVertexCounter < fLintolExtraVertexes:
                            iLintolVertexCounter = iLintolVertexCounter + 1
                            fAngle = fAngle + fAngleIncreaments

                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol, side A"
                            cTempVertex = ClsVertex(cVertexLintolFirstATop.fX + (cVertexLintolLastATop.fX - cVertexLintolFirstATop.fX) / 2 + fCompondentX * fRadius * math.sin(fAngle),
                                cVertexLintolFirstATop.fY + (cVertexLintolLastATop.fY - cVertexLintolFirstATop.fY) / 2 + fCompondentY * fRadius * math.sin(fAngle),
                                self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fAngle)))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            lstDoorwayVertexesSideATop.append(cTempVertex)

                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            iVertexSecondAId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol, side B"
                            cTempVertex = ClsVertex(cVertexLintolFirstBTop.fX + (cVertexLintolLastBTop.fX - cVertexLintolFirstBTop.fX) / 2 + fCompondentX * fRadius * math.sin(fAngle),
                                cVertexLintolFirstBTop.fY + (cVertexLintolLastBTop.fY - cVertexLintolFirstBTop.fY) / 2 + fCompondentY * fRadius * math.sin(fAngle),
                                self.vOffset.z + fHeightOfArchCentre + (fRadius * math.cos(fAngle)))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            lstDoorwayVertexesSideBTop.append(cTempVertex)

                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            iVertexSecondBId = cTempVertex.iId

                            #####################################################################################################################
                            #   Still need to create all the faces with these extra vertexes in the lintol and down the side of the door frame  #
                            #####################################################################################################################

                            #Side A: above door
                            cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexFirstAId, iVertexSecondAId])
                            cTempFace.iId = cFeature.faceMaxId() + 1

                            cFeature.addFace(cTempFace)

                            #Side B: above door
                            cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexFirstBId, iVertexSecondBId])
                            cTempFace.iId = cFeature.faceMaxId() + 1

                            cFeature.addFace(cTempFace)

                            iVertexFirstAId = iVertexSecondAId
                            iVertexFirstBId = iVertexSecondBId

                        #Side A: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexSecondAId, cVertexLintolLastATop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)

                        #Side B: above door
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexSecondBId, cVertexLintolLastBTop.iId])
                        cTempFace.iId = cFeature.faceMaxId() + 1

                        cFeature.addFace(cTempFace)

                    bIsFirstVariablesSet = True

                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideATop, lstDoorwayVertexesSideBTop, "flat", True, cVertexLintolFirstATop.iId, cVertexLintolLastATop.iId, cVertexLintolFirstBTop.iId, cVertexLintolLastBTop.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideAStart, lstDoorwayVertexesSideBStart, "flat", True, cVertexLintolFirstAStart.iId, cVertexLintolLastAStart.iId, cVertexLintolFirstBStart.iId, cVertexLintolLastBStart.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstDoorwayVertexesSideAEnd, lstDoorwayVertexesSideBEnd, "flat", True, cVertexLintolFirstAEnd.iId, cVertexLintolLastAEnd.iId, cVertexLintolFirstBEnd.iId, cVertexLintolLastBEnd.iId)
                else:
                    print "doorway missing variables"
                    print "    door name " + cFeature.sName

                    self.sClassMessage = "doorway missing variables"
                    self.sClassUsefulValue = "    door name " + cFeature.sName





            del cVertexLintolFirstAEnd
            del cVertexLintolFirstAStart
            del cVertexLintolFirstATop
            del cVertexLintolFirstBEnd
            del cVertexLintolFirstBStart
            del cVertexLintolFirstBTop

            del cVertexLintolLastAEnd
            del cVertexLintolLastAStart
            del cVertexLintolLastATop
            del cVertexLintolLastBEnd
            del cVertexLintolLastBStart
            del cVertexLintolLastBTop

            del cVertexTopFeatureA
            del cVertexTopFeatureB

            del lstDoorwayVertexesSideAStart
            del lstDoorwayVertexesSideBStart
            del lstDoorwayVertexesSideAEnd
            del lstDoorwayVertexesSideBEnd
            del lstDoorwayVertexesSideATop
            del lstDoorwayVertexesSideBTop





            return iVertexCounter
        except:
            self.errorCode()
            return iVertexCounter

    def addVertexesWindow(self, cFeature, iVertexCounter, lstVert, lstClsVert):
        try:
            if not self.iId == cFeature.iWallId:
                print "Different Id's: Window"

            if cFeature.sSubType == "square":
                print "square"
                iVertexCounter = self.addVertexesWindowSquare(cFeature, iVertexCounter, lstVert, lstClsVert)
            elif cFeature.sSubType == "round":
                print "round"
                iVertexCounter = self.addVertexesWindowRound(cFeature, iVertexCounter, lstVert, lstClsVert)

            return iVertexCounter
        except:
            self.errorCode()
            return iVertexCounter

    def addVertexesWindowSquare(self, cFeature, iVertexCounter, lstVert, lstClsVert):
        try:
            #all windows of every style start off square
            #if the style is square we just add the sill
            #if the style is not square then we add extra vertexes to connect to the square outline
            lstWindowFrameVertexesSideAStart = []
            lstWindowFrameVertexesSideBStart = []
            lstWindowFrameVertexesSideAEnd = []
            lstWindowFrameVertexesSideBEnd = []
            lstWindowFrameVertexesSideATop = []
            lstWindowFrameVertexesSideBTop = []
            lstWindowFrameVertexesSideABottom = []
            lstWindowFrameVertexesSideBBottom = []

            self.sClassSubStep = "Window"
            #Note: "top of the feature" means the top of the wall and NOT the top of the doorway
            self.sClassMessage = "top of the feature, side a"
            #top of the feature, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureA = cTempVertex

            self.sClassMessage = "top of the feature, side b"
            #top of the feature, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureB = cTempVertex

            self.sClassMessage = "bottom of the feature, side a"
            #top of the feature, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexBottomFeatureA = cTempVertex

            self.sClassMessage = "bottom of the feature, side b"
            #top of the feature, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexBottomFeatureB = cTempVertex






            bIsFoundWindowFrameWidth, fWindowFrameWidth = self.getFeatureVariables(cFeature.iId, sVariableName="window frame width")
            bIsFoundWindowFrameHeight, fWindowFrameHeight = self.getFeatureVariables(cFeature.iId, sVariableName="window frame Height")
            bIsFoundLintolExtraVertexesHorizontal, fLintolExtraVertexesHorizontal = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes horizontal")
            bIsFoundLintolExtraVertexesVertical, fLintolExtraVertexesVertical = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes vertical")

            if bIsFoundWindowFrameWidth == True and bIsFoundWindowFrameHeight == True:
                self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAStart.append(cTempVertex)
                lstWindowFrameVertexesSideABottom.append(cTempVertex)
                cVertexFrameLastAStart = cTempVertex
                cVertexFrameFirstABottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                lstWindowFrameVertexesSideABottom.append(cTempVertex)
                cVertexFrameLastAEnd = cTempVertex
                cVertexFrameLastABottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBStart.append(cTempVertex)
                lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                cVertexFrameLastBStart = cTempVertex
                cVertexFrameFirstBBottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                cVertexFrameLastBEnd = cTempVertex
                cVertexFrameLastBBottom = cTempVertex







                self.sClassMessage = "top of the window frame, side 'a' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAStart.append(cTempVertex)
                lstWindowFrameVertexesSideATop.append(cTempVertex)
                cVertexFrameFirstAStart = cTempVertex
                cVertexFrameFirstATop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'a' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                lstWindowFrameVertexesSideATop.append(cTempVertex)
                cVertexFrameFirstAEnd = cTempVertex
                cVertexFrameLastATop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'b' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBStart.append(cTempVertex)
                lstWindowFrameVertexesSideBTop.append(cTempVertex)
                cVertexFrameFirstBStart = cTempVertex
                cVertexFrameFirstBTop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'b' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                lstWindowFrameVertexesSideBTop.append(cTempVertex)
                cVertexFrameFirstBEnd = cTempVertex
                cVertexFrameLastBTop = cTempVertex






                if bIsFoundLintolExtraVertexesHorizontal == True:
                    iLintolVertexCounter = 0

                    iVertexFirstATopId = cVertexFrameFirstATop.iId
                    iVertexFirstBTopId = cVertexFrameFirstBTop.iId
                    iVertexFirstABottomId = cVertexFrameFirstABottom.iId
                    iVertexFirstBBottomId = cVertexFrameFirstBBottom.iId

                    while iLintolVertexCounter < fLintolExtraVertexesHorizontal:
                        iLintolVertexCounter = iLintolVertexCounter + 1

                        #Top of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol, side A"
                        cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + iLintolVertexCounter * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX) / (fLintolExtraVertexesHorizontal + 1),
                            cVertexFrameFirstATop.fY + iLintolVertexCounter * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY) / (fLintolExtraVertexesHorizontal + 1),
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideATop.append(cTempVertex)
                        iVertexSecondATopId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol, side B"
                        cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + iLintolVertexCounter * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX) / (fLintolExtraVertexesHorizontal + 1),
                            cVertexFrameFirstBTop.fY + iLintolVertexCounter * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY) / (fLintolExtraVertexesHorizontal + 1),
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBTop.append(cTempVertex)
                        iVertexSecondBTopId = cTempVertex.iId

                        #bottom of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol, side A"
                        cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + iLintolVertexCounter * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX) / (fLintolExtraVertexesHorizontal + 1),
                            cVertexFrameFirstATop.fY + iLintolVertexCounter * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY) / (fLintolExtraVertexesHorizontal + 1),
                            self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideABottom.append(cTempVertex)
                        iVertexSecondABottomId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol, side B"
                        cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + iLintolVertexCounter * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX) / (fLintolExtraVertexesHorizontal + 1),
                            cVertexFrameFirstBTop.fY + iLintolVertexCounter * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY) / (fLintolExtraVertexesHorizontal + 1),
                            self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                        iVertexSecondBBottomId = cTempVertex.iId

                        #####################################################################################################################
                        #   Still need to create all the faces with these extra vertexes in the lintol and down the side of the door frame  #
                        #####################################################################################################################

                        #Side A: above window
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexFirstATopId, iVertexSecondATopId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        #Side B: above window
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexFirstBTopId, iVertexSecondBTopId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        iVertexFirstATopId = iVertexSecondATopId
                        iVertexFirstBTopId = iVertexSecondBTopId

                        #Side A: below window
                        cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, iVertexFirstABottomId, iVertexSecondABottomId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        #Side B: below window
                        cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, iVertexFirstBBottomId, iVertexSecondBBottomId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        iVertexFirstABottomId = iVertexSecondABottomId
                        iVertexFirstBBottomId = iVertexSecondBBottomId

                    #Side A: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexSecondATopId, cVertexFrameLastATop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexSecondBTopId, cVertexFrameLastBTop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side A: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, iVertexSecondABottomId, cVertexFrameLastABottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, iVertexSecondBBottomId, cVertexFrameLastBBottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)
                else:
                    #No extra vertexes in the lintol
                    #Side A: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, cVertexFrameFirstATop.iId, cVertexFrameLastATop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, cVertexFrameFirstBTop.iId, cVertexFrameLastBTop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side A: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, cVertexFrameFirstABottom.iId, cVertexFrameLastABottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, cVertexFrameFirstBBottom.iId, cVertexFrameLastBBottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)







                if bIsFoundLintolExtraVertexesVertical == True:
                    iLintolVertexCounter = 0

                    iVertexFirstAStartId = cVertexFrameFirstAStart.iId
                    iVertexFirstBStartId = cVertexFrameFirstBStart.iId
                    iVertexFirstAEndId = cVertexFrameFirstAEnd.iId
                    iVertexFirstBEndId = cVertexFrameFirstBEnd.iId

                    while iLintolVertexCounter < fLintolExtraVertexesVertical:
                        iLintolVertexCounter = iLintolVertexCounter + 1

                        #Start of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideAStart.append(cTempVertex)
                        iVertexSecondAStartId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBStart.append(cTempVertex)
                        iVertexSecondBStartId = cTempVertex.iId

                        #end of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                        iVertexSecondAEndId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                        iVertexSecondBEndId = cTempVertex.iId





                self.addFacesSill(lstVert, lstClsVert, lstWindowFrameVertexesSideATop, lstWindowFrameVertexesSideBTop, "flat", True, cVertexFrameFirstATop.iId, cVertexFrameLastATop.iId, cVertexFrameFirstBTop.iId, cVertexFrameLastBTop.iId)
                self.addFacesSill(lstVert, lstClsVert, lstWindowFrameVertexesSideAStart, lstWindowFrameVertexesSideBStart, "flat", True, cVertexFrameFirstAStart.iId, cVertexFrameLastAStart.iId, cVertexFrameFirstBStart.iId, cVertexFrameLastBStart.iId)
                self.addFacesSill(lstVert, lstClsVert, lstWindowFrameVertexesSideAEnd, lstWindowFrameVertexesSideBEnd, "flat", True, cVertexFrameFirstAEnd.iId, cVertexFrameLastAEnd.iId, cVertexFrameFirstBEnd.iId, cVertexFrameLastBEnd.iId)
                self.addFacesSill(lstVert, lstClsVert, lstWindowFrameVertexesSideABottom, lstWindowFrameVertexesSideBBottom, "flat", True, cVertexFrameFirstABottom.iId, cVertexFrameLastABottom.iId, cVertexFrameFirstBBottom.iId, cVertexFrameLastBBottom.iId)

            return iVertexCounter
        except:
            self.errorCode()
            return iVertexCounter

    def addVertexesWindowRound(self, cFeature, iVertexCounter, lstVert, lstClsVert):
        try:
            fVertexRatio = 3.0 #the number of vertexes in the frame compared to the vertexes in the lintol

            #all windows of every style start off square
            #if the style is square we just add the sill
            #if the style is not square then we add extra vertexes to connect to the square outline
            lstWindowFrameVertexesSideAStart = []
            lstWindowFrameVertexesSideBStart = []
            lstWindowFrameVertexesSideAEnd = []
            lstWindowFrameVertexesSideBEnd = []
            lstWindowFrameVertexesSideATop = []
            lstWindowFrameVertexesSideBTop = []
            lstWindowFrameVertexesSideABottom = []
            lstWindowFrameVertexesSideBBottom = []

            self.sClassSubStep = "Window"
            #Note: "top of the feature" means the top of the wall and NOT the top of the doorway
            self.sClassMessage = "top of the feature, side a"
            #top of the feature, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureA = cTempVertex

            self.sClassMessage = "top of the feature, side b"
            #top of the feature, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z + cFeature.fHeight)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexTopFeatureB = cTempVertex

            self.sClassMessage = "bottom of the feature, side a"
            #top of the feature, side a
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "a"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexBottomFeatureA = cTempVertex

            self.sClassMessage = "bottom of the feature, side b"
            #top of the feature, side b
            cTempVertex = ClsVertex(self.vOffset.x + cFeature.fPosHor * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                self.vOffset.y + cFeature.fPosHor * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                self.vOffset.z)
            cTempVertex.iFeatureId = cFeature.iId
            cTempVertex.iWallId = self.iId
            cTempVertex.sOrientation = "middle"
            cTempVertex.sSide = "b"
            cTempVertex.iId = iVertexCounter
            iVertexCounter = iVertexCounter + 1
            lstClsVert.append(cTempVertex)
            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
            lstVert.verts.append(objVert)

            cVertexBottomFeatureB = cTempVertex


            bIsFoundWindowFrameWidth, fWindowFrameWidth = self.getFeatureVariables(cFeature.iId, sVariableName="window frame width")
            bIsFoundWindowFrameHeight, fWindowFrameHeight = self.getFeatureVariables(cFeature.iId, sVariableName="window frame Height")
            bIsFoundLintolExtraVertexesHorizontal, fLintolExtraVertexesHorizontal = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes horizontal")
            bIsFoundLintolExtraVertexesVertical, fLintolExtraVertexesVertical = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes vertical")

            if bIsFoundWindowFrameWidth == True and bIsFoundWindowFrameHeight == True:
                self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAStart.append(cTempVertex)
                lstWindowFrameVertexesSideABottom.append(cTempVertex)
                cVertexFrameLastAStart = cTempVertex
                cVertexFrameFirstABottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                lstWindowFrameVertexesSideABottom.append(cTempVertex)
                cVertexFrameLastAEnd = cTempVertex
                cVertexFrameLastABottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBStart.append(cTempVertex)
                lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                cVertexFrameLastBStart = cTempVertex
                cVertexFrameFirstBBottom = cTempVertex

                self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                cVertexFrameLastBEnd = cTempVertex
                cVertexFrameLastBBottom = cTempVertex







                self.sClassMessage = "top of the window frame, side 'a' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAStart.append(cTempVertex)
                lstWindowFrameVertexesSideATop.append(cTempVertex)
                cVertexFrameFirstAStart = cTempVertex
                cVertexFrameFirstATop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'a' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "a"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                lstWindowFrameVertexesSideATop.append(cTempVertex)
                cVertexFrameFirstAEnd = cTempVertex
                cVertexFrameLastATop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'b' of wall, 'start' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "start"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBStart.append(cTempVertex)
                lstWindowFrameVertexesSideBTop.append(cTempVertex)
                cVertexFrameFirstBStart = cTempVertex
                cVertexFrameFirstBTop = cTempVertex

                self.sClassMessage = "top of the window frame, side 'b' of wall, 'end' side of doorway"
                cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                    self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                    self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                cTempVertex.iFeatureId = cFeature.iId
                cTempVertex.iWallId = self.iId
                cTempVertex.sOrientation = "end"
                cTempVertex.sSide = "b"
                cTempVertex.iId = iVertexCounter
                iVertexCounter = iVertexCounter + 1
                lstClsVert.append(cTempVertex)
                objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                lstVert.verts.append(objVert)

                lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                lstWindowFrameVertexesSideBTop.append(cTempVertex)
                cVertexFrameFirstBEnd = cTempVertex
                cVertexFrameLastBTop = cTempVertex






                if bIsFoundLintolExtraVertexesHorizontal == True:
                    iLintolVertexCounter = 0

                    iVertexFirstATopId = cVertexFrameFirstATop.iId
                    iVertexFirstBTopId = cVertexFrameFirstBTop.iId
                    iVertexFirstABottomId = cVertexFrameFirstABottom.iId
                    iVertexFirstBBottomId = cVertexFrameFirstBBottom.iId

                    while iLintolVertexCounter < fLintolExtraVertexesHorizontal / fVertexRatio:
                        iLintolVertexCounter = iLintolVertexCounter + 1

                        #Top of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol, side A"
                        cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + iLintolVertexCounter * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            cVertexFrameFirstATop.fY + iLintolVertexCounter * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideATop.append(cTempVertex)
                        iVertexSecondATopId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol, side B"
                        cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + iLintolVertexCounter * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            cVertexFrameFirstBTop.fY + iLintolVertexCounter * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBTop.append(cTempVertex)
                        iVertexSecondBTopId = cTempVertex.iId

                        #bottom of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol, side A"
                        cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + iLintolVertexCounter * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            cVertexFrameFirstATop.fY + iLintolVertexCounter * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideABottom.append(cTempVertex)
                        iVertexSecondABottomId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol, side B"
                        cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + iLintolVertexCounter * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            cVertexFrameFirstBTop.fY + iLintolVertexCounter * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY) / (fLintolExtraVertexesHorizontal / fVertexRatio + 1),
                            self.vOffset.z + cFeature.fPosVert - fWindowFrameHeight / 2.0)
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "internal"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBBottom.append(cTempVertex)
                        iVertexSecondBBottomId = cTempVertex.iId

                        #####################################################################################################################
                        #   Still need to create all the faces with these extra vertexes in the lintol and down the side of the door frame  #
                        #####################################################################################################################

                        #Side A: above window
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexFirstATopId, iVertexSecondATopId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        #Side B: above window
                        cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexFirstBTopId, iVertexSecondBTopId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        iVertexFirstATopId = iVertexSecondATopId
                        iVertexFirstBTopId = iVertexSecondBTopId

                        #Side A: below window
                        cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, iVertexFirstABottomId, iVertexSecondABottomId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        #Side B: below window
                        cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, iVertexFirstBBottomId, iVertexSecondBBottomId])
                        cTempFace.iId = cFeature.faceMaxId() + 1
                        cFeature.addFace(cTempFace)

                        iVertexFirstABottomId = iVertexSecondABottomId
                        iVertexFirstBBottomId = iVertexSecondBBottomId

                    #Side A: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, iVertexSecondATopId, cVertexFrameLastATop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, iVertexSecondBTopId, cVertexFrameLastBTop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side A: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, iVertexSecondABottomId, cVertexFrameLastABottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, iVertexSecondBBottomId, cVertexFrameLastBBottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)
                else:
                    #No extra vertexes in the lintol
                    #Side A: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureA.iId, cVertexFrameFirstATop.iId, cVertexFrameLastATop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: above window
                    cTempFace = ClsFace(cFeature.iId, [cVertexTopFeatureB.iId, cVertexFrameFirstBTop.iId, cVertexFrameLastBTop.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side A: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureA.iId, cVertexFrameFirstABottom.iId, cVertexFrameLastABottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)

                    #Side B: below window
                    cTempFace = ClsFace(cFeature.iId, [cVertexBottomFeatureB.iId, cVertexFrameFirstBBottom.iId, cVertexFrameLastBBottom.iId])
                    cTempFace.iId = cFeature.faceMaxId() + 1
                    cFeature.addFace(cTempFace)







                if bIsFoundLintolExtraVertexesVertical == True:
                    iLintolVertexCounter = 0

                    iVertexFirstAStartId = cVertexFrameFirstAStart.iId
                    iVertexFirstBStartId = cVertexFrameFirstBStart.iId
                    iVertexFirstAEndId = cVertexFrameFirstAEnd.iId
                    iVertexFirstBEndId = cVertexFrameFirstBEnd.iId

                    while iLintolVertexCounter < fLintolExtraVertexesVertical / fVertexRatio:
                        iLintolVertexCounter = iLintolVertexCounter + 1

                        #Start of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical / fVertexRatio + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideAStart.append(cTempVertex)
                        iVertexSecondAStartId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor - fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical / fVertexRatio + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "start"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBStart.append(cTempVertex)
                        iVertexSecondBStartId = cTempVertex.iId

                        #end of window frame
                        #Side A
                        self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical / fVertexRatio + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "a"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideAEnd.append(cTempVertex)
                        iVertexSecondAEndId = cTempVertex.iId

                        #Side B
                        self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                        cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                            self.vOffset.y + (cFeature.fPosHor + fWindowFrameWidth / 2.0) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                            self.vOffset.z + cFeature.fPosVert + fWindowFrameHeight * (float(iLintolVertexCounter / (fLintolExtraVertexesVertical / fVertexRatio + 1.0)) - 0.5))
                        cTempVertex.iFeatureId = cFeature.iId
                        cTempVertex.iWallId = self.iId
                        cTempVertex.sOrientation = "end"
                        cTempVertex.sSide = "b"
                        cTempVertex.iId = iVertexCounter
                        iVertexCounter = iVertexCounter + 1
                        lstClsVert.append(cTempVertex)
                        objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                        lstVert.verts.append(objVert)

                        lstWindowFrameVertexesSideBEnd.append(cTempVertex)
                        iVertexSecondBEndId = cTempVertex.iId



#############################################################################
###                                                                       ###
###                          Single  arch                                 ###
###                                                                       ###
#############################################################################


                lstWindowVertexesSideAStart = []
                lstWindowVertexesSideBStart = []
                lstWindowVertexesSideAEnd = []
                lstWindowVertexesSideBEnd = []
                lstWindowVertexesSideATop = []
                lstWindowVertexesSideBTop = []
                lstWindowVertexesSideABottom = []
                lstWindowVertexesSideBBottom = []



                bIsFoundWindowWidth, fWindowWidth = self.getFeatureVariables(cFeature.iId, sVariableName="window width")
                bIsFoundWindowHeight, fWindowHeight = self.getFeatureVariables(cFeature.iId, sVariableName="window Height")
                bIsFoundLintolExtraVertexesHorizontal, fLintolExtraVertexesHorizontal = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes horizontal")
                bIsFoundLintolExtraVertexesVertical, fLintolExtraVertexesVertical = self.getFeatureVariables(cFeature.iId, sVariableName="window lintol extra vertexes vertical")

#######################
#                     #
#  Corners of curve  #
#                     #
#######################

                fAngleOfCorner = math.asin(fWindowHeight / math.sqrt((fWindowHeight * fWindowHeight) + (fWindowWidth * fWindowWidth)))


                if bIsFoundWindowWidth == True and bIsFoundWindowHeight == True:
                    fCornerHeight = fWindowHeight * math.sin(fAngleOfCorner) / 2.0
                    fCornerWidth = fWindowWidth * math.cos(fAngleOfCorner) / 2.0

                    if fCornerHeight < 0:
                        fCornerHeight = -1 * fCornerHeight

                    if fCornerWidth < 0:
                        fCornerWidth= -1 * fCornerWidth

                    self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fCornerWidth) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fCornerWidth) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert - fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideAStart.append(cTempVertex)
                    lstWindowVertexesSideABottom.append(cTempVertex)
                    cVertexLintolLastAStart = cTempVertex
                    cVertexLintolFirstABottom = cTempVertex

                    self.sClassMessage = "bottom of the window frame, side 'a' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fCornerWidth) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fCornerWidth) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert - fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideAEnd.append(cTempVertex)
                    lstWindowVertexesSideABottom.append(cTempVertex)
                    cVertexLintolLastAEnd = cTempVertex
                    cVertexLintolLastABottom = cTempVertex

                    self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fCornerWidth) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fCornerWidth) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert - fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideBStart.append(cTempVertex)
                    lstWindowVertexesSideBBottom.append(cTempVertex)
                    cVertexLintolLastBStart = cTempVertex
                    cVertexLintolFirstBBottom = cTempVertex

                    self.sClassMessage = "bottom of the window frame, side 'b' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fCornerWidth) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fCornerWidth) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert - fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideBEnd.append(cTempVertex)
                    lstWindowVertexesSideBBottom.append(cTempVertex)
                    cVertexLintolLastBEnd = cTempVertex
                    cVertexLintolLastBBottom = cTempVertex












                    self.sClassMessage = "top of the window frame, side 'a' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fCornerWidth) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fCornerWidth) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert + fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideAStart.append(cTempVertex)
                    lstWindowVertexesSideATop.append(cTempVertex)
                    cVertexLintolFirstAStart = cTempVertex
                    cVertexLintolFirstATop = cTempVertex

                    self.sClassMessage = "top of the window frame, side 'a' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fCornerWidth) * math.sin(self.fRotationalVertical) + self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fCornerWidth) * math.cos(self.fRotationalVertical) + self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert + fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "a"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideAEnd.append(cTempVertex)
                    lstWindowVertexesSideATop.append(cTempVertex)
                    cVertexLintolFirstAEnd = cTempVertex
                    cVertexLintolLastATop = cTempVertex

                    self.sClassMessage = "top of the window frame, side 'b' of wall, 'start' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor - fCornerWidth) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor - fCornerWidth) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert + fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideBStart.append(cTempVertex)
                    lstWindowVertexesSideBTop.append(cTempVertex)
                    cVertexLintolFirstBStart = cTempVertex
                    cVertexLintolFirstBTop = cTempVertex

                    self.sClassMessage = "top of the window frame, side 'b' of wall, 'end' side of doorway"
                    cTempVertex = ClsVertex(self.vOffset.x + (cFeature.fPosHor + fCornerWidth) * math.sin(self.fRotationalVertical) - self.fThinkness * math.cos(self.fRotationalVertical) / 2.0,
                        self.vOffset.y + (cFeature.fPosHor + fCornerWidth ) * math.cos(self.fRotationalVertical) - self.fThinkness * math.sin(self.fRotationalVertical) / 2.0,
                        self.vOffset.z + cFeature.fPosVert + fCornerHeight)
                    cTempVertex.iFeatureId = cFeature.iId
                    cTempVertex.iWallId = self.iId
                    cTempVertex.sOrientation = "internal"
                    cTempVertex.sSide = "b"
                    cTempVertex.iId = iVertexCounter
                    iVertexCounter = iVertexCounter + 1
                    lstClsVert.append(cTempVertex)
                    objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                    lstVert.verts.append(objVert)

                    lstWindowVertexesSideBEnd.append(cTempVertex)
                    lstWindowVertexesSideBTop.append(cTempVertex)
                    cVertexLintolFirstBEnd = cTempVertex
                    cVertexLintolLastBTop = cTempVertex








#########################
#                       #
#   Horizontal frame   #
#                       #
#########################

                    if bIsFoundLintolExtraVertexesHorizontal == True:
                        iLintolVertexCounter = 0

                        iVertexFirstATopId = cVertexLintolFirstATop.iId
                        iVertexFirstBTopId = cVertexLintolFirstBTop.iId
                        iVertexFirstABottomId = cVertexLintolFirstABottom.iId
                        iVertexFirstBBottomId = cVertexLintolFirstBBottom.iId

                        fAngleStart = fAngleOfCorner
                        fAngleEnd = math.pi - fAngleOfCorner

                        fAngleIncrements = (fAngleEnd - fAngleStart) / (fLintolExtraVertexesHorizontal + 1)
                        fAngle = fAngleStart

                        while iLintolVertexCounter < fLintolExtraVertexesHorizontal:
                            iLintolVertexCounter = iLintolVertexCounter + 1

                            fAngle = fAngle + fAngleIncrements

                            fSillHeight = (fWindowHeight / fWindowFrameHeight) *  (math.sin(fAngle) / 2.0)
                            fSillWidth = (fWindowWidth  / fWindowFrameWidth) * (math.cos(fAngle) / 2.0)


                            #Top of window frame
                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol, side A"
                            cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + (0.5 + fSillWidth) * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX),
                                cVertexFrameFirstATop.fY + (0.5 + fSillWidth) * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY),
                                cVertexFrameLastAStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideATop.append(cTempVertex)
                            iVertexSecondATopId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol, side B"
                            cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX),
                                cVertexFrameFirstBTop.fY + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY),
                                cVertexFrameLastBStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideBTop.append(cTempVertex)
                            iVertexSecondBTopId = cTempVertex.iId

                            #bottom of window frame
                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol, side A"
                            cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + (0.5 + fSillWidth) * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX),
                                cVertexFrameFirstATop.fY + (0.5 + fSillWidth) * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY),
                                cVertexFrameLastAStart.fZ + (0.5 - fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideABottom.append(cTempVertex)
                            iVertexSecondABottomId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol, side B"
                            cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX),
                                cVertexFrameFirstBTop.fY + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY),
                                cVertexFrameLastBStart.fZ + (0.5 - fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideBBottom.append(cTempVertex)
                            iVertexSecondBBottomId = cTempVertex.iId





#######################
#                     #
#   Vertical frame   #
#                     #
#######################


                    if bIsFoundLintolExtraVertexesVertical == True:
                        iLintolVertexCounter = 0

                        iVertexFirstAStartId = cVertexLintolFirstAStart.iId
                        iVertexFirstBStartId = cVertexLintolFirstBStart.iId
                        iVertexFirstAEndId = cVertexLintolFirstAEnd.iId
                        iVertexFirstBEndId = cVertexLintolFirstBEnd.iId

                        fAngleStart = fAngleOfCorner
                        fAngleEnd = -1 * fAngleOfCorner

                        fAngleIncrements = (fAngleEnd - fAngleStart) / (fLintolExtraVertexesVertical + 1)
                        fAngle = fAngleStart

                        while iLintolVertexCounter < fLintolExtraVertexesVertical:
                            iLintolVertexCounter = iLintolVertexCounter + 1

                            fAngle = fAngle + fAngleIncrements

                            fSillHeight = (fWindowHeight / fWindowFrameHeight) *  (math.sin(fAngle) / 2.0)
                            fSillWidth = (fWindowWidth  / fWindowFrameWidth) * (math.cos(fAngle) / 2.0)

                            #Start of window frame
                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                            cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + (0.5 - fSillWidth) * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX),
                                cVertexFrameFirstATop.fY + (0.5 - fSillWidth) * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY),
                                cVertexFrameLastAStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideAStart.append(cTempVertex)
                            iVertexSecondAStartId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                            cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + (0.5 - fSillWidth) * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX),
                                cVertexFrameFirstBTop.fY + (0.5 - fSillWidth) * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY),
                                cVertexFrameLastBStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideBStart.append(cTempVertex)
                            iVertexSecondBStartId = cTempVertex.iId

                            #end of window frame
                            #Side A
                            self.sClassMessage = "Extra vertexes on lintol vertical, side A"
                            cTempVertex = ClsVertex(cVertexFrameFirstATop.fX + (0.5 + fSillWidth) * (cVertexFrameLastATop.fX - cVertexFrameFirstATop.fX),
                                cVertexFrameFirstATop.fY + (0.5 + fSillWidth) * (cVertexFrameLastATop.fY - cVertexFrameFirstATop.fY),
                                cVertexFrameLastAStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "a"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideAEnd.append(cTempVertex)
                            iVertexSecondAEndId = cTempVertex.iId

                            #Side B
                            self.sClassMessage = "Extra vertexes on lintol vertical, side B"
                            cTempVertex = ClsVertex(cVertexFrameFirstBTop.fX + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fX - cVertexFrameFirstBTop.fX),
                                cVertexFrameFirstBTop.fY + (0.5 + fSillWidth) * (cVertexFrameLastBTop.fY - cVertexFrameFirstBTop.fY),
                                cVertexFrameLastBStart.fZ + (0.5 + fSillHeight) * (cVertexFrameFirstAStart.fZ - cVertexFrameLastAStart.fZ))
                            cTempVertex.iFeatureId = cFeature.iId
                            cTempVertex.iWallId = self.iId
                            cTempVertex.sOrientation = "internal"
                            cTempVertex.sSide = "b"
                            cTempVertex.iId = iVertexCounter
                            iVertexCounter = iVertexCounter + 1
                            lstClsVert.append(cTempVertex)
                            objVert = NMesh.Vert(cTempVertex.fX, cTempVertex.fY, cTempVertex.fZ)
                            lstVert.verts.append(objVert)

                            lstWindowVertexesSideBEnd.append(cTempVertex)
                            iVertexSecondBEndId = cTempVertex.iId




                    #the window sill
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideATop, lstWindowVertexesSideBTop, "flat", True, cVertexLintolFirstATop.iId, cVertexLintolLastATop.iId, cVertexLintolFirstBTop.iId, cVertexLintolLastBTop.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideAStart, lstWindowVertexesSideBStart, "flat", True, cVertexLintolFirstAStart.iId, cVertexLintolLastAStart.iId, cVertexLintolFirstBStart.iId, cVertexLintolLastBStart.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideAEnd, lstWindowVertexesSideBEnd, "flat", True, cVertexLintolFirstAEnd.iId, cVertexLintolLastAEnd.iId, cVertexLintolFirstBEnd.iId, cVertexLintolLastBEnd.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideABottom, lstWindowVertexesSideBBottom, "flat", True, cVertexLintolFirstABottom.iId, cVertexLintolLastABottom.iId, cVertexLintolFirstBBottom.iId, cVertexLintolLastBBottom.iId)



                    cVertexLintolFirstATop.printPosition("cVertexLintolFirstATop")
                    cVertexFrameFirstATop.printPosition("cVertexFrameFirstATop")
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideATop, lstWindowFrameVertexesSideATop, "flat", True, cVertexLintolFirstATop.iId, cVertexLintolLastATop.iId, cVertexFrameFirstATop.iId, cVertexFrameLastATop.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideBTop, lstWindowFrameVertexesSideBTop, "flat", True, cVertexLintolFirstBTop.iId, cVertexLintolLastBTop.iId, cVertexFrameFirstBTop.iId, cVertexFrameLastBTop.iId)

                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideABottom, lstWindowFrameVertexesSideABottom, "flat", True, cVertexLintolFirstABottom.iId, cVertexLintolLastABottom.iId, cVertexFrameFirstABottom.iId, cVertexFrameLastABottom.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideBBottom, lstWindowFrameVertexesSideBBottom, "flat", True, cVertexLintolFirstBBottom.iId, cVertexLintolLastBBottom.iId, cVertexFrameFirstBBottom.iId, cVertexFrameLastBBottom.iId)

                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideAStart, lstWindowFrameVertexesSideAStart, "flat", True, cVertexLintolFirstAStart.iId, cVertexLintolLastAStart.iId, cVertexFrameFirstAStart.iId, cVertexFrameLastAStart.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideBStart, lstWindowFrameVertexesSideBStart, "flat", True, cVertexLintolFirstBStart.iId, cVertexLintolLastBStart.iId, cVertexFrameFirstBStart.iId, cVertexFrameLastBStart.iId)

                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideAEnd, lstWindowFrameVertexesSideAEnd, "flat", True, cVertexLintolFirstAEnd.iId, cVertexLintolLastAEnd.iId, cVertexFrameFirstAEnd.iId, cVertexFrameLastAEnd.iId)
                    self.addFacesSill(lstVert, lstClsVert, lstWindowVertexesSideBEnd, lstWindowFrameVertexesSideBEnd, "flat", True, cVertexLintolFirstBEnd.iId, cVertexLintolLastBEnd.iId, cVertexFrameFirstBEnd.iId, cVertexFrameLastBEnd.iId)


            return iVertexCounter
        except:
            self.errorCode()
            return iVertexCounter

    def joinDividerToDivider(self, cFeatureM, cFeatureN, lstVert, lstClsVert):
        try:
            self.sClassStep = "create the faces: divider meets divider"
            #1)  loop through both sides of the wall (a and b)
            #2)  create 2 lists of vertexes (one for each feature)
            #3)  pick the bottom two vertexes (one from each list)
            #4)  Find the next vertex up (could be on either list)
            #5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list
            #6)  which ever vertex was found on point (4) now has to replace the lowest vertex processed on that feature

            if not cFeatureM.iWallId == cFeatureN.iWallId:
                print "***********************************"
                print "Error: Connecting different walls"
                print "***********************************"


            self.sClassSubStep = "(1) loop through both sides of the wall (a and b)"
            for sSide in ["a", "b"]:
                self.sClassSubStep = "(2) create 2 lists of vertexes (one for each feature)"
                lstMVertexes = None
                lstNVertexes = None

                lstMVertexes = []
                lstNVertexes = []

                iCounter = 0
                for cTempVertex in lstClsVert:
                    if cTempVertex.iFeatureId == cFeatureM.iId and cTempVertex.iWallId == self.iId:
                        lstMVertexes.append(cTempVertex)
                        iCounter = iCounter + 1
                    if cTempVertex.iFeatureId == cFeatureN.iId and cTempVertex.iWallId == self.iId:
                        lstNVertexes.append(cTempVertex)
                        iCounter = iCounter + 1

                self.sClassSubStep = "(3) Pick the bottom two vertexes (one from each list)"
                bIsFoundLowestM, lowestMVertex = self.lowestVertexInList(lstMVertexes, 0, sSide)
                bIsFoundLowestN, lowestNVertex = self.lowestVertexInList(lstNVertexes, 0, sSide)

                self.sClassUsefulValue = "No. Vertexes in lists " + str(iCounter)

                self.sClassSubStep = "(4)  Find the next vertex up (could be on either list): First time"
                lstExceptions = None
                lstExceptions = [lowestMVertex, lowestNVertex]

                if lstMVertexes is None:
                    self.sClassMessage = "lstMVertexes == None"
                if lstNVertexes is None:
                    self.sClassMessage = "lstNVertexes == None"
                if lstExceptions is None:
                    self.sClassMessage = "lstExceptions == None"

                bIsFoundNextVertex, nextVertex = self.lowestVertexInTwoLists(lstMVertexes, lstNVertexes, 0, lstExceptions, sSide)

                self.sClassSubStep = "(5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list: First time"
                objFaceRight = NMesh.Face()
                objFaceRight.v.append(lstVert.verts[lowestMVertex.iId])
                objFaceRight.v.append(lstVert.verts[lowestNVertex.iId])
                objFaceRight.v.append(lstVert.verts[nextVertex.iId])
                lstVert.faces.append(objFaceRight)

                lstExceptions.append(nextVertex)

                while bIsFoundLowestM == True and bIsFoundLowestN == True and bIsFoundNextVertex == True:
                    self.sClassSubStep = "(6)  which ever vertex was found on point (4) now has to replace the lowest vertex processed on that feature"
                    if nextVertex.iFeatureId == lowestMVertex.iFeatureId:
                        lowestMVertex = nextVertex
                    elif nextVertex.iFeatureId == lowestNVertex.iFeatureId:
                        lowestNVertex = nextVertex
                    else:
                        self.sClassMessage = "the next vertex is not on the same feature as either of the two other vertexes"

                    self.sClassSubStep = "(4)  Find the next vertex up (could be on either list): Second time"
                    bIsFoundNextVertex, nextVertex = self.lowestVertexInTwoLists(lstMVertexes, lstNVertexes, 0, lstExceptions, sSide)

                    if bIsFoundNextVertex == True:
                        lstExceptions.append(nextVertex)
                        self.sClassSubStep = "(5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list: Second time"
                        objFaceRight = NMesh.Face()
                        objFaceRight.v.append(lstVert.verts[lowestMVertex.iId])
                        objFaceRight.v.append(lstVert.verts[lowestNVertex.iId])
                        objFaceRight.v.append(lstVert.verts[nextVertex.iId])
                        lstVert.faces.append(objFaceRight)
        except:
            self.errorCode()

    def joinDividerToDoor(self, cFeatureFirst, cFeatureSecond, lstVert, lstClsVert):
        try:
            #######################################
            #      connect doorway to divider    #
            #######################################

            if not cFeatureFirst.iWallId == cFeatureSecond.iWallId:
                print "***********************************"
                print "Error: Connecting different walls"
                print "***********************************"
            else:
                print "Connecting Features"
                print "    " + cFeatureFirst.sName
                print "    " + cFeatureSecond.sName

            self.sClassStep = "create the faces: divider meets door"
            #1)  loop through both sides of the wall (a and b)
            #2)  create 2 lists of vertexes (one for each feature)
            #3)  pick the bottom two vertexes (one from each list)
            #4)  Find the next vertex up (could be on either list)
            #5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list
            #6)  which ever vertex was found on point (4) now has to replace the lowest vertex processed on that feature

            self.sClassSubStep = "(1) loop through both sides of the wall (a and b)"
            for sSide in ["a", "b"]:
                self.sClassSubStep = "(2) create 2 lists of vertexes (one for each feature)"
                lstFirstVertexes = None
                lstSecondVertexes = None

                lstFirstVertexes = []
                lstSecondVertexes = []

                iCounter = 0
                for cTempVertex in lstClsVert:
                    if cTempVertex.iFeatureId == cFeatureFirst.iId and cTempVertex.iWallId == self.iId and (cTempVertex.sOrientation == "start" or cTempVertex.sOrientation == "middle"):
                        lstFirstVertexes.append(cTempVertex)
                        iCounter = iCounter + 1
                    if cTempVertex.iFeatureId == cFeatureSecond.iId and cTempVertex.iWallId == self.iId and (cTempVertex.sOrientation == "end" or cTempVertex.sOrientation == "middle"):
                        lstSecondVertexes.append(cTempVertex)
                        iCounter = iCounter + 1

                self.sClassSubStep = "(3) Pick the bottom two vertexes (one from each list)"
                bIsFoundLowestFirst, lowestFirstVertex = self.lowestVertexInList(lstFirstVertexes, 0, sSide)
                bIsFoundLowestSecond, lowestSecondVertex = self.lowestVertexInList(lstSecondVertexes, 0, sSide)

                self.sClassUsefulValue = "No. Vertexes in lists " + str(iCounter)

                self.sClassSubStep = "(4)  Find the next vertex up (could be on either list): First time"
                lstExceptions = None
                lstExceptions = [lowestFirstVertex, lowestSecondVertex]

                if lstFirstVertexes is None:
                    self.sClassMessage = "lstFirstVertexes == None"
                if lstSecondVertexes is None:
                    self.sClassMessage = "lstSecondVertexes == None"
                if lstExceptions is None:
                    self.sClassMessage = "lstExceptions == None"

                bIsFoundNextVertex, nextVertex = self.lowestVertexInTwoLists(lstFirstVertexes, lstSecondVertexes, 0, lstExceptions, sSide)

                self.sClassSubStep = "(5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list: First time"
                objFaceRight = NMesh.Face()
                objFaceRight.v.append(lstVert.verts[lowestFirstVertex.iId])
                objFaceRight.v.append(lstVert.verts[lowestSecondVertex.iId])
                objFaceRight.v.append(lstVert.verts[nextVertex.iId])
                lstVert.faces.append(objFaceRight)

                lstExceptions.append(nextVertex)

                while bIsFoundLowestFirst == True and bIsFoundLowestSecond == True and bIsFoundNextVertex == True:
                    self.sClassSubStep = "(6)  which ever vertex was found on point (4) now has to replace the lowest vertex processed on that feature"
                    if nextVertex.iFeatureId == lowestFirstVertex.iFeatureId:
                        lowestFirstVertex = nextVertex
                    elif nextVertex.iFeatureId == lowestSecondVertex.iFeatureId:
                        lowestSecondVertex = nextVertex
                    else:
                        self.sClassMessage = "the next vertex is not on the same feature as either of the two other vertexes"

                    self.sClassSubStep = "(4)  Find the next vertex up (could be on either list): Second time"
                    bIsFoundNextVertex, nextVertex = self.lowestVertexInTwoLists(lstFirstVertexes, lstSecondVertexes, 0, lstExceptions, sSide)

                    if bIsFoundNextVertex == True:
                        lstExceptions.append(nextVertex)
                        self.sClassSubStep = "(5)  Using the 3 vertexes  (from (3) and (4)) create a face and add it to the faces list: Second time"
                        objFaceRight = NMesh.Face()
                        objFaceRight.v.append(lstVert.verts[lowestFirstVertex.iId])
                        objFaceRight.v.append(lstVert.verts[lowestSecondVertex.iId])
                        objFaceRight.v.append(lstVert.verts[nextVertex.iId])
                        lstVert.faces.append(objFaceRight)


            del lstFirstVertexes
            del lstSecondVertexes 

        except:
            self.errorCode()

    def addFacesSill(self, lstVert, lstClsVert, lstVertexSideA, lstVertexSideB, sType, bHasEnds, iSideAStartVertexId = None, iSideAEndVertexId = None, iSideBStartVertexId = None, iSideBEndVertexId = None):
        __doc__ ="""
        create all the ClsFace objects that connect the two sides of the wall.
        This will be used in Doorways and windows as well as the end of walls

        bHasEnds distinguishes doors and windows where on a door you can start
        at one end work your way arond to the other end, where as for a window
        you will keep going around and around.
        """
        try:
            if sType == "flat":
                if bHasEnds == True:
                    #1)  Pick the first two vertexes we are starting with
                    #2)  pick the next closest vertex
                    #3)  make a face
                    lstDone = [] #a list of all the vertexes that have already been used

                    bIsFoundA, ClsVertexA = self.getVertexFromList(lstVertexSideA, iSideAStartVertexId)
                    bIsFoundB, ClsVertexB = self.getVertexFromList(lstVertexSideB, iSideBStartVertexId)

                    if bIsFoundA == False or bIsFoundB == False:
                        self.addWarning("addFacesSill: Can't find Vertex in a list where it should be.")

                    lstDone.append(ClsVertexA)
                    lstDone.append(ClsVertexB)

                    bIsFound, ClsNextVertex, sLstName = self.getClosestClsVertexFromTwoLists(lstVertexSideA, lstVertexSideB, lstDone, ClsVertexA, ClsVertexB)

                    while bIsFound == True:
                        objFaceRight = NMesh.Face()
                        objFaceRight.v.append(lstVert.verts[ClsVertexA.iId])
                        objFaceRight.v.append(lstVert.verts[ClsVertexB.iId])
                        objFaceRight.v.append(lstVert.verts[ClsNextVertex.iId])
                        lstVert.faces.append(objFaceRight)

                        lstDone.append(ClsNextVertex)

                        if sLstName == "A":
                            ClsVertexA = ClsNextVertex
                        elif sLstName == "B":
                            ClsVertexB = ClsNextVertex

                        bIsFound, ClsNextVertex, sLstName = self.getClosestClsVertexFromTwoLists(lstVertexSideA, lstVertexSideB, lstDone, ClsVertexA, ClsVertexB)
        except:
            self.errorCode()

    def addFeaturesExtraFaces(self, cFeature, lstVert, lstClsVert):
        try:
            ###################################
            #           Extra Faces          #
            ###################################

            if cFeature.extraFacesExist() == True:
                cTempFace = ClsFace(cFeature.iId, [])
                cTempVertex = ClsVertex(0, 0, 0)

                cFeature.faceMoveFirst()
                while not cFeature.faceEof() == True:
                    bIsError = False
                    bIsError, cTempFace = cFeature.getFace()

                    if bIsError == False:
                        objFaceRight = NMesh.Face()

                        if cTempFace.hasVertexes() == True:
                            cTempFace.vertexMoveFirst()
                            while not cTempFace.vertexEof():
                                bIsError, iTempVertexId = cTempFace.getVertexId()
                                if bIsError == False:
                                    vTempVertex = lstVert.verts[iTempVertexId]
                                else:
                                    self.addWarning("Can't return a VertexId for the face.")
                                objFaceRight.v.append(vTempVertex)
                                cTempFace.vertexMoveNext()
                            cFeature.faceMoveNext()
                            lstVert.faces.append(objFaceRight)
                        else:
                            self.addWarning("Can't find Vertexes in Face")
        except:
            self.errorCode()

    def firstFeature(self):
        try:
            bIsFound = False
            for cFeature in self.lstFeatures:
                if cFeature.iWallId == self.iId:
                    bIsFound = True
                    return bIsFound, cFeature
            if bIsFound == False:
                print "Can't find first Feature, wall Id: " + str(self.iId)
                return bIsFound, None
        except:
            print "Can't find first Feature, wall Id: " + str(self.iId)
            self.errorCode()
            return False, None


    def buildWall(self, iVertexCounter, lstVert, lstClsVert):
        __doc__ = """
        The plan
        --------
        1)Loop through all the features and for each feature create a series of vertexes
        2)put the vertexes in both the lstClsVert and lstVert
        3)loop through the features depending on the combination of which features are appearing next to eachother join the vertexes together (by populating cFaces with face class) in different combinations
        4)loop though the cFaces list of class instances and create face object in the mesh, using the lstClsVert and cFaces to look up the ID values
        """
        try:
            self.sortFeatures()
            self.sClassStep = "Create containers (lists)"
            #Create the mesh object this is a list of vertexes
#            lstVert = NMesh.GetRaw()
#            lstClsVert = []
#            cFaces = []

            #Create a mapping object to keep track of which vertexes are going to be mapped to which
            #once all the vertexes are created we can then follow the map and create the faces

            #Z = Height
            #X = Width
            #Y = Depth
            #add the vertexs

            self.sClassStep = "create the vertexes"

            print ""
            print "Count at beginning of building wall"
            print "iVertexCounter: " + str(iVertexCounter)
#            print "lstVert: " + self.countItemsInList(lstVert)
#            print "lstClsVert: " + self.countItemsInList(lstClsVert)
            print ""

            print "Started Building Wall"
            print "    Length " + str(self.fLength)
            print "    Thickness " + str(self.fThinkness)
            print "    Height " + str(self.fDefaultHeight)
            print "    Rotational angle " + str(self.fRotationalVertical)
            print "    iVertexCounter " + str(iVertexCounter)


            for cFeatureCurrent in self.lstFeatures:
                if cFeatureCurrent.iWallId == self.iId:
                    print "Type: " + cFeatureCurrent.sType
                    print "Sub Type: " + cFeatureCurrent.sSubType
                    print "Wall Id " + str(cFeatureCurrent.iWallId)
                    if cFeatureCurrent.sType == "divider":
    #                    print "adding vertexes for divider"
                        iVertexCounter = self.addVertexesDivider(cFeatureCurrent, iVertexCounter, lstVert, lstClsVert)
                    elif cFeatureCurrent.sType == "door":
    #                    print "adding vertexes for door"
                        iVertexCounter = self.addVertexesDoor(cFeatureCurrent, iVertexCounter, lstVert, lstClsVert)
                    elif cFeatureCurrent.sType == "window":
    #                    print "adding vertexes for window"
                        iVertexCounter = self.addVertexesWindow(cFeatureCurrent, iVertexCounter, lstVert, lstClsVert)

            self.sClassStep = "create the faces"
            print "Create the faces"
            #add the faces to the existing vertexes
            bIsFound, cFeaturePrevious = self.firstFeature()

            if not bIsFound == True:
                print "Can't find first Feature of wall"

            for cFeatureCurrent in self.lstFeatures:
                if cFeatureCurrent.iWallId == self.iId and cFeaturePrevious.iWallId == self.iId:
                    if not (cFeatureCurrent.iId == cFeaturePrevious.iId):
                        if cFeatureCurrent.sType == "divider" and cFeaturePrevious.sType == "divider":
                            self.joinDividerToDivider(cFeatureCurrent, cFeaturePrevious, lstVert, lstClsVert)
                        elif (cFeatureCurrent.sType == "divider" and cFeaturePrevious.sType == "door") or (cFeatureCurrent.sType == "door" and cFeaturePrevious.sType == "divider"):
                            print "        Features divider and door"
                            self.joinDividerToDoor(cFeatureCurrent, cFeaturePrevious, lstVert, lstClsVert)
                            self.sClassSubStep = "(1) loop through both sides of the wall (a and b)"
                        elif (cFeatureCurrent.sType == "divider" and cFeaturePrevious.sType == "window") or (cFeatureCurrent.sType == "window" and cFeaturePrevious.sType == "divider"):
                            print "        Features divider and door"
                            self.joinDividerToDoor(cFeatureCurrent, cFeaturePrevious, lstVert, lstClsVert)
                            self.sClassSubStep = "(1) loop through both sides of the wall (a and b)"
                        else:
                            print "        Features of unknown types are meeting"
                            print "        Features Current = " + cFeatureCurrent.sType
                            print "        Features Previous = " + cFeaturePrevious.sType

                    self.addFeaturesExtraFaces(cFeatureCurrent, lstVert, lstClsVert)

                    cFeaturePrevious = cFeatureCurrent

            print ""
            print "Count at end of building wall"
            print "iVertexCounter: " + str(iVertexCounter)
#            print "lstVert: " + self.countItemsInList(lstVert)
#            print "lstClsVert: " + self.countItemsInList(lstClsVert)
            print ""
            return iVertexCounter, lstVert, lstClsVert
#            objMyBox = NMesh.PutRaw(lstVert)
        except:
            self.errorCode()
