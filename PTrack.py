from PLine import *
from PPoint import *
from MiscTrack import *

class PTrack(PLine):
    def __init__(self, master, number):
        PLine.__init__(self, master, number)
        self.Type='PTrack'
        self.Owner=None
        self.Color='None'

    def SetOwner(self, owner):
        self.Owner=owner
        if self.Drawn:
            self.DrawLabel()
            self.Bind()

    def TellOwner(self):
        return self.Owner

    def SetLineColor(self, color):
        if self.Drawn and color!=self.Color:
            try:
                self.cv.itemconfig(self.Name+'Line', fill=color)
                self.Color=color
            except:
                print self.Name+'Line', color

    def SetLineWidth(self, width):
        self.Basewidth=width
        if width==1:
            self.cv.lower(self.Name+'Line')
        self.UpdateScale()

    def SetLabelColor(self, color):
        self.cv.itemconfig(self.Name+'LabelBox', fill=color)
        self.cv.itemconfig(self.Name+'LabelMask', fill=color)

    def SetLabelTextColor(self, color):
        self.cv.itemconfig(self.Name+'LabelText', fill=color)

    def DrawLabel(self):
        self.UndrawLabel()
        if self.Labeled and self.PM.Scale>=self.PM.MinLabelScale:
            self.LabelCoord, dcoord = self.PM.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))

            if self.Owner!=None and self.Owner.Type=='PSwitch':
                drawfunc=self.cv.create_oval
                textfont=switchlabelfont
                textsize=int(switchlabeltext*self.PM.Scale)
                textstyle=switchlabelstyle
                fgcolor='Black'
                bgcolor='White'
            else:
                drawfunc=self.cv.create_rectangle
                textfont=blocklabelfont
                textsize=int(blocklabeltext*self.PM.Scale)
                textstyle=blocklabelstyle
                bgcolor='Black'
                fgcolor='White'

            self.cv.create_text(dcoord, text=self.LabelText, fill=fgcolor,
                                font=(textfont, textsize, textstyle),
                                tags=(self.Name, self.Name+'Label', self.Name+'LabelText', 'LabelText'))

            ltbbox=self.cv.bbox(self.Name+'LabelText')
            border=2*self.PM.Scale
            bbox=(ltbbox[0]-border, ltbbox[1]-border, ltbbox[2]+border, ltbbox[3]+border)
            drawfunc(bbox, fill=bgcolor, outline=None, width=0,
                     tags=(self.Name, self.Name+'Label', self.Name+'LabelBox', 'LabelBox'))
            drawfunc(bbox, fill=bgcolor, outline=None, width=0,
                     tags=(self.Name, self.Name+'Label', self.Name+'LabelMask', 'LabelMask'),
                     stipple='gray75')

            self.cv.lower(self.Name+'LabelBox')
            self.cv.lift(self.Name+'LabelMask')
            self.cv.lift(self.Name+'LabelText')

            self.Bind()
            self.LabelDrawn=True
    
    def UpdateLabel(self):
        if self.PM.Scale<self.PM.MinLabelScale and self.LabelDrawn:
            self.UndrawLabel()
        elif self.PM.Scale>=self.PM.MinLabelScale and not self.LabelDrawn:
            self.DrawLabel()
        elif self.Drawn and self.Labeled:
            coord, dcoord = self.PM.TrueCoord(-1, 'label', self.LinePos(self.LabelPos))
            self.cv.coords(self.Name+'LabelText', dcoord)
            if self.Owner!=None and self.Owner.Type=='PSwitch':
                textfont=switchlabelfont
                textsize=int(switchlabeltext*self.PM.Scale)
                textstyle=switchlabelstyle
            else:
                textfont=blocklabelfont
                textsize=int(blocklabeltext*self.PM.Scale)
                textstyle=blocklabelstyle

            self.cv.itemconfig(self.Name+'LabelText', font=(textfont, textsize, textstyle))
            ltbbox=self.cv.bbox(self.Name+'LabelText')
            if ltbbox==None:
                self.UndrawLabel()
            else:
                border=2*self.PM.Scale
                bbox=(ltbbox[0]-border, ltbbox[1]-border, ltbbox[2]+border, ltbbox[3]+border)
                self.cv.coords(self.Name+'LabelMask', bbox)
                self.cv.coords(self.Name+'LabelBox', bbox)

    def Bind(self):
        if self.PM.Clickable:
            self.cv.tag_unbind(self.Name+'Label', '<B1-Motion>')
            self.cv.tag_unbind(self.Name, '<Button-1>')
            self.cv.tag_unbind(self.Name+'Line', '<Button-1>')
            self.cv.tag_unbind(self.Name+'Line', '<Button-3>')
            self.cv.tag_unbind(self.Name+'Label', '<Button-1>')

            if self.Owner!=None:
                if self.PM.Mode=='Edit':
                    self.cv.tag_bind(self.Name+'Label', '<B1-Motion>', self.DragLabel)
                    self.cv.tag_bind(self.Name+'Line', '<Button-1>', self.AddPoint)
                    self.cv.tag_bind(self.Name+'Line', '<Button-3>', lambda x: self.Owner.DeleteInstance(self))
                elif self.PM.Mode=='Run':
                    self.cv.tag_bind(self.Name+'Label', '<Button-1>', self.Clicked)
                    self.cv.tag_bind(self.Name+'Line', '<Button-1>', self.Clicked)
                    self.cv.tag_bind(self.Name+'Label', '<Control-Button-1>', self.DebugInfo)
                    self.cv.tag_bind(self.Name+'Line', '<Control-Button-1>', self.DebugInfo)
                    self.cv.tag_bind(self.Name+'Label', '<Button-3>', self.OutOfService)
                    self.cv.tag_bind(self.Name+'Line', '<Button-3>', self.OutOfService)

    def AddPoint(self, event):
        minindex, intcoord=self.NearestSegment('dcoord', (self.cv.canvasx(event.x), self.cv.canvasy(event.y)))
        self.PM.AddTrackPointToLine(intcoord, self.Number, minindex+1)

    def Clicked(self, event):
        if self.PM.Clickable:
            self.Owner.Clicked(event,self)

    def OutOfService(self, event):
        if self.PM.Clickable:
            self.Owner.OutOfService(event)

    def DebugInfo(self, event):
        if self.PM.Clickable:
            self.Owner.DebugInfo(event)

    def IsGap(self, end):
        if self.Owner!=None:
            return self.Owner.IsGap(end, self)
        else:
            return False

    def SignalColor(self, end):
        return self.Owner.SignalColor(end, self)

    def TrueEnd(self, point):
        end=self.IsPointEnd(point)
        end=self.Owner.TrueEnd(end, self)
        return end
