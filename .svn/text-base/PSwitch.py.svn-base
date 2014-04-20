from PLine import *
from PPoint import *
from PTrack import *
from MiscTrack import *


NONE='none'
FIRST='first'
LAST='last'

class PSwitch:
    def __init__(self, master, owner):
        self.PM=master
        self.cv=self.PM.cv
        self.Switch=owner
        self.Type='PSwitch'
        self.Name=self.Switch.name
        self.Lines0={}
        self.Lines1={}
        self.Switch.AddDisplayObject(self)
        self.SignalColor0='White'
        self.SignalColor1='White'
        self.SignalColor2='White'
        self.UpdateStatus()
    
    def AddLine(self, line0, line1):
        if self.Switch.name[-2:]=='-1':
            labeltext=self.Switch.name[1:-2]
            labelstatus=False
        else:
            labeltext=self.Switch.name[1:]
            labelstatus=True

        self.Lines0[line0.Number]=line0
        line0.SetOwner(self)
        line0.SetLabelText(labeltext)
        line0.LabelStatus(labelstatus)

        self.Lines1[line1.Number]=line1
        line1.SetOwner(self)
        line1.SetLabelText(labeltext)
        line1.LabelStatus(False)

        self.SetMode()

    def DeleteInstance(self, instline):
        point0=instline.TellEndPoint(0)
        lines=point0.TellOwners()
        for line in lines.keys():
            linenum=lines[line].Number
            if self.Lines0.has_key(linenum):
                self.PM.DeleteLine(self.Lines0[linenum])
                del self.Lines0[linenum]
            elif self.Lines1.has_key(linenum):
                self.PM.DeleteLine(self.Lines1[linenum])
                del self.Lines1[linenum]
        if len(self.Lines0.keys())==0:
            self.PM.DeleteObject(self)

    def DeleteAllInstances(self):
        self.Switch.DelDisplayObject(self)
        for line in self.Lines0.keys():
            self.PM.DeleteLine(self.Lines0[line])
            del self.Lines0[line]
        for line in self.Lines1.keys():
            self.PM.DeleteLine(self.Lines1[line])
            del self.Lines1[line]

    def UpdateStatus(self):
        if self.PM.Mode=='Run':
            color=self.Switch.FindLabelColor()
            if self.Switch.HeadEnd==0:
                arrow=FIRST
            elif self.Switch.HeadEnd in (1, 2):
                arrow=LAST
            else:
                arrow=NONE

            if self.Switch.switchpos==0:
                width0=activewidth
                fill0=self.Switch.FindColor()
                arrow0=arrow
                width1=inactivewidth
                fill1=blkcolor[INACC][UNOCC]
                arrow1=NONE
            else:
                width0=inactivewidth
                fill0=blkcolor[INACC][UNOCC]
                arrow0=NONE
                width1=activewidth
                fill1=self.Switch.FindColor()
                arrow1=arrow

##            print fill0, fill1, color, occ, act, self.Name
            
            for linenum in self.Lines0.keys():
                self.Lines0[linenum].SetLineColor(fill0)
                self.Lines0[linenum].SetLineWidth(width0)
                self.Lines0[linenum].SetLabelColor(color)
                self.Lines0[linenum].UpdateArrow(arrow0)
            for linenum in self.Lines1.keys():
                self.Lines1[linenum].SetLineColor(fill1)
                self.Lines1[linenum].SetLineWidth(width1)
                self.Lines1[linenum].UpdateArrow(arrow1)

            color0=self.SignalColor(0)
            if self.SignalColor0!=color0:
                self.SignalColor0=color0
                self.cv.itemconfig(self.Name+'Signal0', fill=color0)
            color1=self.SignalColor(1)
            if self.SignalColor1!=color1:
                self.SignalColor1=color1
                self.cv.itemconfig(self.Name+'Signal1', fill=color1)
            color2=self.SignalColor(2)
            if self.SignalColor2!=color2:
                self.SignalColor2=color2
                self.cv.itemconfig(self.Name+'Signal2', fill=color2)

        elif self.PM.Mode=='Edit':
            if self.Switch.hand==0:
                color0='Red'
                color1='Green'
            else:
                color0='Green'
                color1='Red'

            for linenum in self.Lines0.keys():
                self.Lines0[linenum].SetLineColor(color0)
                self.Lines0[linenum].SetLineWidth(4)
            for linenum in self.Lines1.keys():
                self.Lines1[linenum].SetLineColor(color1)
                self.Lines1[linenum].SetLineWidth(4)

    def SetMode(self):
        self.UpdateStatus()
        for linenum in self.Lines0.keys():
            self.Lines0[linenum].Bind()
        for linenum in self.Lines1.keys():
            self.Lines1[linenum].Bind()

    def OutOfService(self, event=None):
        self.Switch.OutOfService(event)

    def Clicked(self, event, source=None):
        self.Switch.ThrowSwitch(event)

    def DebugInfo(self, event=None):
        self.Switch.DebugInfo(event)

    def NextObject(self, end, line):
        if end==1:
            if self.Lines1.has_key(line.Number):
                end=2
        object=self.Switch.Cons[end].Object
        if object!=None:
            con=self.Switch.Cons[end].ObjCon
        else:
            con=0
        return object, con

    def TrueEnd(self, end, line):
        if end==1:
            if self.Lines1.has_key(line.Number):
                end=2
        return end

    def IsGap(self, end, line):
        end=self.TrueEnd(end, line)
        isgap=self.Switch.IsGap(end)
        return isgap

    def SignalColor(self, end, line=None):
        if line!=None:
            end=self.TrueEnd(end, line)
        return self.Switch.SignalColor(end)

    def Connects(self, events=None):
        objname0=self.Switch.Cons[0].Object
        objcon0=self.Switch.Cons[0].ObjCon
        objname1=self.Switch.Cons[1].Object
        objcon1=self.Switch.Cons[1].ObjCon
        objname2=self.Switch.Cons[2].Object
        objcon2=self.Switch.Cons[2].ObjCon
        print self.Switch.name, '0:', objname0, objcon0, '1:', objname1, objcon1, '2:', objname2, objcon2      

    def Connection(self, connection):
        object=self.Switch.Cons[connection].Object
        objcon=self.Switch.Cons[connection].ObjCon
        return object, objcon

    def TellPoints(self, connection):
        points=[]
        if connection == 2:
            Lines=self.Lines1
        else:
            Lines=self.Lines0
        for line in Lines.keys():
            points+=[Lines[line].TellEndPoint(connection)]
        return points

    def TellLines(self):
        return self.Lines0.keys(), self.Lines1.keys()

    def ShowDebugInfo(self, debugtext):
        self.cv.delete('debug-info')
        for line in self.Lines0.values():
            if line.LabelDrawn:
                dcoord=line.TellLabelDCoord()
                self.cv.create_text(dcoord,
                              text=debugtext,
                              fill='White',
                              font=('Arial', 10),
                              tags=('debug-info', 'debug-text'))
                tbbox=self.cv.bbox('debug-info')
                bbox=(tbbox[0]-2, tbbox[1]-2, tbbox[2]+2, tbbox[3]+2)
                self.cv.create_rectangle(bbox,
                                           fill='Black',
                                           outline='White',
                                           width=1,
                                           tags=('debug-info', 'debug-box'))
                self.cv.lift('debug-text')
                self.cv.tag_bind('debug-box', '<Leave>', lambda *args, **kw: self.cv.delete('debug-info'))
