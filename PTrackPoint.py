from PFunc import *
import PPoint

import math

# Constants for point and signal sizes
SIGSIZE=10
POINTSIZE=10

class PTrackPoint(PPoint.PPoint):
    def __init__(self, master, coord, number, tokens=None):
        PPoint.PPoint.__init__(self, master, coord, number)

        self.Type='PTrackPoint'
        self.DrawShape=self.DrawTrackPoint
        self.DragShape=self.DragTrackPoint
        self.UpdateShape=self.UpdateTrackPoint
        self.DrawShape()
        #self.SetMode()

    def IsStubEnd(self):
        owners=self.Owners.keys()

        if len(owners) == 1:
            owner=self.Owners[owners[0]]
            isend=owner.IsPointEnd(self)
            if isend in (0, 1) and owner.Owner!=None:
                nextobj, nextend = owner.Owner.NextObject(isend, owner)
                if nextobj==None:
                    return 1 # Point is a stub end
                else:
                    return 0 # More track can be added at the point
            else:
                return 3 # Point is in the middle of a piece of track
        elif len(owners) == 2:
            isend=self.Owners[owners[0]].IsPointEnd(self)
            if isend == -1:
                return 3
            line0=self.Owners[owners[0]]
            line1=self.Owners[owners[1]]
            if line0.Owner==line1.Owner and line0.Owner!=None:
                nextobj, nextend = line0.Owner.NextObject(0, line0)
                if nextobj==None:
                    return 1 # Point is a switch point which cannot be extended
                else:
                    return 0 # More track can be added at the point
        return 2 # The point is fully built out

    def DrawTrackPoint(self):
        self.Undraw()
        self.IsEnd=self.IsStubEnd()

        if self.PM.Mode=='Edit':
            if self.IsEnd==0:
                self.DrawAsBox()
                self.DrawArrow()
            elif self.IsEnd==1:
                self.DrawAsX()
            elif self.IsEnd==2:
                self.DrawAsBox()
            else:
                self.DrawAsBox()
                self.SetBoxColors(fill='Grey', outline='Grey')
            self.PointDrawn=True
        elif self.PM.Mode=='Run':
            if self.IsEnd==0:
                self.DrawArrow()
            elif self.IsEnd==1:
                self.DrawAsX()
            self.DrawSignals()
            self.PointDrawn=True

    def DragTrackPoint(self):
        if self.PM.Scale<self.PM.MinPointScale and self.PointDrawn:
            self.Undraw()
        elif self.PM.Scale>=self.PM.MinPointScale and not self.PointDrawn:
            self.DrawShape()
        else:
            if self.IsEnd==0:
                self.DragAsBox()
                self.DragArrow()
            elif self.IsEnd==1:
                self.DragAsX()
            else:
                self.DragAsBox()
            self.DragSignals()

    def UpdateTrackPoint(self):
        isend=self.IsStubEnd()

        if isend!=self.IsEnd:
            self.IsEnd=isend
            self.DrawTrackPoint()
        else:
            if self.PM.Mode=='Edit':
                self.DragShape()
            elif self.PM.Mode=='Run':
                self.DragSignals()

    def DragSignals(self):
        sigsize=7*self.PM.Scale
        dcoord=self.TellDCoord()
        bbox=(dcoord[0]-sigsize, dcoord[1]-sigsize, dcoord[0]+sigsize, dcoord[1]+sigsize)

        self.cv.coords(self.Name+'Signal0', bbox)
        self.cv.coords(self.Name+'Signal1', bbox)

    def UpdateSignals(self):
        if self.IsGap():
            ownernames=self.Owners.keys()
            if len(ownernames)==2:
                end0=self.Owners[ownernames[0]].TrueEnd(self)
                color0=self.Owners[ownernames[0]].SignalColor(end0)
                end1=self.Owners[ownernames[1]].TrueEnd(self)
                color1=self.Owners[ownernames[1]].SignalColor(end1)

                self.cv.itemconfig(self.Name+'Signal0', fill=color0)
                self.cv.itemconfig(self.Name+'Signal1', fill=color1)

    def DrawSignals(self):
