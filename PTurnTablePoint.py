from PFunc import *
import PTrackPoint

import math

class PTurnTablePoint(PTrackPoint.PTrackPoint):
    def __init__(self, master, coord, number, tokens=None):
        PTrackPoint.PTrackPoint.__init__(self, master, coord, number, tokens)
        self.Type='PTurnTablePoint'
        self.Circle=None
        self.AdjustCoords=self.KeepOnCircle

    def SetCircle(self, circle):
        self.Circle=circle
        self.Circle.AddCircumferencePoint(self)

    def IsStubEnd(self):
        return 3 # The point is between a turntable and the track

    def KeepOnCircle(self, coords):
        if self.Circle == None:
            return coords
        center=self.Circle.TellCenter().TellCoord()
        difCoord=(coords[0]-center[0],coords[1]-center[1])

        #yes, I know this has overflow problems if the distances are too large
        #they shouldn't be here
        dist=math.sqrt(difCoord[0]*difCoord[0] + difCoord[1]*difCoord[1])
        radius=self.Circle.TellRadius()
        return (center[0] + difCoord[0]*radius/dist, center[1] + difCoord[1]*radius/dist)
    
    def IsGap(self):
        """TurnTablePoints are never block gaps"""
        return False
