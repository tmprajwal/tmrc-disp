from PFunc import *
from math import floor

class PCircle:
    def __init__(self, master, number, center, radius):
        self.Type='PCircle'
        self.Category='circle'
        self.PM=master
        self.cv=self.PM.cv
        self.CircumferencePoints=[]
        self.Center=center
        self.Radius=radius
        self.Number=number
        self.Name='Circle'+str(self.Number)
        self.Drawn=False
        self.LabelDrawn=False
        self.Labeled=True
        #self.Arrow=None
        #self.SetArrowShape()
        self.Basewidth=1
        self.DrawnWidth=1
        self.LabelPos=(0,0)
        self.LabelCoord=(0,0)
        self.LabelText=self.Name
        self.Owner=None
        self.Color='White'

        self.Center.AddOwner(self)
        self.Draw()

        #self.TotalLength=0
        #self.Length=0
        #self.Frac=0

    def SetOwner(self, owner):
        self.Owner=owner
        if self.Drawn:
            #self.DrawLabel()
            self.Bind()

    def TellOwner(self):
        return self.Owner
 
    def SetCircleColor(self, color):
        if self.Drawn and color!=self.Color:
            try:
                self.cv.itemconfig(self.Name+'Circle', outline=color)
                self.Color=color
            except:
                print self.Name+'Circle', color

    def Bind(self):
        pass
        #self.cv.tag_bind(self.Name+'Label', '<B1-Motion>', self.DragLabel)
        #self.cv.tag_bind(self.Name+'Line', '<Button-1>', self.AddPoint)

    def Draw(self):
        """Draws this circle"""
        if self.Drawn==False:
            self.cv.create_oval([0,0,0,0], tags=(self.Name, 'Circle', self.Name+'Circle'),
                                outline=self.Color)
            #self.DrawLabel()
            self.Bind()
            self.Drawn=True
        self.UpdateScale()
        self.Center.UpdateShape()
        for pt in self.CircumferencePoints:
            pt.UpdateShape()

    def UpdateScale(self):
        """Update display after scale change."""
        if self.Drawn==True:
            coord = self.Center.TellDCoord()
            scalerad = self.Radius*self.PM.Scale
            boxcoords = [coord[0]-scalerad,coord[1]-scalerad,coord[0]+scalerad,coord[1]+scalerad]
            
            self.cv.coords(self.Name+'Circle', *boxcoords)
            newwidth=max(floor(self.PM.Scale*self.Basewidth), 1)
            if newwidth!=self.DrawnWidth:
                self.DrawnWidth=newwidth
                self.cv.itemconfig(self.Name+'Circle', width=self.DrawnWidth)
            #self.UpdateLabel()

    def UpdatePoints(self, point=None):
        """when moving the center"""
        self.UpdateScale()
        self.Center.UpdateShape()
        for pt in self.CircumferencePoints:
            pt.UpdateShape()
            if point == self.Center.Number:
               pt.DragPoint()

    def AddCircumferencePoint(self, point):
        """Add Point to the circumference"""
        self.CircumferencePoints+=[point]
        point.AddOwner(self)
        point.DragPoint()

    def TellCenter(self):
        return self.Center

    def TellRadius(self):
        return self.Radius

    def TellCircumferencePointList(self):
        return self.CircumferencePoints[:]

    def DeletePoint(self, point):
        """Delete a circumference point from a PCircle.

        This function will delete the specified point from
        the PCircle object."""
        index=self.CircumferencePoints.index(point)
        del self.CircumferencePoints[index]
        self.UpdatePoints(point)

    def Undraw(self):
        if self.Drawn==True:
            self.cv.delete(self.Name)
            self.Drawn=False


