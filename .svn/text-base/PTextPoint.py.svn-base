from PFunc import *
from Tkinter import *
import Pmw
import PPoint

import math

# Constants for point and signal sizes
SIGSIZE=10
POINTSIZE=10

class PTextPoint(PPoint.PPoint):
    def __init__(self, master, coord, number, tokens=None):
        PPoint.PPoint.__init__(self, master, coord, number)

        self.Type='PTextPoint'
        self.DrawShape=self.DrawTextPoint
        self.DragShape=self.DragTextPoint
        self.UpdateShape=self.UpdateTextPoint
        self.Text='Textpoint '+str(self.Number)
        self.TextSize=28
        if tokens!=None:
            for token in tokens[3:]:
                stoken=token.split('|')
                exec('self.'+stoken[0]+'='+stoken[1])
        self.DrawShape()
        #self.SetMode()
        self.EditWindow=None

    def DrawTextPoint(self):
        self.Undraw()

        if self.PM.Mode=='Edit':
            self.DrawAsText()
            self.DrawAsBox()
            self.PointDrawn=True
            self.DefineBindings()
        elif self.PM.Mode=='Run':
            self.DrawAsText()
            self.PointDrawn=True

    def DragTextPoint(self):
        if self.TextSize*self.PM.Scale<8 and self.PointDrawn:
            self.Undraw()
        elif self.TextSize*self.PM.Scale>=8 and not self.PointDrawn:
            self.DrawShape()
        else:
            self.DragAsBox()
            self.DragAsText()

    def UpdateTextPoint(self):
        self.DragShape()

    def DrawAsText(self):
        self.cv.create_text(self.dcoord, text=self.Text, fill='White',
                            font=('Arial', int(self.PM.Scale*self.TextSize)),
                            tags=('Text', self.Name+'Text', self.Name))
        self.cv.tag_bind(self.Name+'Text', '<Button-1>', self.TextClicked)

    def DragAsText(self):
        self.cv.coords(self.Name+'Text', self.dcoord)
        self.cv.itemconfig(self.Name+'Text', font=('Arial', int(self.PM.Scale*self.TextSize), 'bold'))

    def DragPoint(self, event=None, delta=None):
        if event!=None:
            if self.Selected==False:
                self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'dlabel', (self.cv.canvasx(event.x), self.cv.canvasy(event.y)))
            elif self.Selected==True:
                delta=(int(self.cv.canvasx(event.x)/self.PM.Scale-self.coord[0]), int(self.cv.canvasy(event.y)/self.PM.Scale-self.coord[1]))
                self.PM.SelectDrag(self, delta)
                return
        elif delta!=None:
            self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', (self.coord[0]+delta[0], self.coord[1]+delta[1]))
        else:
            self.coord, self.dcoord=self.PM.TrueCoord(self.Number, 'coord', self.coord)

        self.DragShape()

    def SetSelected(self, select=False, fill='White', outline='Red'):
        if select==True:
            self.SetBoxColors(fill=fill, outline=outline)
            self.Selected=True
        else:
            self.SetBoxColors(fill='White', outline='Red')
            self.Selected=False

    def TextClicked(self, event=None):
        if self.PM.Mode=='Run':
            pass
        elif self.PM.Mode=='Edit':
            if self.EditWindow==None:
                self.CreateTextEditWindow()

    def CreateTextEditWindow(self):
        self.EditWindow=Toplevel(self.PM.DM.Window)
        self.EditWindow.title('Text Point Editor')
        self.EditWindow.protocol("WM_DELETE_WINDOW", self.CloseTextEditWindow)
        self.EditWindow.resizable(0,0)
        self.EditWindow.transient(self.PM.DM.Window)

        Label(self.EditWindow, text='Enter text for point').pack(side=TOP)
        self.EnteredName=StringVar()
        self.EnteredName.set(self.Text)
        self.TextEntry=Entry(self.EditWindow, width=25, textvariable=self.EnteredName)
        self.TextEntry.pack(side=TOP)
        self.TextEntry.focus_set()

        self.SizeCounter=Pmw.Counter(self.EditWindow, labelpos='e',
                                     label_text='Text size',
                                     datatype='integer',
                                     entryfield_value=self.TextSize,
                                     entryfield_validate = {'validator' : 'integer', 'min' : '1'},
                                     increment=1)
        self.SizeCounter.pack(side=TOP)

        buttonframe=Frame(self.EditWindow)
        Button(buttonframe, command=self.ApplyChanges, text='Apply Changes').pack(side=LEFT)
        Button(buttonframe, command=self.CloseTextEditWindow, text='Close').pack(side=LEFT)
        buttonframe.pack(side=TOP)

    def ApplyChanges(self, event=None):
        self.Text = self.EnteredName.get()
        self.TextSize = int(self.SizeCounter.getvalue())
        self.cv.itemconfig(self.Name+'Text', text=self.Text, fill='White',
                           font=('Arial', int(self.PM.Scale*self.TextSize)))


    def CloseTextEditWindow(self, event=None):
        self.EditWindow.destroy()
        del self.EditWindow
        self.EditWindow=None

    def SaveString(self, newnum):
        type=self.Type
        coords=str(self.TellCoord())
        text=self.Text
        textsize=str(self.TextSize)
        string=type+'||num|'+newnum+'||coord|'+coords+'||Text|"'+text+'"||TextSize|'+textsize+'\n'
        return string
