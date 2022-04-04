#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ = "MyGUI"
__version__ = "0.1"
__bpydoc__ = """
This class is to experiment with classes and stuff in seperate files
"""

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import Blender
from Blender import Draw, BGL, Window, NMesh, Mathutils
#import math
#from math import *


class MY_GUI:
    GUI_TYPE_WALL_NORMAL           = 1
    GUI_TYPE_WALL_PRISON_BARS      = 2

    EVT_BTN_CRE          =  1
    EVT_BTN_ESC          =  2
    EVT_BTN_TEST         =  3
    EVT_SLI_WIDTH        =  4
    EVT_SLI_HIEGHT       =  5
    EVT_SLI_NUM_BARS     =  6
    EVT_SLI_NUM_HOR      =  7
    EVT_SLI_BAR_WIDTH    =  8
    EVT_SLI_OFFSET_X     =  9
    EVT_SLI_OFFSET_Y     = 10
    EVT_SLI_OFFSET_Z     = 11
    EVT_TXT_TITLE        = 12

    def event(evt, val):
        if evt == Draw.ESCKEY:
            Draw.Exit()
        return

    def button_event(evt):
        global wallWidth, wallHieght
        if evt == EVT_BTN_CRE:
                    createWall()
        elif evt == EVT_BTN_ESC:
            Draw.Exit()
        elif evt == EVT_SLI_OFFSET_X or evt == EVT_SLI_OFFSET_Y or evt == EVT_SLI_OFFSET_Z:
                    moveCursor()
        elif evt == EVT_BTN_TEST:
                    moveCursor()
                    messageBox()
        return

    def prisionBarsGUI(self):
        #do all the stuff
        Draw.String("Creating Walls: Prison Bars", EVT_TXT_TITLE, 5, 600, 400, 30, "", 64, "Creating Walls")

        sliderWallWidth          = Draw.Slider ("Wall Width: ",             self.EVT_SLI_WIDTH,     5, 50,  400, 15, 1.0,    0.5,  50.0,  0, "Over all width of the wall of bars")
        sliderWallHieght         = Draw.Slider ("Wall Hieght: ",            self.EVT_SLI_HIEGHT,    5, 80,  400, 15, 1.0,    0.5,  10.0,  0, "Over all hieght of the wall of bars")
        sliderNumBars            = Draw.Slider ("Number of Bars: ",         self.EVT_SLI_NUM_BARS,  5, 110, 400, 15,   2,      1,   500,  0, "Number of bars in this prison wall")
        sliderNumHor             = Draw.Slider ("Number of Horizontals: ",  self.EVT_SLI_NUM_HOR,   5, 140, 400, 15,   2,      2,    10,  0, "Number of Horizontal seperators")
        sliderBarThickness       = Draw.Slider ("Bar Thickness: ",          self.EVT_SLI_BAR_WIDTH, 5, 170, 400, 15, 0.1,    0.1,  10.0,  0, "Thickness of the Bars")
        sliderBarOffSetX         = Draw.Slider ("Off Set X: ",              self.EVT_SLI_OFFSET_X,  5, 200, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen X Axis")
        sliderBarOffSetY         = Draw.Slider ("Off Set Y: ",              self.EVT_SLI_OFFSET_Y,  5, 230, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen Y Axis")
        sliderBarOffSetZ         = Draw.Slider ("Off Set Z: ",              self.EVT_SLI_OFFSET_Z,  5, 260, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen Z Axis")

        Draw.PushButton ("Create!", self.EVT_BTN_CRE, 5, 5, 80, 25, "Create the World")
        Draw.PushButton ("Exit",    self.EVT_BTN_ESC, 106, 5, 80, 25, "Lets get out of here")
        Draw.PushButton ("Test",    self.EVT_BTN_TEST, 205, 5, 80, 25, "Test something")

    def wallGUI(self):
        #do all the stuff
        Draw.String("Creating Walls: Prison Bars", self.EVT_TXT_TITLE, 5, 600, 400, 30, "", 64, "Creating Walls")

        sliderWallWidth          = Draw.Slider ("Wall Width: ",     self.EVT_SLI_WIDTH,     5, 50,  400, 15, 1.0,    0.5,  50.0,  0, "Over all width of the wall of bars")
        sliderWallHieght         = Draw.Slider ("Wall Hieght: ",    self.EVT_SLI_HIEGHT,    5, 80,  400, 15, 1.0,    0.5,  10.0,  0, "Over all hieght of the wall of bars")
        sliderBarOffSetX         = Draw.Slider ("Off Set X: ",      self.EVT_SLI_OFFSET_X,  5, 200, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen X Axis")
        sliderBarOffSetY         = Draw.Slider ("Off Set Y: ",      self.EVT_SLI_OFFSET_Y,  5, 230, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen Y Axis")
        sliderBarOffSetZ         = Draw.Slider ("Off Set Z: ",      self.EVT_SLI_OFFSET_Z,  5, 260, 400, 15, 0.0, -100.1, 100.0,  0, "Off Set from Origen Z Axis")

        Draw.PushButton ("Create!",   self.EVT_BTN_CRE, 5, 5, 80, 25, "Create the World")
        Draw.PushButton ("Exit",      self.EVT_BTN_ESC, 107, 5, 80, 25, "Lets get out of here")
        Draw.PushButton ("Test",      self.EVT_BTN_TEST, 205, 5, 80, 25, "Test something")


    def __init__(self, guiType):
        """Documentation"""
        if  guiType == self.GUI_TYPE_WALL_NORMAL:
            Draw.Register (self.wallGUI, event, button_event)
        elif guiType == GUI_TYPE_WALL_PRISON_BARS:
            Draw.Register (self.prisionBarsGUI, event, button_event)

