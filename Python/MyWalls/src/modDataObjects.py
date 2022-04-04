#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modDataObjects"
__module__ = "modDataObjects"
__version__ = "0.1"
__bpydoc__ = """
Just the classes that contain all the data
"""

from modBasics import ClsBasics
from Blender import Mathutils
#import modBasics
#reload(modBasics)

class ClsFeature(ClsBasics):
    __doc__ = """
    a feature is a feature in a  walls of type ='door', 'window', 'divider' or 'end of wall'
    Note: the perpous of a divider is to provide more points to draw vertexs from
    Note: the 'end of wall' type is self explainatory
    """
#    global lstVariables

    def __init__(self, psName, psType, psSubType, pfPosHor, pfPosVert, pfHeight, pfWidth):
        __doc__ = """
        Type = 'door'
               'window',
               'divider' (a vertical line of pont that can a have vertex's coming off of them)
               'end of wall'
        Doors
        =====
        Sub Type = 'square'
                   'simple arch' i.e. just one curve with the centre in the centre of the feature
                   'double curve arch' i.e. two curves with centre of curve off centre of the feature

        required extra variables (subtype: square) = 'doorway Height'
                                                     'doorway width'

        required extra variables (subtype: simple arch) = 'doorway Height'
                                                          'doorway width'
                                                          'centre of arch Height'
                                                          'arch radius'

        required extra variables (subtype: double curve arch) = 'doorway Height'
                                                                'doorway width'
                                                                'centre of arches Height'
                                                                'arches radius'
                                                                'centre of arches offset from feature centre'
        """
        self.initialiseBasicsClass()
        try:
            self.sClassName = "ClsFeature"

            self.iId = 0
            self.iWallId = 0
            self.sName = psName
            self.sType = psType
            self.sSubType = psSubType
            self.fPosHor = pfPosHor
            self.fPosVert = pfPosVert
            self.fHeight = pfHeight
            self.fWidth = pfWidth
            self.iFaceCounter = 0
            self.iFaceCurrent = 0
            self.lstExtraFaces = []
        except:
            self.errorCode()

    def getName(self):
        return self._sName
    def setName(self, value):
        self._sName = value
    sName = property(getName, setName)

    def getType(self):
        return self._sType
    def setType(self, value):
        self._sType = value
    sType = property(getType, setType)

    def getSubType(self):
        return self._sSubType
    def setSubType(self, value):
        self._sSubType = value
    sSubType = property(getSubType, setSubType)

    def getHeight(self):
        return self._fHeight
    def setHeight(self, value):
        self._fHeight = float(value)
    fHeight = property(getHeight, setHeight)

    def getWidth(self):
        return self._fWidth
    def setWidth(self, value):
        self._fWidth = float(value)
    fWidth = property(getWidth, setWidth)

    def getPosVert(self):
        return self._fPosVert
    def setPosVert(self, value):
        self._fPosVert = float(value)
    fPosVert = property(getPosVert, setPosVert)

    def getPosHor(self):
        return self._fPosHor
    def setPosHor(self, value):
        self._fPosHor = float(value)
    fPosHor = property(getPosHor, setPosHor)

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = value
    iId = property(getId, setId)

    def getWallId(self):
        return self._iWallId
    def setWallId(self, value):
        self._iWallId = value
    iWallId = property(getWallId, setWallId)

    def addFace(self, cFace):
        try:
            self.lstExtraFaces.append(cFace)
            self.iFaceCounter = self.iFaceCounter + 1
        except:
            self.errorCode()

    def extraFacesExist(self):
        try:
            if self.lstExtraFaces is []:
                return False
            else:
                return True
        except:
            self.errorCode()
            return False


    def getFace(self):
        __doc__ = """
        first return: Is Error
        second return: Face Class for current face
        """
        try:
            if self.faceEof():
                return True, 0
            else:
                return False, self.lstExtraFaces[self.iFaceCurrent]
        except:
            self.errorCode()
            return True, 0

    def faceMoveFirst(self):
        __doc__ = """
        return boolean: is error
        """
        try:
            self.iFaceCurrent = 0
            return False
        except:
            self.errorCode()
            return True

    def faceMoveNext(self):
        __doc__ = """
        return boolean: is error
        """
        try:
            if self.iFaceCounter > self.iFaceCurrent:
                self.iFaceCurrent = self.iFaceCurrent + 1
                return False
            else:
                return True
        except:
            self.errorCode()
            return True

    def faceEof(self):
        try:
            if self.iFaceCounter > self.iFaceCurrent:
                return False
            else:
                return True
        except:
            self.errorCode()

    def faceMaxId(self):
        try:
            iMax = 0
            for cTempFace in self.lstExtraFaces:
                if iMax < cTempFace.iId:
                    iMax = cTempFace.iId
            return iMax
        except:
            self.errorCode()
            return 0



