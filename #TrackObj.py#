# Thomas O'Reilly, 3 August 2002
# TMRC System 3 display software track element base class

from MiscTrack import *

class TrackObj:
    """Parent class for track objects

    This class in intended to be a superclass for the block
    and switch object classes."""
    def __init__(self, master, name):
        self.master=master
        self.name=name
        self.DName=self.name
        self.DisplayObjects=[]
    
    def AddDisplayObject(self, displayobject):
        self.DisplayObjects+=[displayobject]

    def ConInfo(self, end, value, vsub):
        """Store track connection data.

        Stores the type, name, and connection of connected
        objects in the correct memory locations.  ObjCon is
        the connection on the block or switch Object that is
        connected to end 'end' on the block."""
        if end in range(len(self.Cons)) and self.master.Ddict.has_key(value):
            self.Cons[end].Object=self.master.Ddict[value]
            self.Cons[end].ObjCon=vsub
            self.Cons[end].ObjType=self.Cons[end].Object.ObjType()
            if self.HeadBlock != None:
                self.HeadBlock.IsHeadBlock()
        else:
            self.master.logger.LogWarnMsg('Unknown something '+value+' '+str(end))

    def DelDisplayObject(self, displayobject):
        index=self.DisplayObjects.index(displayobject)
        del self.DisplayObjects[index]

    def UpdateDisplayObjects(self):
        for displayobject in self.DisplayObjects:
            displayobject.UpdateStatus()

    def SetDName(self, dname):
        self.DName=dname
        for displayobject in self.DisplayObjects:
            displayobject.SetDName(self.DName)

    def IsGap(self, end):
        return self.Cons[end].gap

    def SignalColor(self, end):
        if end not in (0, 1):
            return 'Purple'
        return sigcolor[self.Cons[end].Signal]

    def DebugInfo(self, event=None):
        OutStr='(info (Obj "'+self.name+'"))'
        self.master.SockWrite(OutStr)

    def ShowDebugInfo(self, debugtext):
        for displayobject in self.DisplayObjects:
            if displayobject.Type in ('PBlock', 'PSwitch', 'PCrossing', 'PTurnTable'):
                displayobject.ShowDebugInfo(debugtext)

