from Tkinter import *
import math
import random

class PLineManager:
    def __init__(self, cv, mode='demo'):
        self.cv=cv

        self.pointnum=0
        self.linenum=0
        self.arrownum=0
        self.points={}
        self.lines={}
        self.arrows={}

        self.Scale=1
        self.SnapInc=20

        if mode=='demo':
            self.AddLine()
            self.AddPointToLine((50, 50), 0, None)
            self.AddPointToLine((200, 50), 0, None)

    def AddLine(self):
        self.lines[self.linenum]=PLine(self, self.linenum)
        self.linenum+=1

    def DeleteLine(self, linenum):
        pass

    def ChangeScale(self, ratio):
        self.Scale*=ratio
        points=self.points.keys()
        for point in points:
            self.points[point].ScalePoint(self.Scale)
        lines=self.lines.keys()
        for line in lines:
            self.lines[line].UpdateScale(self.Scale)

    def AddPointToLine(self, coord, line, index=None):
        self.points[self.pointnum]=PPoint(self, coord, self.pointnum)
        self.points[self.pointnum].AddOwner(self.lines[line])
        self.lines[line].InsertPoint(self.points[self.pointnum], self.pointnum, index)
        self.pointnum+=1

    def DeletePoint(self, pointnum):
        owners=self.points[pointnum].TellOwners()
        if len(owners.keys())>1:
            print 'Cannot delete shared point', pointnum
        elif len(owners[owners.keys()[0]].TellPointList())<=2:
            print 'Deleting point', pointnum, 'will leave line lonely'
        else:
            owners[owners.keys()[0]].DeletePoint(pointnum)
            self.points[pointnum].Undraw()
            del self.points[pointnum]

    def TrueCoord(self, pointnum, type, coord):
        if type in ('dcoord', 'dlabel'):
            coord=(coord[0]/float(self.Scale), coord[1]/float(self.Scale))
        if self.SnapInc!=0 and type not in ('label', 'dlabel'):
            Snap=int(self.SnapInc)
            coord=(int(Snap*math.floor(float(coord[0])/Snap+0.5)), int(Snap*math.floor(float(coord[1])/Snap+0.5)))
            dcoord=(int(Snap*math.floor(float(coord[0])/Snap+0.5)*self.Scale), int(Snap*math.floor(float(coord[1])/Snap+0.5)*self.Scale))
        else:
            coord=coord
            dcoord=(coord[0]*self.Scale, coord[1]*self.Scale)
        return coord, dcoord

    def GetCoordsArrow(self):
        point0=self.PPoints[self.PPointList[0]]
        point1=self.PPoints[self.PPointList[len(self.PPointList)-1]]

        angle0=self.TellAngle(self.PPointList[0])[0]
        angle1=self.TellAngle(self.PPointList[len(self.PPointList)-1])[0]
        
        coords=[(10, 0), (50, 0), (35, 5), (35, -5)]
        coords0=[(0, 0), (0, 0), (0, 0), (0, 0)]
        coords1=[(0, 0), (0, 0), (0, 0), (0, 0)]

        for i in range(4):
            coords0[i]=RotateCoord(coords[i], -angle0)
            coords0[i]=(coords0[i][0]+point0.TellCoord()[0], coords0[i][1]+point0.TellCoord()[1])
            coords1[i]=RotateCoord(coords[i], -angle1)
            coords1[i]=(coords1[i][0]+point1.TellCoord()[0], coords1[i][1]+point1.TellCoord()[1])

        return coords0, coords1

    def DrawArrow(self, arrownum):
        ownercount0=self.PPoints[self.PPointList[0]].TellOwners()
        ownercount1=self.PPoints[self.PPointList[len(self.PPointList)-1]].TellOwners()
#        if ownercount
        coords0, coords1=self.GetCoordsArrow()
        self.master.cv.create_line((coords0[0], coords0[1]), width=3, fill='Yellow', tags=(self.name, 'Line', self.name+'AL0'))
        self.master.cv.create_line((coords0[2], coords0[1], coords0[3]), width=3, fill='Yellow', tags=(self.name, 'Line', self.name+'AH0'))
        self.master.cv.create_line((coords1[0], coords1[1]), width=3, fill='Yellow', tags=(self.name, 'Line', self.name+'AL1'))
        self.master.cv.create_line((coords1[2], coords1[1], coords1[3]), width=3, fill='Yellow', tags=(self.name, 'Line', self.name+'AH1'))

    def DragArrows(self):
        coords0, coords1=self.GetCoordsArrow()
        self.master.cv.coords(self.name+'AH0', coords0[0]+coords0[1])
        self.master.cv.coords(self.name+'AL0', coords0[2]+coords0[1]+coords0[3])
        self.master.cv.coords(self.name+'AH1', coords1[0]+coords1[1])
        self.master.cv.coords(self.name+'AL1', coords1[2]+coords1[1]+coords1[3])

