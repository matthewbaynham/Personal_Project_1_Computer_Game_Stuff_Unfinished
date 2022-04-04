#!BPY

"""
Name: 'Build Walls'
Blender: 248
Group: 'Object'
Tooltip: 'Writing my python stuff....'
"""
import binascii

__author__ = "Matthew Baynham"
__date__ ="$08-May-2009 12:33:38$"
__name__ = "MyWalls"
__module__ = "MyWalls"
__url__ = ("blender", "stuff","my homepage, http://www.doesnt-Exist.com",)
__version__ = "0.2"
__bpydoc__ = """
To Do
=====
1)  Colour and Texture

2)  square Doors
    i)  Check doors can handle extra vertexes on the sides of the doorway

3)  arch doors
    i)  create arch door with double curve
    ii) the single arch doors need to have a multiplier ratio, so that the
        curve can be stretched by multipling it.

4)  tops of walls and ends of the wall,
    i)  add a property to  feature to define if the the top of end if
        cunnecting side A and side B
    ii) if the feature has this property set then connect the top and side

5)  windows
    i)  arched (round top sqare bottom)

6)  Features can be assigned a floor section if two features in a wall are
    assigned a floor section then all features in between are assigned the
    same floor section.

7)  pull in design of structure (room, building, etc) from text file.

8)  make the structure (room, building, etc), the point of focus and not walls
    so we are not creating a series of walls we are creating a building.
"""





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
    #sys.path.append("C:/Python26/Lib/lib-tk")
#    sys.path.append("C:/Python26/Lib")
#    sys.path.append("C:/Code/C++/Python Import")

    #sys.path.append("C:/Python26/Lib/site-packages/wx-2.8-msw-unicode/wxPython")
else:
    sys.path.append("./")
    sys.path.append("./MyWalls/src")
    sys.path.append("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyWalls/src")
    #sys.path.append("C:/Python26/Lib/lib-tk")
    sys.path.append("C:/Python26/Lib")
    sys.path.append("C:/Code/C++/Python Import")

    sys.path.append("C:/Python26/Lib/site-packages/wx-2.8-msw-unicode/wxPython")

#from modulefinder import ModuleFinder
#
#finder = ModuleFinder()
#finder.run_script("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyWalls/src/MyBrick.py")
#finder.run_script("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyWalls/src/WallWithDoors.py")
#finder.run_script("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyWalls/src/modBasics.py")


#finder.run_script("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyClassProject/src/myClass.py")
#finder.run_script("C:/Program Files/Blender Foundation/Blender/.blender/scripts/MyClassProject/src/MyGUI.py")


#from MyGUI import MY_GUI
#from myClass import MY_BOX
#from MyWxPythonGui import MyWxGUI
#import MyWxPythonGui

import modBuilding
reload(modBuilding)
import modWall
reload(modWall)
import modBasics
reload(modBasics)
import modDataObjects
reload(modDataObjects)
import modMisc
reload(modMisc)
import modMaths
reload(modMaths)
import modTextFile
reload(modTextFile)
import modContainer
reload(modContainer)

from modBasics import ClsBasics
from modDataObjects import ClsFeature, ClsVertex, ClsFace, ClsFeatureVariable
from modMisc import ClsMisc
from modMaths import ClsMaths
from modTextFile import ClsTextFile
from modBuilding import ClsBuilding


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

#objWall = modWall.ClsWall("fred", 3.0, 1.0, 35.0)
#
##add divider
#iFeatureFirstId = objWall.addFeature("first thing added", "divider", "stuff", 3.0, 0, 4.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureFirstId, "first divider", "extra vertexes", 1)
#
##add door
#iFeatureId = objWall.addFeature("first thing added", "door", "square", 4.0, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height", 2)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway width", 0.4)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway lintol extra vertexes", 4)
#
##add divider
#iFeatureSecondId = objWall.addFeature("first thing added", "divider", "stuff", 8.0, 0, 2.5, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureSecondId, "second divider", "extra vertexes", 5)
#
##add door
#iFeatureId = objWall.addFeature("first thing added", "door", "square", 9.1, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height", 2.5)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway width", 0.2)
#
##add divider
#iFeatureSecondId = objWall.addFeature("first thing added", "divider", "stuff", 10.0, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureSecondId, "second divider", "extra vertexes", 5)
#
##add door
#iFeatureId = objWall.addFeature("arch door way", "door", "single arch", 14.0, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height", 2)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway width", 0.4)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway lintol extra vertexes", 8)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height of arch centre", 1.75)
#
##add divider
#iFeatureSecondId = objWall.addFeature("first thing added", "divider", "stuff", 15.5, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureSecondId, "second divider", "extra vertexes", 5)
#
##add door
#iFeatureId = objWall.addFeature("arch door way", "door", "single arch", 17.0, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height", 2)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway width", 0.5)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway lintol extra vertexes", 9)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "doorway Height of arch centre", 1.75)
#
##add divider
#iFeatureSecondId = objWall.addFeature("first thing added", "divider", "stuff", 18.5, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureSecondId, "second divider", "extra vertexes", 5)
#
##add window
#iFeatureId = objWall.addFeature("first window", "window", "square", 20.0, 1.8, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window frame Height", 1)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window frame width", 1.5)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window lintol extra vertexes horizontal", 5)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window lintol extra vertexes vertical", 3)
#
##add divider
#iFeatureSecondId = objWall.addFeature("first thing added", "divider", "stuff", 21.5, 0, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureSecondId, "second divider", "extra vertexes", 5)
#
##add window
#iFeatureId = objWall.addFeature("first window", "window", "round", 23.0, 1.8, 3.0, 0)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window frame Height", 1.2)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window frame width", 1.7)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window Height", 1)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window width", 1.5)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window lintol extra vertexes horizontal", 11)
#bError, iVariableId = objWall.addFeatureVariables(iFeatureId, "door stuff", "window lintol extra vertexes vertical", 9)
#
#
#
#objWall.buildWall()
#
#print "Warnings:"
#objWall.printWarnings()



objSourceFile = ClsTextFile("/root/Test Wall 005.txt")
bHasErrors, objHouse = objSourceFile.readData()
if bHasErrors == True:
    print ""
    print "Please check source file."
else:
    # @type objHouse ClsBuilding
    objHouse.buildBuilding()

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

#print "Test ClsTextFile: Start"
#CFile = ClsTextFile("/root/Test File.txt")
#CFile.readData()
#print "Test ClsTextFile: End"
#print string.rstrip("0123456789", 2)

