from Tkinter import *
import tkFileDialog
import math
import random

from PCircle import *
from PLine import *
from PPoint import *
from PFunc import *

class PLineManager:
    def __init__(self, cv):
        self.cv=cv

        self.pointnum=0
        self.linenum=0
        self.circlenum=0
        self.arrownum=0
        self.points={}
        self.lines={}
        self.circles={}
        self.arrows={}
        self.PickedPoints0=[]
        self.PickedPoints1=[]
        self.CursorCoord=(0, 0)

        self.Scale=1
        self.SnapInc=20

    def AddCircle(self, center, radius):
        self.circles[self.circlenum]=PCircle(self, self.circlenum, center, radius)
        self.circlenum+=1
        return self.circles[self.circlenum-1]

    def AddLine(self):
        self.lines[self.linenum]=PLine(self, self.linenum)
        self.linenum+=1
        return self.lines[self.linenum-1]

    def AddPoint(self, coord):
        self.points[self.pointnum]=PPoint(self, coord, self.pointnum)
        self.pointnum+=1
        return self.points[self.pointnum-1]

    def ChangeScale(self, ratio=0, scale=1):
        if ratio==0:
            self.Scale=scale
        else:
            self.Scale*=ratio
        points=self.points.keys()
        for point in points:
            self.points[point].ScalePoint()
        lines=self.lines.keys()
        for line in lines:
            self.lines[line].UpdateScale()
        circles=self.circles.keys()
        for circle in circles:
            self.circles[circle].UpdateScale()
        self.Refresh()

    def TrueBBox(self):
        if len(self.points.keys())==0:
            return None
        else:
            pointnums=self.points.keys()
            zerocoords=self.points[pointnums[0]].TellCoord()
            xmin=zerocoords[0]
            xmax=zerocoords[0]
            ymin=zerocoords[1]
            ymax=zerocoords[1]
            for pointnum in pointnums[1:]:
                coords=self.points[pointnum].TellCoord()
                if coords[0]<xmin:
                    xmin=coords[0]
                elif coords[0]>xmax:
                    xmax=coords[0]
                if coords[1]<ymin:
                    ymin=coords[1]
                elif coords[1]>ymax:
                    ymax=coords[1]
            circlenums=self.circles.keys()
            for circlenum in circlenums:
                ccoords=self.circles[circlenum].TellCenter().TellCoord()
                rad=self.circles[circlenum].TellRadius()
                if coords[0]-rad<xmin:
                    xmin=coords[0]-rad
                elif coords[0]+rad>xmax:
                    xmax=coords[0]+rad
                if coords[1]-rad<ymin:
                    ymin=coords[1]-rad
                elif coords[1]+rad>ymax:
                    ymax=coords[1]+rad

            return (xmin, ymin, xmax, ymax)

    def ScaleToFit(self, width=None, height=None):
        bbox=self.TrueBBox()
        if bbox==None:
            return None
        else:
            truewidth=float(bbox[2]-bbox[0])+50
            trueheight=float(bbox[3]-bbox[1])+50
            if width!=None:
                xscale=width/truewidth
                newscale=xscale
            if height!=None:
                yscale=height/trueheight
                newscale=yscale
            if width!=None and height!=None:
                if xscale<yscale:
                    newscale=xscale

            self.ChangeScale(scale=newscale)
            return (int(truewidth*newscale), int(trueheight*newscale))

    def AddPointToLine(self, coord, line, index=None):
        point=self.AddPoint(coord)
        line.InsertPoint(point, index)

    def DeletePoint(self, point):
        owners=point.TellOwners()
        if len(owners.keys())>1:
            print 'Cannot delete shared point', point.Number
        elif len(owners.keys())==1:
            if not hasattr(owners[owners.keys()[0]],'TellPointList'):
                print 'Cannot delete point', point.Number, 'it is used by', owners[owners.keys()[0]].Type, owners[owners.keys()[0]].Number
            elif len(owners[owners.keys()[0]].TellPointList())<=2:
                print 'Deleting point', point.Number, 'will leave line lonely'
            else:
                owners[owners.keys()[0]].DeletePoint(point)
                point.Undraw()
                del self.points[point.Number]
        else:
            point.Undraw()
            del self.points[point.Number]

    def DeleteLine(self, line):
        pointlist=line.TellPointList()

        for point in pointlist:
            line.DeletePoint(point)
            point.DelOwner(line)
            point.UpdateShape()
            owners=point.TellOwners()
            if len(owners.keys())==0:
                self.DeletePoint(point)

        del self.lines[line.Number]

    def DeleteCircle(self, circle):
        pointlist=circle.TellCircumferencePointList()
        center=circle.TellCenter()
        
        for point in pointlist:
            circle.DeletePoint(point)
            point.DelOwner(circle)
            point.UpdateShape()
            owners=point.TellOwners()
            if len(owners.keys())==0:
                self.DeletePoint(point)

        del self.circles[circle.Number]
        circle.Undraw()
        center.DelOwner(circle)
        center.UpdateShape()
        owners=center.TellOwners()
        if len(owners.keys())==0:
            self.DeletePoint(center)

    def TrueCoord(self, pointnum, type, coord, adjusting_func=None):
        if type in ('dcoord', 'dlabel'):
            coord=(coord[0]/float(self.Scale), coord[1]/float(self.Scale))
        if adjusting_func != None:
            coord=adjusting_func(coord)
        elif self.SnapInc!=0 and type not in ('label', 'dlabel'):
            Snap=int(self.SnapInc)
            coord=(int(Snap*math.floor(float(coord[0])/Snap+0.5)), int(Snap*math.floor(float(coord[1])/Snap+0.5)))
        else:
            coord=coord
        dcoord=(int(coord[0]*self.Scale), int(coord[1]*self.Scale))
        return coord, dcoord

    def DrawCross(self, event=None):
        self.CancelSelect()
        self.DrawVertical(event)
        self.DrawHorizontal(event)
        self.BP0=None
        self.BP1=None
        self.cv.bind('<Motion>', self.DragCross)
        self.cv.bind('<Button-1>', self.BoxPoint)
        self.cv.bind('<Button-3>', self.CancelSelect)

    def BoxPoint(self, event=None):
        if self.BP0==None:
            self.BP0=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
            self.UndrawCross()
            self.DrawBox()
            self.cv.bind('<Motion>', self.DragBox)
        else:
            self.BP1=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
            self.UndrawBox()
            bbox=[0, 0, 0, 0]
            if self.BP1[0]>=self.BP0[0]:
                bbox[0]=self.BP0[0]
                bbox[2]=self.BP1[0]
            else:
                bbox[0]=self.BP1[0]
                bbox[2]=self.BP0[0]
            if self.BP1[1]>=self.BP0[1]:
                bbox[1]=self.BP0[1]
                bbox[3]=self.BP1[1]
            else:
                bbox[1]=self.BP1[1]
                bbox[3]=self.BP0[1]
            self.SelectByBox(bbox)
            self.cv.unbind('<Button-1>')
            self.cv.unbind('<Button-3>')

    def DrawBox(self, event=None):
        coords=(self.BP0, self.BP0)
        self.cv.create_rectangle(coords, outline='White', tags=('Box'))

    def UndrawBox(self):
        self.cv.delete('Box')
            
    def DragBox(self, event=None):
        self.CursorCoord=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
        coords=self.BP0+self.CursorCoord
        self.cv.coords('Box', coords)

    def SelectByBox(self, bbox):
        pointnumbers=self.points.keys()
        self.PickedPoints0=[]
        for pointnumber in pointnumbers:
            dcoord=self.points[pointnumber].TellDCoord()
            if bbox[0]<dcoord[0]<bbox[2] and bbox[1]<dcoord[1]<bbox[3]:
                self.PickedPoints0+=[self.points[pointnumber]]
                self.points[pointnumber].SetSelected(True, fill='Blue', outline='White')
            else:
                self.PickedPoints1+=[self.points[pointnumber]]
                self.points[pointnumber].SetSelected(True, fill='Green', outline='White')

    def DragCross(self, event):
        self.CursorCoord=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
        self.DragVertical(event)
        self.DragHorizontal(event)

    def UndrawCross(self, event=None):
        self.UndrawVertical()
        self.UndrawHorizontal()

    def VerticalCoords(self, event):
        if 'x' in dir(event):
            x=self.cv.canvasx(event.x)
        else:
            x=0
        height=self.cv.winfo_height()
        coordsv=(x, self.cv.canvasy(0), x, self.cv.canvasy(height))
        return coordsv

    def DrawVertical(self, event=None):
        self.cv.delete('CrossV')
        coordsv = self.VerticalCoords(event)
        self.cv.create_line(coordsv, tags=('Cross', 'CrossV'), fill='White')
        self.cv.bind('<Motion>', self.DragVertical)
        self.cv.bind('<Button-1>', self.SelectX)
        self.cv.bind('<Button-3>', self.CancelSelect)

    def UndrawVertical(self, event=None):
        self.cv.delete('CrossV')
        self.cv.unbind('<Motion>')

    def DragVertical(self, event):
        self.CursorCoord=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
        coordsv = self.VerticalCoords(event)
        self.cv.coords('CrossV', coordsv)

    def HorizontalCoords(self, event):
        if 'y' in dir(event):
            y=self.cv.canvasy(event.y)
        else:
            y=0
        width=self.cv.winfo_width()
        coordsh=(self.cv.canvasx(0), y, self.cv.canvasx(width), y)
        return coordsh

    def DrawHorizontal(self, event=None):
        self.cv.delete('CrossH')
        coordsh = self.HorizontalCoords(event)
        self.cv.create_line(coordsh, tags=('Cross', 'CrossH'), fill='White')
        self.cv.bind('<Motion>', self.DragHorizontal)
        self.cv.bind('<Button-1>', self.SelectY)
        self.cv.bind('<Button-3>', self.CancelSelect)

    def UndrawHorizontal(self, event=None):
        self.cv.delete('CrossH')
        self.cv.unbind('<Motion>')

    def DragHorizontal(self, event=None):
        if event==None:
            pass
        self.CursorCoord=(self.cv.canvasx(event.x), self.cv.canvasy(event.y))
        coordsh = self.HorizontalCoords(event)
        self.cv.coords('CrossH', coordsh)

    def SelectDrag(self, point, delta):
        if point in self.PickedPoints0:
            for point in self.PickedPoints0:
                point.DragPoint(delta=delta)
        elif point in self.PickedPoints1:
            for point in self.PickedPoints1:
                point.DragPoint(delta=delta)

    def SelectBySplit(self, X=None, Y=None):
        pointnumbers=self.points.keys()
        self.PickedPoints0=[]
        self.PickedPoints1=[]
        for pointnumber in pointnumbers:
            dcoord=self.points[pointnumber].TellDCoord()
            if X!=None:
                if dcoord[0]<X:
                    self.PickedPoints0+=[self.points[pointnumber]]
                    self.points[pointnumber].SetSelected(True, fill='Blue', outline='White')
                else:
                    self.PickedPoints1+=[self.points[pointnumber]]
                    self.points[pointnumber].SetSelected(True, fill='Green', outline='White')
            if Y!=None:
                if dcoord[1]<Y:
                    self.PickedPoints0+=[self.points[pointnumber]]
                    self.points[pointnumber].SetSelected(True, fill='Blue', outline='White')
                else:
                    self.PickedPoints1+=[self.points[pointnumber]]
                    self.points[pointnumber].SetSelected(True, fill='Green', outline='White')

    def SelectX(self, event):
        self.SelectBySplit(X=self.CursorCoord[0])
        self.CancelSelect()

    def SelectY(self, event):
        self.SelectBySplit(Y=self.CursorCoord[1])
        self.CancelSelect()

    def CancelSelect(self, event=None):
        self.UndrawCross()
        self.UndrawBox()
        self.SelectUnbind()

    def SelectUnbind(self, event=None):
        self.cv.unbind('<Motion>')
        self.cv.unbind('<Button-1>')
        self.cv.unbind('<Button-3>')

    def Unselect(self, event=None, points=None):
        if points==None:
            for point in self.PickedPoints0:
                point.SetSelected(False)
            for point in self.PickedPoints1:
                point.SetSelected(False)
        else:   
            for point in points:
                point.SetSelected(False)
                if point in self.PickedPoints0:
                    index=self.PickedPoints0.index(pointnumber)
                    del self.PickedPoints0[index]
                elif point in self.PickedPoints1:
                    index=self.PickedPoints1.index(pointnumber)
                    del self.PickedPoints1[index]

    def Refresh(self):
        pass

    def Restack(self):
        cv=self.cv.interior()
##        cv.lower('Point')
        cv.lower('Arrow')
        cv.lower('LineLabel')
        cv.lower('Line')

if __name__=='__main__':
    root=Tk()
    cv=Canvas(root, bg='Black')
    cv.pack(side=TOP, fill=BOTH, expand=1)
    pm=PLineManager(cv)
    root.bind('a', lambda x: pm.ChangeScale(1.1))
    root.bind('z', lambda x: pm.ChangeScale(1/1.1))

    root.mainloop()