class PLine:
    def __init__(self, master, number):
        self.master=master
        self.PPoints={}
        self.PPointList=[]
        self.number=number
        self.name='Line'+str(self.number)
        self.drawn=False
        self.basewidth=4
        self.LabelPos=0.5
        self.LabelCoord=(0,0)

        self.TotalLength=0
        self.Length=0
        self.Frac=0

    def LineLength(self):
        segs=len(self.PPointList)-1
        length=[0]*segs
        frac=[0]*segs
        totallength=0
        for i in range(segs):
            length[i]=PointDistance(self.PPoints[self.PPointList[i]].TellCoord(), self.PPoints[self.PPointList[i+1]].TellCoord())
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
            return self.PPoints[self.PPointList[len(self.PPointList)-1]].TellCoord()
        while totfrac<frac:
            totfrac+=self.Frac[i]
            i+=1
        prevfrac=totfrac-self.Frac[i-1]
        nextfrac=totfrac
        prevcoord=self.PPoints[self.PPointList[i-1]].TellCoord()
        nextcoord=self.PPoints[self.PPointList[i]].TellCoord()
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
        coord0=self.PPoints[self.PPointList[segment]].TellCoord()
        coord1=self.PPoints[self.PPointList[segment+1]].TellCoord()
        between=IsInBetween(coord0, coord1, coord)

        if between:
            partial=PointDistance(coord, self.PPoints[self.PPointList[segment]].TellCoord())
            return frac+partial/self.TotalLength
        else:
            return -1

    def DrawLabel(self):
        self.LabelCoord, dcoord = self.master.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
        self.master.cv.create_text(dcoord, text=self.name, tags=(self.name, 'LineLabel', self.name+'Label'), fill=RandomColor())
        self.master.cv.tag_bind(self.name+'Label', '<B1-Motion>', self.DragLabel)
    
    def UpdateLabel(self):
        coord, dcoord = self.master.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
        self.master.cv.coords(self.name+'Label', dcoord)

    def DragLabel(self, event):
        minindex, intcoord = self.NearestSegment('dlabel', (event.x, event.y))
        newLabelPos=self.LineFrac(minindex, intcoord)
        if newLabelPos!=-1:
            self.LabelPos=newLabelPos
            self.UpdateLabel()
    
    def UpdatePoints(self, pointnum):
        """Update stuff after inserting or deleting point.

        This function will be called after inserting or deleting
        points to update coordinates, recheck slopes, etc."""
        if len(self.PPoints)<2:
            print 'Too few points to show line', self.number
            if self.drawn==True:
                self.master.cv.delete(self.name)
                self.drawn=False
            self.TotalLength=0
            self.Length=0
            self.Frac=0
        else:
            coords=[]
            self.LineLength()
            for point in range(0, len(self.PPoints)):
                coords+=self.PPoints[self.PPointList[point]].TellDCoord()
            if self.drawn==False:
                self.master.cv.create_line(coords, tags=(self.name, 'Line', self.name+'Line'), fill=RandomColor(), width=self.basewidth, smooth=0)
                self.master.cv.tag_bind(self.name+'Line', '<Button-1>', self.AddPoint)
                self.DrawLabel()
                self.drawn=True
            else:
                self.master.cv.coords(self.name+'Line', *coords)
                self.UpdateLabel()
            for point in range(0, len(self.PPoints)):
                self.PPoints[self.PPointList[point]].UpdateShape()

    def UpdateScale(self, scale):
        """Update display after scale change."""
        if self.drawn==True:
            coords=[]
            for point in range(0, len(self.PPoints)):
                coords+=self.PPoints[self.PPointList[point]].TellDCoord()
            self.master.cv.coords(self.name+'Line', *coords)
            self.master.cv.itemconfig(self.name+'Line', width=scale*self.basewidth)
            self.UpdateLabel()

    def InsertPoint(self, point, pointnumber, index=None):
        """Add or insert point to SpLine.

        This creates a new point in the SpLine at the specified coordinates.
        Coord should be a tuple or list with two elements.  If index is
        specified, the new point is inserted into the point list at that
        index, otherwise it is added to the end of the list."""
        self.PPoints[pointnumber]=point
        if index==None:
            self.PPointList+=[pointnumber]
        else:
            index=int(index)
            self.PPointList=self.PPointList[:index]+ \
                          [pointnumber]+ \
                          self.PPointList[index:]
        self.UpdatePoints(pointnumber)

    def NearestSegment(self, pointtype, coord):
        mindist=2147482647
        minindex=None
        coord, dcoord=self.master.TrueCoord(-1, pointtype, coord)
        coord1=self.PPoints[self.PPointList[0]].TellCoord()
        for i in range(len(self.PPointList)-1):
            coord0=coord1
            coord1=self.PPoints[self.PPointList[i+1]].TellCoord()
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
        minindex, intcoord=self.NearestSegment('dcoord', (event.x, event.y))
        self.master.AddPointToLine((event.x, event.y), self.number, minindex+1)

    def TellPointList(self):
        return self.PPointList

    def DeletePoint(self, pointnum):
        """Delete a point from a PLine.

        This function will delete the point at the specified index from
        the PLine object.  If index is not specified, the last point
        in the list will be deleted."""
        index=self.PPointList.index(pointnum)
        self.PPointList=self.PPointList[:index]+self.PPointList[index+1:]
        del self.PPoints[pointnum]
        self.UpdatePoints(pointnum)

    def IsPointEnd(self, pointnum):
        index=self.PPointList.insdex(pointnum)
        if index==0:
            return 0
        elif index==len(self.PPointList)-1:
            return 1
        else:
            return -1

    def TellAngle(self, pointnum):
        """Return the angle of the specified node.

        Returns the angle of the line at the specified point.  If it is the end
        it returns the angle of that end (0 is pointing right).  If it is a
        midline node, returns the angles of the two adjacent lines.
        Values are in radians, and are positive in the clockwise direction as
        the y-axis points down."""
        index=self.PPointList.index(pointnum)
        if len(self.PPoints)<2:
            angle=(0.0,)
        elif index==0:
            p0coord=self.PPoints[self.PPointList[0]].TellCoord()
            p1coord=self.PPoints[self.PPointList[1]].TellCoord()
            angle=(math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0]),)
        elif index==len(self.PPoints)-1:
            p0coord=self.PPoints[self.PPointList[index]].TellCoord()
            p1coord=self.PPoints[self.PPointList[index-1]].TellCoord()
            angle=(math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0]),)
        else:
            p0coord=self.PPoints[self.PPointList[index]].TellCoord()
            p1coord=self.PPoints[self.PPointList[index-1]].TellCoord()
            angle0=math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0])
            p0coord=self.PPoints[self.PPointList[index]].TellCoord()
            p1coord=self.PPoints[self.PPointList[index+1]].TellCoord()
            angle1=math.atan2(p0coord[1]-p1coord[1], p0coord[0]-p1coord[0])
            angle=(angle0, angle1)
        return angle