class ClsVertex(ClsBasics):
    __doc__ = """
    ID - corisponds to the id in the list of vertexs within Mesh object
    Orientation - Orientation within the feature, eg. the beginning or the end of the door
    (Orientation note: we don't want to connect the vertexes on the left side
    of a door with the vertexes on the divider to the right of the door)
    Orientation Options: 'start', 'middle', 'end'
    Side - This refers to which side of the wall the vertex is positioned on
    Side Options:'a', 'b', 'middle'
    """
    def __init__(self, x, y, z):
        self.initialiseBasicsClass()
        try:
            self.sClassName = "ClsVertex"

            self.fX = x
            self.fY = y
            self.fZ = z
            self.iId = 0
            self.iFeatureId = 0
        except:
            self.errorCode()

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = value
    iId = property(getId, setId)

    def getFeatureId(self):
        return self._iFeatureId
    def setFeatureId(self, value):
        self._iFeatureId = value
    iFeatureId = property(getFeatureId, setFeatureId)

    def getWallId(self):
        return self._iWallId
    def setWallId(self, value):
        self._iWallId = value
    iWallId = property(getWallId, setWallId)

    def getX(self):
        return self._fX
    def setX(self, value):
        self._fX = value
    fX = property(getX, setX)

    def getY(self):
        return self._fY
    def setY(self, value):
        self._fY = value
    fY = property(getY, setY)

    def getZ(self):
        return self._fZ
    def setZ(self, value):
        self._fZ = value
    fZ = property(getZ, setZ)

    def getOrientation(self):
        return self._sOrientation
    def setOrientation(self, value):
        self._sOrientation = value
    sOrientation = property(getOrientation, setOrientation)

    def getSide(self):
        return self._sSide
    def setSide(self, value):
        self._sSide = value
    sSide = property(getSide, setSide)

    def printPosition(self, sTitle):
        try:
            bTurnOn = False
            if bTurnOn == True:
                print sTitle
                print "ID: " + str(self.iId) + "X: " + str(self.fX) + "  Y: " + str(self.fY) + "  Z: " + str(self.fZ)
        except:
            self.errorCode()

class ClsFace(ClsBasics):
    __doc__ = """
    ID - corisponds to the id in the list of vertexs within Mesh object
    """
    def __init__(self, iFeatureId, lstVertesIds):
        self.initialiseBasicsClass()
        try:
            self.iId = 0
            self.iFeatureId = iFeatureId
            self.lstVertexIds = []
            self.iVertexCounter = 0
            for iVertexId in lstVertesIds:
                self.lstVertexIds.append(iVertexId)
                self.iVertexCounter = self.iVertexCounter + 1
            self.iCurrentVertex = 0
        except:
            self.errorCode()

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = value
    iId = property(getId, setId)

    def getFeatureId(self):
        return self._iFeatureId
    def setFeatureId(self, value):
        self._iFeatureId = value
    iFeatureId = property(getFeatureId, setFeatureId)

    def isFoundVertexId(self, iVertexId):
        try:
            bIsFound = False
            for iTemp in self.lstVertexIds:
                if iVertexId == iTemp:
                    bIsFound = True
                    return True
            if bIsFound == False:
                return False
        except:
            self.errorCode()
            return False

    def hasVertexes(self):
        try:
            if self.lstVertexIds is []:
                return False
            else:
                return True
        except:
            self.errorCode()
            return False

    def addVertex(self, iVertexId):
        try:
            if self.isFoundVertexId(iVertexId):
                self.lstVertexIds.append(iVertexId)
        except:
            self.errorCode()

    def getVertexCounter(self):
        return self._cVertexCounter
    iVertexCounter = property(getVertexCounter)

    def getVertexId(self):
        __doc__ = """
        first return: is error
        second return: vertex id
        """
        try:
            if self.iVertexCounter > self.iCurrentVertex:
                return False, self.lstVertexIds[self.iCurrentVertex]
            else:
                return True, 0
        except:
            self.errorCode()
            return True, 0

    def vertexMoveFirst(self):
        self.iCurrentVertex = 0

    def vertexMoveNext(self):
        __doc__ = """
        return boolean: is error
        """
        try:
            if self.iVertexCounter > self.iCurrentVertex:
                self.iCurrentVertex = self.iCurrentVertex + 1
                return False
            else:
                return True
        except:
            self.errorCode()
            return True

    def vertexMove(self, iPosition):
        __doc__ = """
        return boolean: is error
        """
        try:
            if self.iVertexCounter > iPosition and iPosition >= 0:
                self.iCurrentVertex = iPosition
                return False
            else:
                return True
        except:
            self.errorCode()
            return True

    def vertexBof(self):
        __doc__ = """
        return boolean: is error
        """
        try:
            if self.iCurrentVertex == 0:
                return True
            else:
                return False
        except:
            self.errorCode()
            return True

    def vertexEof(self):
        try:
            if self.iVertexCounter > self.iCurrentVertex:
                return False
            else:
                return True
        except:
            self.errorCode()

