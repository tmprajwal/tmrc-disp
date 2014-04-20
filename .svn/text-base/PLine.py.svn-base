from PFunc import *
from math import floor

class PLine:
    def __init__(self, master, number):
        self.Type='PLine'
        self.Category='line'
        self.PM=master
        self.cv=self.PM.cv
        self.PPoints=[]
        self.Number=number
        self.Name='Line'+str(self.Number)
        self.Drawn=False
        self.LabelDrawn=False
        self.Labeled=True
        self.Arrow=None
        self.SetArrowShape()
        self.Basewidth=4
        self.DrawnWidth=4
        self.LabelPos=0.5
        self.LabelCoord=(0,0)
        self.LabelText=self.Name

        self.TotalLength=0
        self.Length=0
        self.Frac=0

    def LineLength(self):
        segs=len(self.PPoints)-1
        length=[0]*segs
        frac=[0]*segs
        totallength=0
        for i in range(segs):
            length[i]=PointDistance(self.PPoints[i].TellCoord(), self.PPoints[i+1].TellCoord())
            totallength+=length[i]
        if totallength!=0:
            for i in range(segs):
                frac[i]=length[i]/totallength
        else:
            for i in range(segs):
                frac[i]=1

        self.TotalLength=totallength
        self.Length=length
        self.Frac=frac

    def LinePos(self, frac):
        totfrac=0
        i=0
        if frac==1.0:
            return self.PPoints[-1].TellCoord()
        while totfrac<frac:
            totfrac+=self.Frac[i]
            i+=1
        prevfrac=totfrac-self.Frac[i-1]
        nextfrac=totfrac
        prevcoord=self.PPoints[i-1].TellCoord()
        nextcoord=self.PPoints[i].TellCoord()
        if frac==prevfrac:
            return prevcoord
        else:
            partial=(frac-prevfrac)/(nextfrac-prevfrac)
            newx=prevcoord[0]+(nextcoord[0]-prevcoord[0])*partial
            newy=prevcoord[1]+(nextcoord[1]-prevcoord[1])*partial
            return (newx, newy)

    def LineFrac(self, segment, coord):
        frac=0
        for i in range(segment):
            frac+=self.Frac[i]
        coord0=self.PPoints[segment].TellCoord()
        coord1=self.PPoints[segment+1].TellCoord()
        between=IsInBetween(coord0, coord1, coord)

        if between:
            partial=PointDistance(coord, self.PPoints[segment].TellCoord())
            return frac+partial/self.TotalLength
        else:
            return -1

    def LabelStatus(self, draw):
        if draw==True and self.Labeled==False:
            self.Labeled=True
            self.DrawLabel()
        if draw==False and self.Labeled==True:
            self.Labeled=False
            self.UndrawLabel()

    def Bind(self):
        self.cv.tag_bind(self.Name+'Label', '<B1-Motion>', self.DragLabel)
        self.cv.tag_bind(self.Name+'Line', '<Button-1>', self.AddPoint)

    def DrawLabel(self):
        self.UndrawLabel()
        if self.Labeled:
            self.LabelCoord, dcoord = self.PM.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
            self.cv.create_text(dcoord, text=self.LabelText, tags=(self.Name, 'LineLabel', self.Name+'Label', self.Name+'LabelText'), fill=RandomColor())
            self.Bind()
            self.LabelDrawn=True
    
    def UndrawLabel(self):
        self.cv.delete(self.Name+'Label', self.Name+'Label')
        self.LabelDrawn=False

    def TellLabelPos(self):
        return self.LabelPos

    def TellLabelDCoord(self):
        labelcoord, dcoord = self.PM.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
        return dcoord

    def SetLabelPos(self, labelpos):
        self.LabelPos=labelpos
        self.UpdateLabel()

    def UpdateLabel(self):
        if self.Drawn and self.Labeled:
            coord, dcoord = self.PM.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
            self.cv.coords(self.Name+'Label', dcoord)

    def SetLabelText(self, text):
        if self.LabelText!=text:
            self.LabelText=text
            if self.Drawn and self.Labeled:
                self.cv.itemconfig(self.Name+'LabelText', text=text)
                self.UpdateLabel()

    def DragLabel(self, event):
        minindex, intcoord = self.NearestSegment('dlabel', (self.cv.canvasx(event.x), self.cv.canvasy(event.y)))
        newLabelPos=self.LineFrac(minindex, intcoord)
        if newLabelPos!=-1:
            self.LabelPos=newLabelPos
            self.UpdateLabel()
    
    def UpdatePoints(self, point=None):
        """Update stuff after inserting or deleting point.

        This function will be called after inserting or deleting
        points to update coordinates, recheck slopes, etc."""
        if len(self.PPoints)<2:
            if self.Drawn==True:
                self.cv.delete(self.Name)
                self.Drawn=False
            self.TotalLength=0
            self.Length=0
            self.Frac=0
        else:
            coords=[]
            self.LineLength()
            if self.Drawn==False:
                self.SetArrowShape()
                self.cv.create_line([0,0,0,0], tags=(self.Name, 'Line', self.Name+'Line'),
                                    fill=RandomColor(), smooth=0, arrow=self.Arrow,
                                    arrowshape=self.ArrowShape)
                self.DrawLabel()
                self.Bind()
                self.Drawn=True
            self.UpdateScale()
            for point in self.PPoints:
                point.UpdateShape()

    def CorrectCoords(self, coords):
        """Correct the display coordinates passed in such that lines that should be 45deg
        but aren't quite because of a rounding error end up actually 45deg. This makes
        the display not have random line width changes.

        Takes a list of x,y pairs and returns a list of x,y pairs
        """
        last_horiz = True
        last_vert = True
        out = []
        for (x,y), (nextx, nexty) in zip(coords, coords[1:]):
            xdiff = nextx - x
            ydiff = nexty - y

            diffdiff = abs(xdiff) - abs(ydiff)
            if 0 < abs(diffdiff) <= 2 and xdiff != 0 and ydiff != 0:
                # Almost a 45 degree angle, but not quite
                
                #print "correcting", self.Name, (x,y), (nextx,nexty), "to",
                if last_vert and last_horiz and diffdiff in (-2, 2):
                    x -= diffdiff/2 * (xdiff > 0 and -1 or 1)
                    y += diffdiff/2 * (ydiff > 0 and -1 or 1)
                elif last_horiz:
                    x -= diffdiff * (xdiff > 0 and -1 or 1)
                elif last_vert:
                    y += diffdiff * (ydiff > 0 and -1 or 1)
                #print (x,y), (nextx,nexty)
            out.append((x,y))
            last_vert = xdiff == 0
            last_horiz = ydiff == 0
        # add the final point (which we never adjust)
        out.append((nextx,nexty))
        return out
                
    def UpdateScale(self):
        """Update display after scale change."""
        if self.Drawn==True:
            coords = self.CorrectCoords([point.TellDCoord() for point in self.PPoints])
            flatcoords = []
            for coord in coords:
                flatcoords += coord
            
            self.cv.coords(self.Name+'Line', *flatcoords)
            newwidth=max(floor(self.PM.Scale*self.Basewidth), 1)
            if self.Arrow!=None:
                self.DrawnWidth=newwidth
                self.SetArrowShape()
                self.cv.itemconfig(self.Name+'Line', width=self.DrawnWidth, arrowshape=self.ArrowShape)
            elif newwidth!=self.DrawnWidth:
                self.DrawnWidth=newwidth
                self.cv.itemconfig(self.Name+'Line', width=self.DrawnWidth)
            self.UpdateLabel()

    def SetArrowShape(self):
        self.ArrowShape=(30*self.PM.Scale, 30*self.PM.Scale, 6*self.PM.Scale)

    def UpdateArrow(self, arrow=None):
        if arrow!=self.Arrow:
            self.Arrow=arrow
            self.SetArrowShape()
            self.cv.itemconfig(self.Name+'Line', arrow=self.Arrow, arrowshape=self.ArrowShape)

    def InsertPoint(self, point, index=None, hold=False):
        """Add or insert point to SpLine.

        This creates a new point in the SpLine at the specified coordinates.
        Coord should be a tuple or list with two elements.  If index is
        specified, the new point is inserted into the point list at that
        index, otherwise it is added to the end of the list."""
        if index==None:
            self.PPoints+=[point]
        else:
            index=int(index)
            self.PPoints=self.PPoints[:index]+ \
                          [point]+ \
                          self.PPoints[index:]
        point.AddOwner(self)
        if hold==False:
            self.UpdatePoints(point)

    def NearestSegment(self, pointtype, coord):
        mindist=2147482647
        minindex=None
        coord, dcoord=self.PM.TrueCoord(-1, pointtype, coord)
        coord1=self.PPoints[0].TellCoord()
        for i in range(len(self.PPoints)-1):
            coord0=coord1
            coord1=self.PPoints[i+1].TellCoord()
            segdist, segintcoord=LineDistance(coord0, coord1, coord)
            if 0<=segdist<mindist:
                mindist=segdist
                minintcoord=segintcoord
                minindex=i
        if minindex!=None:
            return minindex, minintcoord
        else:
            return -1, (0, 0)

    def AddPoint(self, event):
        minindex, intcoord=self.NearestSegment('dcoord', (self.cv.canvasx(event.x), self.cv.canvasy(event.y)))
        self.PM.AddPointToLine(intcoord, self, minindex+1)

    def TellPointList(self):
        return self.PPoints[:]

    def DeletePoint(self, point):
        """Delete a point from a PLine.

        This function will delete the point at the specified index from
        the PLine object.  If index is not specified, the last point
        in the list will be deleted."""
        index=self.PPoints.index(point)
        del self.PPoints[index]
        self.UpdatePoints(point)

    def IsPointEnd(self, point):
        index=self.PPoints.index(point)
        if index==0:
            return 0
        elif index==len(self.PPoints)-1:
            return 1
        else:
            return -1

    def TellEndPoint(self, end):
        if end==0:
            return self.PPoints[0]
        else:
            num=len(self.PPoints)-1
            return self.PPoints[num]

    def TellPoints(self):
        return self.PPoints

    def TellAngle(self, point):
        """Return the angle of the specified node.

        Returns the angle of the line at the specified point.  If it is the end
        it returns the angle of that end (0 is pointing right).  If it is a
        midline node, returns the angles of the two adjacent lines.
        Values are in radians, and are positive in the clockwise direction as
        the y-axis points down."""
        index=self.PPoints.index(point)
        if len(self.PPoints)<2:
            angle=(0.0,)
        elif index==0:
            p0coord=self.PPoints[0].TellCoord()
            p1coord=self.PPoints[1].TellCoord()
            angle=(math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0]),)
            if angle < 0:
                angle += math.pi
        elif index==len(self.PPoints)-1:
            p0coord=self.PPoints[index].TellCoord()
            p1coord=self.PPoints[index-1].TellCoord()
            angle=(math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0]),)
            if angle < 0:
                angle += math.pi
        else:
            p0coord=self.PPoints[index].TellCoord()
            p1coord=self.PPoints[index-1].TellCoord()
            angle0=math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0])
            if angle0 < 0:
                angle0 += math.pi
            p0coord=self.PPoints[index].TellCoord()
            p1coord=self.PPoints[index+1].TellCoord()
            angle1=math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0])
            if angle1 < 0:
                angle1 += math.pi
            angle=(angle0, angle1)
        return angle