class PPoint:
    def __init__(self, master, coord, number):
        self.master=master
        self.number=number

        self.name='Point'+str(number)
                
        self.owners={}
        self.DrawShape=self.DrawAsBox
        
        self.DrawPoint(coord)

    def DrawPoint(self, coord):
        self.coord, self.dcoord=self.master.TrueCoord(self.number, 'coord', coord)
        self.DrawShape()
        self.DefineBindings()

    def ChangeStyle(self, newstyle):
        if newstyle=='X':
            self.DrawAsX()
        else:
            self.DrawAsBox()

    def DefineBindings(self):
        self.master.cv.tag_bind(self.name, '<B1-Motion>', self.DragPoint)
        self.master.cv.tag_bind(self.name, '<Button-1>', self.Pass)
        self.master.cv.tag_bind(self.name, '<Button-3>', lambda x:self.master.DeletePoint(self.number))

    def GetCoordsAsX(self):
        owners=self.owners.keys()
        if len(owners)==1:
            angle=self.owners[owners[0]].TellAngle(self.number)
            if len(angle)==2:
                angle=(angle[0]+angle[1])/2.0+math.pi/2
            else:
                angle=angle[0]
        else:
            angle=0.0
        coords=[(5, 10), (-5, -10), (-5, 10), (5, -10)]
        for i in range(4):
            coords[i]=RotateCoord(coords[i], -angle)
            coords[i]=(coords[i][0]+self.dcoord[0], coords[i][1]+self.dcoord[1])
        return coords

    def DrawAsX(self):
        self.Undraw()
        self.DrawShape=self.DrawAsX
        self.DragShape=self.DragAsX
        self.UpdateShape=self.DragAsX

        coords=self.GetCoordsAsX()
        self.master.cv.create_line((coords[0], coords[1]), width=3, fill='Blue', tags=(self.name, self.name+'L0', 'Point'))
        self.master.cv.create_line((coords[2], coords[3]), width=3, fill='Blue', tags=(self.name, self.name+'L1', 'Point'))

    def DragAsX(self):
        coords=self.GetCoordsAsX()
        self.master.cv.coords(self.name+'L0', coords[0]+coords[1])
        self.master.cv.coords(self.name+'L1', coords[2]+coords[3])

    def GetCoordsAsBox(self):
        return (self.dcoord[0]-5, self.dcoord[1]-5, self.dcoord[0]+5, self.dcoord[1]+5)

    def DrawAsBox(self):
        self.Undraw()
        self.DrawShape=self.DrawAsBox
        self.DragShape=self.DragAsBox
        self.UpdateShape=self.DragAsBox

        coords=self.GetCoordsAsBox()
        self.master.cv.create_rectangle(coords, tags=(self.name, 'Point'), outline='Red', fill='White')

    def DragAsBox(self):
        coords=self.GetCoordsAsBox()
        self.master.cv.coords(self.name, coords)

    def UpdateBox(self):
        pass

    def ScalePoint(self, scale):
        self.coord, self.dcoord=self.master.TrueCoord(self.number, 'coord', self.coord)
        self.DragShape()

    def DragPoint(self, event=None):
        if event!=None:
            self.coord, self.dcoord=self.master.TrueCoord(self.number, 'dcoord', (event.x, event.y))
        else:
            self.coord, self.dcoord=self.master.TrueCoord(self.number, 'coord', self.coord)
        self.DragShape()
        for key in self.owners.keys():
            self.owners[key].UpdatePoints(self.number)

    def Undraw(self):
        self.master.cv.delete(self.name)

    def TellCoord(self):
        return self.coord

    def TellDCoord(self):
        return self.dcoord

    def AddOwner(self, newowner):
        self.owners[newowner.number]=newowner

    def DelOwner(self, name):
        del self.owners[name]

    def TellOwners(self):
        return self.owners

    def Pass(self, event=None):
        pass

