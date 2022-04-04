#!BPY

__author__="Matthew Baynham"
__date__ ="$08-May-2009 12:34:49$"
__name__ ="modMaths"
__module__ = "modMaths"
__version__ = "0.1"
__bpydoc__ = """
module that contain some more code
"""

from Blender import NMesh, Mathutils
import math
from modBasics import ClsBasics
from modDataObjects import ClsFeature, ClsVertex, ClsFace, ClsFeatureVariable
import operator
#import modBasics
#reload(modBasics)

#Read up on the Mathutils function LineIntersect( , , , )
#doesn't work if the lines don't intersect exactly

class ClsMaths(ClsBasics):
    def closestPoint(self, cLineAVertexA, cLineAVertexB, cLineBVertexA, cLineBVertexB):
        __doc__ = """
        two lines A and B represent the edges of faces, I hope they intersect
        First return: boolean True if they do actually intersect
        Second return: vector the closest point to the intersection
        """
        try:
            vLineAVectorA = Mathutils.Vector(cLineAVertexA.fX, cLineAVertexA.fY, cLineAVertexA.fZ)
            vLineAVectorB = Mathutils.Vector(cLineAVertexB.fX, cLineAVertexB.fY, cLineAVertexB.fZ)
            vLineBVectorA = Mathutils.Vector(cLineBVertexA.fX, cLineBVertexA.fY, cLineBVertexA.fZ)
            vLineBVectorB = Mathutils.Vector(cLineBVertexB.fX, cLineBVertexB.fY, cLineBVertexB.fZ)

            vGradientA = vLineAVectorA - vLineAVectorB
            vGradientB = vLineBVectorA - vLineBVectorB

            if vGradientA == vGradientB:
                self.addWarning("Lines are parrallel")

            vOffsetA = Mathutils.Vector(cLineAVertexA.fX, cLineAVertexA.fY, cLineAVertexA.fZ)
            vOffsetB = Mathutils.Vector(cLineBVertexA.fX, cLineBVertexA.fY, cLineBVertexA.fZ)

            #starting position will be in the middle of the vertexes given
            fPositionA = 0.5
            fPositionB = 0.5

            lstDeltasA = []
            lstDeltasB = []
            fDeltaRollingAverageA = 0.0
            fDeltaRollingAverageB = 0.0

            bIsFinished = False
            iCounter = 0

            while not bIsFinished == True:
                fDeltaA = Mathutils.Rand(-1.0, 1.0) + fDeltaRollingAverageA
                fDeltaB = Mathutils.Rand(-1.0, 1.0) + fDeltaRollingAverageB

                if distanceBetweenPointsOnLine(vGradientA, vGradientB, vOffsetA, vOffsetB, fPositionA, fPositionB) > distanceBetweenPointsOnLine(vGradientA, vGradientB, vOffsetA, vOffsetB, fPositionA + fDeltaA, fPositionB = fDeltaB):
                    #adding the deltas helps
                    fPositionA = fPositionA + fDeltaA
                    fPositionB = fPositionB + fDeltaB

                    lstDeltasA.append(fDeltaA)
                    lstDeltasB.append(fDeltaB)

                    #change average to RMS
                    fDeltaRollingAverageA = self.deltaRollingAverage(lstDeltasA, 20)
                    fDeltaRollingAverageB = self.deltaRollingAverage(lstDeltasB, 20)

                iCounter = iCounter + 1
                if iCounter > 10:
                    #now start checking if we are close enough
                    if fDeltaRollingAverageA < 0.001 and fDeltaRollingAverageB < 0.001:
                        bIsFinished = True

                    #If all the deltas are in the same direction then keep going
                    #however if 30 percent are in a different then stop
                    iPositiveA, iNegativeA = deltaDirection(lstDeltasA, 50)
                    if not (iPositiveA == 0 or iNegativeA == 0):
                        if iPositiveA / (iPositiveA + iNegativeA) > 0.3 and iNegativeA / (iPositiveA + iNegativeA) > 0.3:
                            bIsFinishedA = True
                        else:
                            bIsFinishedA = False

                    iPositiveB, iNegativeB = deltaDirection(lstDeltasB, 50)
                    if not (iPositiveB == 0 or iNegativeB == 0):
                        if iPositiveB / (iPositiveB + iNegativeB) > 0.3 and iNegativeB / (iPositiveB + iNegativeB) > 0.3:
                            bIsFinishedB = True
                        else:
                            bIsFinishedB = False

                    if bIsFinishedA == True and bIsFinishedB == True:
                        bIsFinished = True
        except:
            self.errorCode()

        def distanceBetweenPointsOnLine(self, vGradientA, vGradientB, vOffsetA, vOffsetB, fPositionA, fPositionB):
            try:
                vPointA = vGradientA * fPositionA + vOffsetA
                vPointB = vGradientB * fPositionB + vOffsetB

                fRms = ((vPointA.x - vPointB.x)^2 + (vPointA.y - vPointB.y)^2 + (vPointA.z - vPointB.z)^2)^0.5
                return fRms
            except:
                self.errorCode()

        def deltaRollingAverage(self, lst, iNoItems):
            try:
                #count number of items in list
                iCounter = 0
                for iItem in lst:
                    iCounter = iCounter + 1

                fRunningTotal = 0.0
                if iCounter < iNoItems:
                    #if there are less then the max then total then
                    for iItem in lst:
                        fRunningTotal = fRunningTotal + iItem
                    return fRunningTotal / iCounter
                else:
                    #if there are more then the max then total some of them
                    iIndex = iNoItems - iCounter - 1
                    while iIndex < iCounter:
                        fRunningTotal = fRunningTotal + lst[iIndex]
                    return fRunningTotal / iNoItems
            except:
                self.errorCode()

        def deltaDirection(self, lst, iNoItems):
            try:
                #count number of items in list
                iCounter = 0
                for iItem in lst:
                    iCounter = iCounter + 1

                iPositiveCounter = 0
                iNegativeCounter = 0
                if iCounter < iNoItems:
                    for iItem in lst:
                        if not iItem == 0.0:
                            if iItem < 0.0:
                                iNegativeCounter = iNegativeCounter + 1
                            else:
                                iPositiveCounter = iPositiveCounter + 1
                return iPositiveCounter, iNegativeCounter
            except:
                self.errorCode()

    def distanceBetweenTwoClsVertexes(self, ClsVertexA, ClsVertexB):
        try:
            fXcomponent = float(math.pow((ClsVertexA.fX - ClsVertexB.fX), 2.0))
            fYcomponent = float(math.pow((ClsVertexA.fY - ClsVertexB.fY), 2.0))
            fZcomponent = float(math.pow((ClsVertexA.fZ - ClsVertexB.fZ), 2.0))

            fRms = float(math.sqrt(fXcomponent + fYcomponent + fZcomponent))

            return fRms
        except:
            self.errorCode()

    def distanceBetweenClsVertexAndAverageOfVertexList(self, ClsVertex, lstVertex):
        try:
            iCounter = 0
            fTotalX = 0.0
            fTotalY = 0.0
            fTotalZ = 0.0
            for cTemp in lstVertex:
                iCounter = iCounter + 1
                fTotalX = fTotalX + cTemp.fX
                fTotalY = fTotalY + cTemp.fY
                fTotalZ = fTotalZ + cTemp.fZ
            
            if iCounter == 0:
                return 0
            else:
                fXcomponent = math.pow((ClsVertex.fX - (fTotalX / iCounter)), 2.0)
                fYcomponent = math.pow((ClsVertex.fY - (fTotalY / iCounter)), 2.0)
                fZcomponent = math.pow((ClsVertex.fZ - (fTotalZ / iCounter)), 2.0)

                fRms = math.sqrt(fXcomponent + fYcomponent + fZcomponent)

                return fRms
        except:
            self.errorCode()

    def getClosestClsVertexFromTwoLists(self, lstClsVertexA, lstClsVertexB, lstExceptions, ClsVertexA, ClsVertexB):
        try:
            #get any distance
            fDistance = 0
            bIsFound = False
            for ClsTemp in lstClsVertexA:
                if self.isException(ClsTemp, lstExceptions) == False:
                    fDistance = self.distanceBetweenClsVertexAndAverageOfVertexList(ClsTemp, [ClsVertexA, ClsVertexB])
                    ClsClosest = ClsTemp
                    bIsFound = True
                    sLstName = "A"
            for ClsTemp in lstClsVertexB:
                if self.isException(ClsTemp, lstExceptions) == False:
                    fDistance = self.distanceBetweenClsVertexAndAverageOfVertexList(ClsTemp, [ClsVertexA, ClsVertexB])
                    ClsClosest = ClsTemp
                    bIsFound = True
                    sLstName = "B"

            #find the shortest distance
            for ClsTemp in lstClsVertexA:
                if self.isException(ClsTemp, lstExceptions) == False:
                    fDistanceTemp = self.distanceBetweenClsVertexAndAverageOfVertexList(ClsTemp, [ClsVertexA, ClsVertexB])
                    if fDistance > fDistanceTemp:
                        fDistance = fDistanceTemp
                        ClsClosest = ClsTemp
                        bIsFound = True
                        sLstName = "A"
            for ClsTemp in lstClsVertexB:
                if self.isException(ClsTemp, lstExceptions) == False:
                    fDistanceTemp = self.distanceBetweenClsVertexAndAverageOfVertexList(ClsTemp, [ClsVertexA, ClsVertexB])
                    if fDistance > fDistanceTemp:
                        fDistance = fDistanceTemp
                        ClsClosest = ClsTemp
                        bIsFound = True
                        sLstName = "B"

            if bIsFound == True:
                ClsClosest.printPosition("Next")
                return True, ClsClosest, sLstName
            else:
                cTempVertex = ClsVertex(0, 0, 0)
                return False, cTempVertex, ""
        except:
            self.errorCode()

    def isException(self, ClsVertex, lstExceptions):
        try:
            if lstExceptions is []:
                return False
            else:
                bIsFound = False
                for ClsTemp in lstExceptions:
                    if ClsTemp.iId == ClsVertex.iId:
                        bIsFound = True
                        return True
                if bIsFound == True:
                    return True
                else:
                    return False
        except:
            self.errorCode()


    def vertexIsInTriangle(self):
        __doc__ = """
        Each of the sides of the triangle is simply a line
        If for each line the vertex is on the same side as the corner of the triangle then the vertex is in the triangle
        """
        try:
            print "code not writen yet"
        except:
            self.errorCode()