##        self.cv.delete((self.Name+'Signal0', self.Name+'Signal1'))
        if self.IsGap():
            ownernames=self.Owners.keys()
            ownernames.sort()
            if len(ownernames)==2:
                angle0 = self.Owners[ownernames[0]].TellAngle(self)
                angle1 = self.Owners[ownernames[1]].TellAngle(self)

                angle0 = angle0[0]*180/math.pi
                angle1 = angle1[0]*180/math.pi

                avgangle = (angle0+angle1)/2.0
                oppangle = avgangle + 180.0

                name0 = self.Owners[ownernames[0]].Owner.Name
                name1 = self.Owners[ownernames[1]].Owner.Name

                end0=self.Owners[ownernames[0]].IsPointEnd(self)
                color0=self.Owners[ownernames[0]].SignalColor(end0)
                end1=self.Owners[ownernames[1]].IsPointEnd(self)
                color1=self.Owners[ownernames[1]].SignalColor(end1)

                trueEnd0=self.Owners[ownernames[0]].TrueEnd(self)
                trueEnd1=self.Owners[ownernames[1]].TrueEnd(self)

                sigsize=7*self.PM.Scale
                dcoord=self.TellDCoord()
                bbox=(dcoord[0]-sigsize, dcoord[1]-sigsize, dcoord[0]+sigsize, dcoord[1]+sigsize)

                if avgangle<angle0<=oppangle:
                    ang0=avgangle
                    ang1=oppangle
                else:
                    ang0=oppangle
                    ang1=avgangle

                # Angles are negative due to different positive angle directions for
                # natural Tk canvas coordinate system (positive clockwise)
                # and create_arc command (positive counter-clockwise)
                self.cv.create_arc(bbox, start=-ang0, extent=-180, fill=color0, tags=(self.Name, self.Name+'Signal0',name0+'Signal'+str(trueEnd0), 'Signal'))
                self.cv.create_arc(bbox, start=-ang1, extent=-180, fill=color1, tags=(self.Name, self.Name+'Signal1',name1+'Signal'+str(trueEnd1), 'Signal'))

    def IsGap(self):
        owners=self.Owners.keys()
        if len(owners)>0:
            end=self.Owners[owners[0]].IsPointEnd(self)
            if end in (0, 1):
                return self.Owners[owners[0]].IsGap(end)
        else:
            return False

    def GetCoordsAsX(self):
        owners=self.Owners.keys()
        if len(owners)==1:
            angle=self.Owners[owners[0]].TellAngle(self)
            if len(angle)==2:
                angle=(angle[0]+angle[1])/2.0+math.pi/2
            else:
                angle=angle[0]
        else:
            angle=0.0
        coords=[(5, 10), (-5, -10), (-5, 10), (5, -10)]
        for i in range(4):
            coords[i]=RotateCoord(coords[i], -angle)
            coords[i]=(coords[i][0]+self.coord[0], coords[i][1]+self.coord[1])
            temp, coords[i]=self.PM.TrueCoord(self.Number, 'label', coords[i])
        return coords

    def SetSelected(self, select=False, fill='White', outline='Red'):
        if select==True:
            self.SetBoxColors(fill=fill, outline=outline)
            self.Selected=True
        else:
            if self.IsEnd in (0, 1, 2):
                self.SetBoxColors(fill='White', outline='Red')
            else:
                self.SetBoxColors(fill='Grey', outline='Grey')

            self.Selected=False

    def DrawAsX(self):
        self.Undraw()

        coords=self.GetCoordsAsX()
        self.cv.create_line((coords[0], coords[1]), width=3*self.PM.Scale, fill='Red', tags=(self.Name, self.Name+'Point', self.Name+'L0', 'Point'))
        self.cv.create_line((coords[2], coords[3]), width=3*self.PM.Scale, fill='Red', tags=(self.Name, self.Name+'Point', self.Name+'L1', 'Point'))

    def DragAsX(self):
        coords=self.GetCoordsAsX()
        self.cv.coords(self.Name+'L0', coords[0]+coords[1])
        self.cv.coords(self.Name+'L1', coords[2]+coords[3])
        self.cv.itemconfig(self.Name+'L0', width=3*self.PM.Scale)
        self.cv.itemconfig(self.Name+'L1', width=3*self.PM.Scale)

    def GetCoordsArrow(self):
        owners=self.Owners.keys()
        angle=0.0
        angles=[]
        for owner in owners:
            angles+=self.Owners[owner].TellAngle(self)
        for ang in angles:
            angle+=ang
        angle=angle/len(owners)
            
        coords=[(10, 0), (50, 0)]

        for i in range(2):
            coords[i]=RotateCoord(coords[i], -angle)
            coords[i]=(coords[i][0]+self.TellCoord()[0], coords[i][1]+self.TellCoord()[1])
            temp, coords[i]=self.PM.TrueCoord(self.Number, 'label', coords[i])
        return coords

    def DrawArrow(self):
        self.UndrawArrow()
        coords=self.GetCoordsArrow()
        arrowhead=(8*self.PM.Scale, 10*self.PM.Scale, 3*self.PM.Scale)
        self.cv.create_line(coords[0]+coords[1], width=3*self.PM.Scale, arrowshape=arrowhead, fill='Yellow', arrow='last', tags=(self.Name, self.Name+'Arrow', 'Arrow'))
        self.cv.tag_bind(self.Name+'Arrow', '<Button-1>', lambda x: self.ArrowClick(x, True))
        self.cv.tag_bind(self.Name+'Arrow', '<Button-3>', lambda x: self.ArrowClick(x, False))

    def UndrawArrow(self):
        self.cv.delete(self.Name+'Arrow')

    def DragArrow(self):
        coords=self.GetCoordsArrow()
        arrowhead=(8*self.PM.Scale, 10*self.PM.Scale, 3*self.PM.Scale)
        self.cv.itemconfig(self.Name+'Arrow', arrowshape=arrowhead, width=3*self.PM.Scale)
        self.cv.coords(self.Name+'Arrow', coords[0]+coords[1])

    def ArrowClick(self, event, connect):
        if self.PM.Clickable:
            if self.PM.Mode=='Run':
                pass
            elif self.PM.Mode=='Edit':
                self.ExtendLayout(event, connect)

    def ExtendLayout(self, event=None, connect=True):
        owners=self.Owners.keys()
        owner=self.Owners[owners[0]]
        nextobj, nextend = owner.Owner.NextObject(owner.IsPointEnd(self), owner)
        self.PM.ExtendLayout(nextobj, nextend, self, connect)