def RandomColor():
    R=random.random()
    G=random.random()
    B=random.random()
    tk_rgb = "#%02x%02x%02x" % (255*R/2+128, 255*G/2+128, 255*B/2+128)
    return tk_rgb

def RotateCoord(coord, angle):
    newx=coord[0]*math.cos(angle) + coord[1]*math.sin(angle)
    newy=-coord[0]*math.sin(angle) + coord[1]*math.cos(angle)
    return (newx, newy)

def PointDistance(coord0, coord1):
    return math.sqrt((coord0[0]-coord1[0])**2+(coord0[1]-coord1[1])**2)

def LineDistance(coord0, coord1, coorde):
    if coord1[0]==coord0[0]:
        if coord1[1]<coord0[1]:
            coordlow=coord1[1]
            coordhigh=coord0[1]
        elif coord0[1]<coord1[1]:
            coordlow=coord0[1]
            coordhigh=coord1[1]
        else:
            coordlow=coordhigh=coord0[1]
            
        if coorde[1]<coordlow or coorde[1]>coordhigh:
            dist=-1
        else:
            dist=abs(coorde[0]-coord0[0])
        xint=coord0[0]
        yint=coorde[1]

    elif coord1[1]==coord0[1]:
        if coord1[0]<coord0[0]:
            coordlow=coord1[0]
            coordhigh=coord0[0]
        elif coord0[0]<coord1[0]:
            coordlow=coord0[0]
            coordhigh=coord1[0]
        else:
            coordlow=coordhigh=coord0[0]

        if coorde[0]<coordlow or coorde[0]>coordhigh:
            dist=-1
        else:
            dist=abs(coorde[1]-coord0[1])
        xint=coorde[0]
        yint=coord0[1]

    else:
        m=float(coord1[1]-coord0[1])/(coord1[0]-coord0[0])
        b=coord0[1]-m*coord0[0]
        me=-1.0/m
        be=coorde[1]-me*coorde[0]
        xint=(be-b)/(m-me)
        yint=m*xint+b

        between=IsInBetween(coord0, coord1, (xint, yint))

        if between:
            dist=math.sqrt((coorde[0]-xint)**2 + (coorde[1]-yint)**2)
        else:
            dist=-1

    return dist, (xint, yint)

def IsInBetween(coord0, coord1, coord2):
    if coord1[0]<coord0[0]:
        coordxlow=coord1[0]
        coordxhigh=coord0[0]
    else:
        coordxlow=coord0[0]
        coordxhigh=coord1[0]

    if coord1[1]<coord0[1]:
        coordylow=coord1[1]
        coordyhigh=coord0[1]
    else:
        coordylow=coord0[1]
        coordyhigh=coord1[1]

    if coordxlow<=coord2[0]<=coordxhigh and coordylow<=coord2[1]<=coordyhigh:
        return True
    else:
        return False

if __name__=='__main__':
    root=Tk()
    cv=Canvas(root, bg='Black')
    cv.pack(side=TOP, fill=BOTH, expand=1)
    pm=PLineManager(cv)
    root.bind('a', lambda x: pm.ChangeScale(1.1))
    root.bind('z', lambda x: pm.ChangeScale(1/1.1))

    root.mainloop()
