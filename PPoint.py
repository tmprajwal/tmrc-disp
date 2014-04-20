from PFunc import *

class PPoint:
    def __init__(self, master, coord, number, tokens=None):
        self.PM=master
        self.cv=self.PM.cv
        self.Number=number
        
        self.Type='PPoint'
        self.Name='Point'+str(number)
        self.Selected=False
                
        self.Owners={}
        self.DrawShape=self.DrawAsBox
        self.DragShape=self.DragAsBox
        self.UpdateShape=self.DragAsBox
        self.AdjustCoords=None

        self.PointDrawn=False
        
        self.DrawPoint(coord)

    def DrawPoint(self, coord):
        self.Undraw()
        self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', coord, self.AdjustCoords)
        self.DrawShape()
        self.PointDrawn=True
        self.DefineBindings()

    def ChangeStyle(self, newstyle):
        if newstyle=='X':
            self.DrawAsX()
        else:
            self.DrawAsBox()

    def DefineBindings(self):
        self.cv.tag_bind(self.Name+'Point', '<B1-Motion>', self.DragPoint)
        self.cv.tag_bind(self.Name+'Point', '<Button-1>', self.Pass)
        self.cv.tag_bind(self.Name+'Point', '<Button-3>', lambda x:self.PM.DeletePoint(self))

    def GetCoordsAsBox(self):
        return (self.dcoord[0]-5, self.dcoord[1]-5, self.dcoord[0]+5, self.dcoord[1]+5)

    def DrawAsBox(self, where='end'):
        coords=self.GetCoordsAsBox()
        self.cv.create_rectangle(coords, tags=(self.Name, self.Name+'Point', self.Name+'Box', 'Point'), outline='Red', fill='White')

    def SetBoxColors(self, fill='White', outline='Red'):
        self.cv.itemconfig(self.Name+'Box', outline=outline, fill=fill)

    def SetSelected(self, select=False, fill='White', outline='Red'):
        if select==True:
            self.SetBoxColors(fill=fill, outline=outline)
            self.Selected=True
        else:
            self.SetBoxColors(fill=fill, outline=outline)
            self.Selected=False

    def DragAsBox(self):
        coords=self.GetCoordsAsBox()
        self.cv.coords(self.Name+'Box', coords)

    def UpdateBox(self):
        pass

    def ScalePoint(self):
        self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', self.coord, self.AdjustCoords)
        self.DragShape()

    def DragPoint(self, event=None, delta=None):
        if event!=None:
            if self.Selected==False:
                #print 'foo'
                self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'dcoord', (self.cv.canvasx(event.x), self.cv.canvasy(event.y)), self.AdjustCoords)
            elif self.Selected==True:
                delta=(int(self.cv.canvasx(event.x)/self.PM.Scale-self.coord[0]), int(self.cv.canvasy(event.y)/self.PM.Scale-self.coord[1]), self.AdjustCoords)
                self.PM.SelectDrag(self, delta)
                return
        elif delta!=None:
            self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', (self.coord[0]+delta[0], self.coord[1]+delta[1]), self.AdjustCoords)
        else:
            self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', self.coord, self.AdjustCoords)

        for key in self.Owners.keys():
            self.Owners[key].UpdatePoints(self.Number)

    def Undraw(self):
        self.cv.delete(self.Name)
        self.PointDrawn=False

    def TellCoord(self):
        return self.coord

    def TellDCoord(self):
        return self.dcoord

    def AddOwner(self, newowner):
        self.Owners[(newowner.Category,newowner.Number)]=newowner

    def DelOwner(self, oldowner):
        del self.Owners[(oldowner.Category,oldowner.Number)]

    def TellOwners(self):
        return self.Owners

    def Pass(self, event=None):
        pass

    def SetMode(self, mode=None):
        self.DrawShape()

    def SaveString(self, newnum):
        type=self.Type
        coords=str(self.TellCoord())
        string=type+'||num|'+newnum+'||coord|'+coords+'\n'
        return string
    
