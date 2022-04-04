#!BPY
"""
Name: 'AAA Repainting Weight One'
Blender: 248
Group: 'Object'
Tooltip: 'Repaint all the weights such that each vertex has a total weight of one that will can be broken down between all the vertex groups it is in'
"""
__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="aaaRepaintAverageWeightOfOne"
__module__ = "RePaintAverageOfOne"
__version__ = "0.1"
__bpydoc__ = """
Repaints all of the painted weights so that each vertex that has
at least one painted weight will have a total weight of one
across all vertex groups.
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


#lstMeshes = bpy.data.meshes.Get()
#for mBody in lstMeshes:


is_editmode = Window.EditMode()
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


for objMesh in lstObj:
	if objMesh.type == 'Mesh':
		print "Mesh Name: " + objMesh.name
		mBody = objMesh.getData(mesh=True)
		lstWeightMap = []
		lstWeightTotal = []
		for sGroupName in mBody.getVertGroupNames():
        		print "    " + sGroupName
			lstVert = mBody.getVertsFromGroup(sGroupName, 1)
			for vVert in lstVert:
				#Vertex Group Name, Vertex Id, Old Vertex Weight, New Vertex Weight
				objVert = [sGroupName, vVert[0], vVert[1], 0.0]
				lstWeightMap.append(objVert)
				
				bIsFound = False
				if not lstWeightTotal is []:
					for tempVert in lstWeightTotal:
						if tempVert[0] == vVert[0]:
							bIsFound = True
							tempVert[1] = tempVert[1] + vVert[1]
							
				if bIsFound == False:
					tempVert = [vVert[0], vVert[1]]
					lstWeightTotal.append(tempVert)
		
		#process the vertex weights
		print "process the vertex weights"
		for tempVert in lstWeightMap:
			for vertTotal in lstWeightTotal:
				if tempVert[1] == vertTotal[0]:
					if vertTotal[1] == 0.0:
						tempVert[3] = tempVert[2]
					else:
						tempVert[3] = tempVert[2] / vertTotal[1]
		
		
		#update the vertex weights
		print "update the vertex weights"
		for tempVert in lstWeightMap:
			print tempVert
			lstId = []
			lstId.append(int(tempVert[1]))
			mBody.assignVertsToGroup(str(tempVert[0]), lstId, float(tempVert[3]), Blender.Mesh.AssignModes.REPLACE)
#			mBody.assignVertsToGroup(str(tempVert[0]), lstId, float(tempVert[3]), 'replace')





#Window.WaitCursor(1)
#me = ob_act.getData(mesh=1) # old NMesh api is default



#for mBody in bpy.data.meshes:
    #print "Mesh: " + mBody.name
    #print type(mBody)
    #print mBody.activeUVLayer
    
    ##objBody = mBody.getData()
    #object.link(mBody)
    
    #for sGroupName in mBody.getVertGroupNames():
        #print sGroupName


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
print ""
print ""
print ""
print ""
print ""
