from PFunc import *
import PPoint

import math

# Constants for point and signal sizes
SIGSIZE=10
POINTSIZE=10

class PCenterPoint(PPoint.PPoint):
    def __init__(self, master, coord, number, tokens=None):
        PPoint.PPoint.__init__(self, master, coord, number)

        self.Type='PCenterPoint'
        self.DrawShape=self.DrawCenterPoint
        self.DragShape=self.DragCenterPoint
        self.UpdateShape=self.UpdateCenterPoint
        self.DrawShape()
        #self.SetMode()

    def DrawCenterPoint(self):
        self.Undraw()
        if self.PM.Mode=='Edit':
            self.DrawAsBox()
            self.PointDrawn=True
            #self.DefineBindings()
        elif self.PM.Mode=='Run':
            self.PointDrawn=True

    def DragCenterPoint(self):
        if self.PM.Scale<self.PM.MinPointScale and self.PointDrawn:
            self.Undraw()
        elif self.PM.Scale>=self.PM.MinPointScale and not self.PointDrawn:
            self.DrawShape()
        else:
            self.DragAsBox()

    def UpdateCenterPoint(self):
        self.DragShape()
        
