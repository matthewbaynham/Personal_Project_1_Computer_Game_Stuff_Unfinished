#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modFloor"
__module__ = "modFloor"
__version__ = "0.1"
__bpydoc__ = """
Just the classes that contain all the data
"""

from modBasics import ClsBasics
from Blender import Mathutils
import operator
#import modBasics
#reload(modBasics)
#import fileIO

class ClsFloor(ClsBasics):
    __doc__ = """
    The out line of the floor is a list of vertexes that either belong to the bottom 
    of features of walls or other vertexes (eg the edge of a balcony)
    
    Divide the floor into sections which will not have any concave corners. Loop around
    the edge and when a corner is concave then cut that corner and complete that section

    When completing each section we need to full the space with triangles (Faces), when
    each triangle is calculated we need to if there are any features in the middle
    (eg stair wells) and mark these to come back to later.

    Well will need to then full in all the spaces around the features in the middle such
    as stair wells.

    Now think about the edge of the balcony.
    """
    def __init__(self):
        self.initialiseBasicsClass()
        try:
            self.iRecordNo = 0
            print "not written yet"
        except:
            self.errorCode()

    def getTypeOfRecord(self):
        try:
            #the record could be a door, a divider, a window, a wall, a floor
            return self._sTypeOfRecord
        except:
            self.errorCode()
    typeOfRecord = property(getTypeOfRecord)
