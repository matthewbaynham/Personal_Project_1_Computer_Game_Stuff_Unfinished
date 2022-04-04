#!BPY
"""
Name: 'AAA Find Paint Groups for Vertex'
Blender: 248
Group: 'Object'
Tooltip: 'Repaint all the weights such that each vertex has a total weight of one that will can be broken down between all the vertex groups it is in'
"""
__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="paintWeightGroupsForVertex"
__module__ = "aaaPaintWeightGroupsForVertex"
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

def isInLst(xItem, lst):
    bIsFound = False
    for x in lst:
        if x == xItem:
            bIsFound = True
            return bIsFound
    if bIsFound == False:
        return bIsFound




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

        lstSelectedVertexIds = []
        for v in mBody.verts:
            if v.sel == 1:
                lstSelectedVertexIds.append(v.index)

        for x in lstSelectedVertexIds:
            print "Vertex Id: " + str(x)

        lstUnique = []
        for sGroupName in mBody.getVertGroupNames():
            lstVert = mBody.getVertsFromGroup(sGroupName, 1)
            for vVert in lstVert:
                if vVert[1] > 0.0:
                    if isInLst(vVert[0], lstSelectedVertexIds): 
                        print sGroupName + "  " + str(vVert[1])
                        if not(isInLst(sGroupName, lstUnique)):
                            lstUnique.append(sGroupName)

        print "Unique List"
        for xItem in lstUnique:
            print xItem



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
