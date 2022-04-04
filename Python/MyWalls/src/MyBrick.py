 #!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="MyBrick"
__module__ = "MyBrick"
__version__ = "0.1"
__bpydoc__ = """
This class is to experiment with classes and stuff in seperate files
"""

#import Blender
#from Blender import Draw, BGL, Window, NMesh, Mathutils
from Blender import NMesh, Mathutils
#import math
#from math import *

class MyBox():
    #some code just to see if I can write a class

    def vOffset(self):
        #The vOffset property datatype Mathutil.vector.
        def getOffset(self):
            return self._vOffset
        def setOffset(self, value):
            self._vOffset = value
        return locals()
        vOffset = property(self.getOffset, self.setOffset)

    def fHieght(self):
        #The fHieght property.
        def getHieght(self):
            return self._fHieght
        def setHieght(self, value):
            self._fHieght = float(value)
        return locals()
        fHieght = property(self.getHieght, self.setHieght)

    def fWidth(self):
        #The fWidth property.
        def getWidth(self):
            return self._fWidth
        def setWidth(self, value):
            self._fWidth = float(value)
        return locals()
        fWidth = property(self.getWidth, self.setWidth)

    def fDepth(self):
        #The fDepth property.
        def getDepth(self):
            return self._fDepth
        def setDepth(self, value):
            self._fDepth = float(value)
        return locals()
        fDepth = property(self.getDepth, self.setDepth)

    def iRotationVertical(self):
        #The fDepth property.
        def getRotationVertical(self):
            return self._iRotationVertical
        def setRotationVertical(self, value):
            self._iRotationVertical = value
        return locals()
        iRotationVertical = property(self.getRotationVertical, self.setRotationVertical)

    def __init__(self):
        """Documentation"""
        self._fHieght = 0.0
        self._fWidth = 0.0
        self._fDepth = 0.0
        self._vOffset = Mathutils.Vector(0.0, 0.0, 0.0)

    def createBox(self):
        #Create the mesh object
        myBox = NMesh.GetRaw()
        #Z = Hieght
        #X = Width
        #Y = Depth
        #add the vertexs

        objOffset = Mathutils.Vector(0.0, 0.0, 0.0)
        objOffset = self.vOffset
        
        fOffsetX = float(objOffset.x)
        fOffsetY = float(objOffset.y)
        fOffsetZ = float(objOffset.z)
        
        objVert = NMesh.Vert(fOffsetX + (float(self.fWidth) / 2), fOffsetY + (float(self.fDepth) / 2), fOffsetZ + (float(self.fHieght) / 2))
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX + float(self.fWidth) / 2, fOffsetY + float(self.fDepth) / 2, fOffsetZ - float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX + float(self.fWidth) / 2, fOffsetY - float(self.fDepth) / 2, fOffsetZ + float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX + float(self.fWidth) / 2, fOffsetY - float(self.fDepth) / 2, fOffsetZ - float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX - float(self.fWidth) / 2, fOffsetY + float(self.fDepth) / 2, fOffsetZ + float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX - float(self.fWidth) / 2, fOffsetY + float(self.fDepth) / 2, fOffsetZ - float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX - float(self.fWidth) / 2, fOffsetY - float(self.fDepth) / 2, fOffsetZ + float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        objVert = NMesh.Vert(fOffsetX - float(self.fWidth) / 2, fOffsetY - float(self.fDepth) / 2, fOffsetZ - float(self.fHieght) / 2)
        myBox.verts.append(objVert)

        #Fill in the faces
        #right
        objFaceRight = NMesh.Face()

        objFaceRight.v.append(myBox.verts[0])
        objFaceRight.v.append(myBox.verts[3])
        objFaceRight.v.append(myBox.verts[1])

        myBox.faces.append(objFaceRight)

        objFaceRight = NMesh.Face()

        objFaceRight.v.append(myBox.verts[0])
        objFaceRight.v.append(myBox.verts[2])
        objFaceRight.v.append(myBox.verts[3])

        myBox.faces.append(objFaceRight)

        #left
        objFaceLeft = NMesh.Face()

        objFaceLeft.v.append(myBox.verts[4])
        objFaceLeft.v.append(myBox.verts[7])
        objFaceLeft.v.append(myBox.verts[5])

        myBox.faces.append(objFaceLeft)

        objFaceLeft = NMesh.Face()

        objFaceLeft.v.append(myBox.verts[4])
        objFaceLeft.v.append(myBox.verts[6])
        objFaceLeft.v.append(myBox.verts[7])

        myBox.faces.append(objFaceLeft)

        #Back
        objFaceBack = NMesh.Face()

        objFaceBack.v.append(myBox.verts[4])
        objFaceBack.v.append(myBox.verts[5])
        objFaceBack.v.append(myBox.verts[1])

        myBox.faces.append(objFaceBack)

        objFaceBack = NMesh.Face()

        objFaceBack.v.append(myBox.verts[0])
        objFaceBack.v.append(myBox.verts[4])
        objFaceBack.v.append(myBox.verts[1])

        myBox.faces.append(objFaceBack)

        #Front
        objFaceFront = NMesh.Face()

        objFaceFront.v.append(myBox.verts[2])
        objFaceFront.v.append(myBox.verts[7])
        objFaceFront.v.append(myBox.verts[3])

        myBox.faces.append(objFaceFront)

        objFaceFront = NMesh.Face()

        objFaceFront.v.append(myBox.verts[2])
        objFaceFront.v.append(myBox.verts[6])
        objFaceFront.v.append(myBox.verts[7])

        myBox.faces.append(objFaceFront)

        #Bottom
        objFaceBottom = NMesh.Face()

        objFaceBottom.v.append(myBox.verts[1])
        objFaceBottom.v.append(myBox.verts[7])
        objFaceBottom.v.append(myBox.verts[3])

        myBox.faces.append(objFaceBottom)

        objFaceBottom = NMesh.Face()

        objFaceBottom.v.append(myBox.verts[1])
        objFaceBottom.v.append(myBox.verts[5])
        objFaceBottom.v.append(myBox.verts[7])

        myBox.faces.append(objFaceBottom)

        #Top
        objFaceTop = NMesh.Face()

        objFaceTop.v.append(myBox.verts[4])
        objFaceTop.v.append(myBox.verts[2])
        objFaceTop.v.append(myBox.verts[6])

        myBox.faces.append(objFaceTop)

        objFaceTop = NMesh.Face()

        objFaceTop.v.append(myBox.verts[4])
        objFaceTop.v.append(myBox.verts[0])
        objFaceTop.v.append(myBox.verts[2])

        myBox.faces.append(objFaceTop)

        #Don't understand yet
        objMyBox = NMesh.PutRaw(myBox)