class ClsFeatureElement(ClsBasics):
    __doc__ = """
    type = 'corner', 'centre of rotation'
    """
    global lstVariables, lstVertexes

    def __init__(self):
        self.iId = 0
        self.sName = ""
        self.sType = ""
        self.vPosition = Mathutils.Vector(0.0, 0.0, 0.0)

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = int(value)
    iId = property(getId, setId)

    def getName(self):
        return self._sName
    def setName(self, value):
        self._sName = value
    sName = property(getName, setName)

    def getType(self):
        return self._sType
    def setType(self, value):
        self._sType = value
    sType = property(getType, setType)

    def getPosition(self):
        return self._vPosition
    def setPosition(self, value):
        self._vPosition = value
    vPosition = property(getPosition, setPosition)

class ClsFeatureVariable(ClsBasics):
    __doc__ = """
    type = 'corner', 'centre of rotation', 'number of vertexes'
    """
    def __init__(self, iFeatureId, sName, sType, Amount):
        self.iId = 0
        self.iFeatureId = iFeatureId
        self.sName = sName
        self.sType = sType
        self.Amount = Amount

    def getId(self):
        return self._iId
    def setId(self, value):
        self._iId = int(value)
    iId = property(getId, setId)

    def getFeatureId(self):
        return self._iFeatureId
    def setFeatureId(self, value):
        self._iFeatureId = int(value)
    iFeatureId = property(getFeatureId, setFeatureId)

    def getName(self):
        return self._sName
    def setName(self, value):
        self._sName = value
    sName = property(getName, setName)

    def getType(self):
        return self._sType
    def setType(self, value):
        self._sType = value
    sType = property(getType, setType)

    def getAmount(self):
        return self._Amount
    def setAmount(self, value):
        self._Amount = value
    Amount = property(getAmount, setAmount)

#class ClsVertexGroups(ClsBasics):
#    __doc__ = """
#    A group of vertexes that need to be connected
#    """
#    def __init__(self, iFeatureId, sName, sType, Amount):
#        self.iId = 0
#        self.iFeatureId = iFeatureId
#        self.sName = sName
#        self.sType = sType
#        self.lstVertexes = []
#
#    def getId(self):
#        return self._iId
#    def setId(self, value):
#        self._iId = int(value)
#    iId = property(getId, setId)
#
#    def getFeatureId(self):
#        return self._iFeatureId
#    def setFeatureId(self, value):
#        self._iFeatureId = int(value)
#    iFeatureId = property(getFeatureId, setFeatureId)
#
#    def getName(self):
#        return self._sName
#    def setName(self, value):
#        self._sName = value
#    sName = property(getName, setName)
#
#    def getType(self):
#        return self._sType
#    def setType(self, value):
#        self._sType = value
#    sType = property(getType, setType)
#
#    def addVertex(self, iVertexId, iOrder = None):
#        self.lstVertexes.append()
