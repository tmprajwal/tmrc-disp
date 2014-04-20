from PCircle import *
from PPoint import *
from MiscTrack import *

class PTurnTableCircle(PCircle):
    def __init__(self, master, number, center, radius):
        PCircle.__init__(self, master, number, center, radius)
        self.Type='PTurnTableCircle'

    def Bind(self):
        if self.PM.Clickable:
            self.cv.tag_unbind(self.Name, '<Button-1>')
            self.cv.tag_unbind(self.Name+'Circle', '<Button-1>')
            self.cv.tag_unbind(self.Name+'Circle', '<Button-3>')

            if self.Owner!=None:
                if self.PM.Mode=='Edit':
                    #self.cv.tag_bind(self.Name+'Circle', '<Button-1>', self.AddPoint)
                    self.cv.tag_bind(self.Name+'Circle', '<Button-3>', lambda x: self.Owner.DeleteInstance(self))
                elif self.PM.Mode=='Run':
                    self.cv.tag_bind(self.Name+'Circle', '<Button-1>', self.Clicked)
                    self.cv.tag_bind(self.Name+'Circle', '<Control-Button-1>', self.DebugInfo)
                    self.cv.tag_bind(self.Name+'Circle', '<Button-3>', self.OutOfService)

    def Clicked(self, event):
        if self.PM.Clickable:
            self.Owner.Clicked(event,self)

    def OutOfService(self, event):
        if self.PM.Clickable:
            self.Owner.OutOfService(event)

    def DebugInfo(self, event):
        if self.PM.Clickable:
            self.Owner.DebugInfo(event)
