#!BPY
"""
Name: 'AAA Fixing lonely Vertexes, which are not assigned to any bone'
Blender: 249
Group: 'Object'
Tooltip: 'Repaint all the weights such that each vertex has a total weight of one that will can be broken down between all the vertex groups it is in'
"""
__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="aaaFixingLonelyVertexes"
__module__ = "aaaFixingLonelyVertexes"
__version__ = "0.1"
__bpydoc__ = """
For all the vertexes selected we will print out a list of vertex groups which have the vertex selected with paint weight greater then 0.0
"""

import Blender
#from Blender import Draw, BGL, Window, NMesh, Mathutils
from Blender import Mesh, NMesh, Scene, Window, Draw
import bpy
#import math
#from math import *





#import Blender
#from Blender import Draw, BGL, Window, NMesh, Mathutils
#from Blender import NMesh, Mathutils
#import math
from math import *

import sys
print sys.platform
import operator
import string
import StringIO
import curses.ascii

if sys.platform == "linux2":
    sys.path.append("./")
    sys.path.append("./MyWalls/src")
    sys.path.append("/usr/lib/blender/.blender/scripts/MyWalls/src")
else:
    sys.path.append("./")
    sys.path.append("./MyWalls/src")
    sys.path.append("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyWalls/src")
    #sys.path.append("C:/Python26/Lib/lib-tk")
    sys.path.append("C:/Python26/Lib")
    sys.path.append("C:/Code/C++/Python Import")

    sys.path.append("C:/Python26/Lib/site-packages/wx-2.8-msw-unicode/wxPython")

bPrintSystemInfo = False

if bPrintSystemInfo == True:
    print ""
    print "System Info"
    print "OS: " + sys.platform
    print "sys.prefix " + sys.prefix
    print "Python Version " + sys.version
    print ""
    print "Modules loaded:"
    for mod in sys.modules:
        print "    " + (mod)
    print ""

#def isInLst(iVertexId, lst):
#    bIsFound = False
#    for x in lst:
#        if x == iVertexId:
#            bIsFound = True
#            return bIsFound
#    if bIsFound == False:
#        return bIsFound

#lstMeshes = bpy.data.meshes.Get()
#for mBody in lstMeshes:

#need to exit edit mode for the v.sel == 1 to work

is_editmode = Window.EditMode()
Window.EditMode(0)
Window.EditMode(1)
Window.EditMode(0)

# Gets the current scene, there can be many scenes in 1 blend file.
# Saves the editmode state and go's out of 
# editmode if its enabled, we cant make
# changes to the mesh data while in editmode.
sce = bpy.data.scenes.active

# Get the active object, there can only ever be 1
# and the active object is always the editmode object.
lstObj = sce.getChildren()

print "Started"
for objMesh in lstObj:
    if objMesh.type == 'Mesh':
        print "Mesh Name: " + objMesh.name
        mBody = objMesh.getData(mesh=True)

#compile a list of all the vertex id's in the mesh
        lstAllVertexes = []
        for v in mBody.verts:
            lstTemp = [v.index, False] #vertex id and weight is found
            lstAllVertexes.append(lstTemp)

#loop through all the vertex groups and for each vertex find it in the lstAllVertexes list and mark it as found
        print ""
        print "checking vertex groups"
        for sGroupName in mBody.getVertGroupNames():
            print sGroupName
            lstVert = mBody.getVertsFromGroup(sGroupName, 1)
            for vVert in lstVert:
                if vVert[1] > 0.0:
                    for v in lstAllVertexes:
                        if vVert[0] == v[0]:
                            v[1] = True

##loop through the list lstAllVertexes and print out the vertex id's found
#		for w in lstAllVertexes:
#		      for v in mBody.verts:
#			  if w[0] == v.index:
#			      if w[1] == True:
#				  v.sel = 0
#			      else:
#				  v.sel = 1

#for each id in lstAllVertexes we will get all the faces and create a list of vertex id's
#then we will loop through the vertex groups of these and give our lonely vertex the average weight
        print ""
        print "Fixing lonely Vertexes"
        for vLonelyVertex in lstAllVertexes:
            if vLonelyVertex[1] == False:
                print "Vertex is lonely " + str(vLonelyVertex[0])
                lstAverageWeights = []
                fTotalWeight = 0.0
                for fTempFace in mBody.faces:
                    bFaceIsConnected = False
                    for v in fTempFace.verts:
                        if v.index == vLonelyVertex[0]:
                            bFaceIsConnected = True
                    if bFaceIsConnected == True:
                        for sGroupName in mBody.getVertGroupNames():
                            lstVert = mBody.getVertsFromGroup(sGroupName, 1)
                            lstTemp = [sGroupName, 0.0]
                            for vVert in lstVert:
                                for v in fTempFace.verts:
                                    if vVert[0] == v.index:
                                        fTotalWeight = fTotalWeight + vVert[1]
                                        lstTemp[1] = lstTemp[1] + vVert[1]
                            if lstTemp[1] > 0.0:
                                lstAverageWeights.append(lstTemp)
                if fTotalWeight > 0.0:
                    for newWeights in lstAverageWeights:
                        if newWeights[1] / fTotalWeight > 0.0:
                            print "    Group: " + newWeights[0] + "    weight: " + str(newWeights[1] / fTotalWeight)
                            lstLonelyVertexes = []
                            lstLonelyVertexes.append(int(vLonelyVertex[0]))
                            mBody.assignVertsToGroup(str(newWeights[0]), lstLonelyVertexes, 0.0, Blender.Mesh.AssignModes.ADD)
                            mBody.assignVertsToGroup(str(newWeights[0]), lstLonelyVertexes, float(newWeights[1] / fTotalWeight), Blender.Mesh.AssignModes.REPLACE)

print ""
print "Finished"
print ""
print ""
print ""
print ""
print ""
print ""
print ""
print ""
print ""
