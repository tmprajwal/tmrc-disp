# Thomas O'Reilly, 2 March 2002
# TMRC System 3 display software switch object definitions

from MiscTrack import *
from Tkinter import *
import TrackObj

pad=0
throwbgcolor=['White', 'Black']
throwtxcolor=['Black', 'White']

class SwitchObj(TrackObj.TrackObj):
    def __init__(self, master, name):
# Initialize base class
        TrackObj.TrackObj.__init__(self, master, name)

        self.type='switch'
        self.switchpos=0
        self.outofservice=0 #JYK
        self.offline=0
        self.expectedCxn = 3
        self.Cons=[ConObj(), ConObj(), ConObj()]

# These are things related to the graphical display process
        self.card=None
        self.orient=None
        self.hand=LEFTHAND
        self.Swing=False
        self.HeadBlock=None
        self.HeadEnd=None
        self.Train=None

        self.OccStatus=UNOCC
        self.ActStatus=ONLINE
        self.editing=False
        self.Color='White'

    def ObjType(self):
        return 'switch'

    def SignalColor(self, end):
        if end not in (0, 1, 2):
            return 'Purple'
        return sigcolor[self.Cons[end].Signal]

    def UpdateSignal(self, end, signal):
        if end in (0, 1, 2):
            self.Cons[end].Signal=signal
        else:
            self.master.logger.LogWarnMsg('Unknown switch position: '+str(end)+' in switch '+self.name)

    def CheckSwing(self, swing=None):
        if swing!=None:
            self.Swing=swing
        elif self.Swing=='unknown':
            if self.Cons[0].Object==None or self.Cons[0].gap==True:
                self.Swing='swing'
                return
            else:
                if self.Cons[0].Object.type=='block':
                    self.Swing='regular'
                    return
                elif self.Cons[0].Object.type=='switch':
                    if self.Cons[0].ObjCon==0:
                        if self.Cons[0].Object.IsSwing()=='regular':
                            self.Swing='swing'
                            return
                        elif self.Cons[0].Object.IsSwing()=='swing':
                            self.Swing='regular'
                            return
                    else:
                        self.Swing=self.Cons[0].Object.IsSwing()
                        if self.Swing!='unknown':
                            return
                elif self.Cons[0].Object.type=='crossing':
                    print 'In switchobj.py, CheckSwing(), "crossing" type not handled intelligently'

            for con in (1, 2):
                if self.Cons[con].Object==None or self.Cons[con].gap==True:
                    self.Swing='regular'
                    return
                else:
                    if self.Cons[con].Object.type=='block':
                        self.Swing='swing'
                        return
                    elif self.Cons[con].Object.type=='switch':
                        if self.Cons[con].ObjCon==0:
                            self.Swing=self.Cons[con].Object.IsSwing()
                            if self.Swing!='unknown':
                                return
                        else:
                            if self.Cons[con].Object.IsSwing()=='regular':
                                self.Swing='swing'
                                return
                            elif self.Cons[con].Object.IsSwing()=='swing':
                                self.Swing='regular'
                                return
                    elif self.Cons[con].Object.type=='crossing':
                        print 'In switchobj.py, CheckSwing(), "crossing" type not handled intelligently'
                             

    def IsSwing(self):
        return self.Swing

    def UpdateStatus(self, connect=None, callingobject=()):
        occ=self.OccStatus
        act=self.ActStatus
        train=self.Train
        color=self.Color
        if self.Swing!='swing' and self.Cons[0].Object!=None:
            occ, act, train=self.Cons[0].Object.GState(self.Cons[0].ObjCon)
            color=self.Cons[0].Object.FindColor(self.Cons[0].ObjCon)
        else:
            if self.switchpos==0 and self.Cons[1].gap==False and self.Cons[1].Object!=None:
                occ, act, train=self.Cons[1].Object.GState(self.Cons[1].ObjCon)
                color=self.Cons[1].Object.FindColor(self.Cons[1].ObjCon)
            elif self.switchpos==1 and self.Cons[2].gap==False and self.Cons[1].Object!=None:
                occ, act, train=self.Cons[2].Object.GState(self.Cons[2].ObjCon)
                color=self.Cons[2].Object.FindColor(self.Cons[2].ObjCon)

            #if self.Cons[0].Object!=None:
            #    act0=self.Cons[0].Object.IsEndAccessible(self.Cons[0].ObjCon)
            #    if act0==False:
            #        act=INACC

        if occ!=self.OccStatus or act!=self.ActStatus or train!=self.Train or color!=self.Color or connect==None:
            self.OccStatus=occ
            self.ActStatus=act
            self.Train=train
            self.Color=color
            
            for connum in range(len(self.Cons)):
                if self.Cons[connum].Object not in callingobject and self.Cons[connum].Object != None and self.Cons[connum].gap==False:
                    self.Cons[connum].Object.UpdateStatus(self.Cons[connum].ObjCon, callingobject+(self,))

            self.UpdateDisplayObjects()

    def IsEndAccessible(self, end):
        if end==0:
            return True
        elif end in (1, 2) and self.switchpos+1!=end:
            return False
        else:
            return True

    def IsNotHead(self, block):
        if self.HeadBlock==block:
            self.HeadBlock=None
            self.HeadEnd=None
            self.UpdateStatus()

    def IsOppEndHead(self, end, block):
        if end==0:
            oppend=self.switchpos+1
        else:
            oppend=0

        if self.IsEndHead(oppend):
            self.HeadEnd=oppend
            self.HeadBlock=block
            self.UpdateStatus()
            return self
        else:
            return self.Cons[oppend].Object.IsOppEndHead(self.Cons[oppend].ObjCon, block)

    def IsEndHead(self, end):
        if self.Cons[end].gap==True:
            return True
        if self.Cons[end].Object!=None:
            return not self.Cons[end].Object.IsEndAccessible(self.Cons[end].ObjCon)
        else:
            return True

    def OutOfService(self, event=None):
        """Toggles switch service status.

        If switch is in service, sends signal to take it out of
        service.  If switch is out of service, sends signal to put it
        back in service."""
        if self.outofservice==0:
            newoos='#t'
        else:
            newoos='#f'
        OutStr='(setOutOfService (Obj "'+self.name+'") '+newoos+')'
        self.master.SockWrite(OutStr)

    def ThrowSwitch(self, event=None):
        if self.switchpos==0:
            newpos='#t'
        else:
            newpos='#f'
        OutStr='(throwSwitch (Obj "'+self.name+'") '+newpos+')'
        self.master.SockWrite(OutStr)

    def ProcSexp(self, Psexp):
        if Psexp.tokens[0]=='debug-info':
            self.ShowDebugInfo(Psexp.tokens[2])
        elif Psexp.tokens[0]=='set':
            if Psexp.tokens[1][0]=='obj':
                if Psexp.tokens[2]=='switchpos':
                    self.SetSwitchpos(Psexp.tokens[3])
                elif Psexp.tokens[2]=='outofservice': #JYK
                    if Psexp.tokens[3]=='#f':
                        self.outofservice=0
                    else:
                        self.outofservice=1
                    self.UpdateStatus()
                elif Psexp.tokens[2]=='hardwarepresent':
                    if Psexp.tokens[3]=='#f':
                        self.offline=1
                    else:
                        self.offline=0
                    self.UpdateStatus()
                elif Psexp.tokens[2]=='hand':
                    self.SetHand(Psexp.tokens[3])
                elif Psexp.tokens[2]=='numcxn':
                    self.SetNumcxn(Psexp.tokens[3])
                elif Psexp.tokens[2]=='owner':
                    self.Owner=Psexp.tokens[3]
                elif Psexp.tokens[2]=='dname':
                    self.SetDName(Psexp.tokens[3])
                elif Psexp.tokens[2]=='debuginfo':
                    self.ShowDebugInfo(Psexp.tokens[3])
                elif Psexp.tokens[2]=='logicaldirection':
                    pass
                else:
                    self.master.logger.LogWarnMsg('S-exp "'+Psexp.sexp+'" unparsed by switch '+self.name)
                    self.master.logger.LogWarnMsg('Switch object variable type '+Psexp.tokens[2]+' unknown and ignored')
            elif Psexp.tokens[1][0]=='cxn':
    #            print Psexp.variable+'!'
                if Psexp.tokens[2]=='signal':
                    self.UpdateSignal(int(Psexp.tokens[1][2]), Psexp.tokens[3])
                    self.UpdateStatus()
                elif Psexp.tokens[2]=='object':
                    if Psexp.tokens[3]!='nil':
                        self.ConInfo(int(Psexp.tokens[1][2]), Psexp.tokens[3][1], int(Psexp.tokens[3][2]))
                elif Psexp.tokens[2]=='magic':
                    self.Cons[int(Psexp.tokens[1][2])].magic=Psexp.tokens[3] in ('#t', True)
                elif Psexp.tokens[2]=='gap':
                    self.Cons[int(Psexp.tokens[1][2])].SetGap(Psexp.tokens[3])
                else:
                    self.master.logger.LogWarnMsg('S-exp "'+Psexp.sexp+'" unparsed by switch '+self.name)
                    self.master.logger.LogWarnMsg('Unknown connection '+Psexp.tokens[2]+' for switch element')
        else:
            self.master.logger.LogWarnMsg('S-exp "'+Psexp.sexp+'" unparsed by switch '+self.name)
            self.master.logger.LogWarnMsg('Unknown object type: '+Psexp.tokens[1][0])

#### This section holds stuff for the graphical display functions ####
# The display builder calls this first
    def SetSwitchpos(self, switchpos):
        if switchpos in ("#f", 0):
            switchpos=0
        else:
            switchpos=1
        if self.switchpos!=switchpos:
            self.switchpos=switchpos
            self.RecalcHeadBlock()
            self.UpdateStatus()

    def RecalcHeadBlock(self):
        if self.Train != None:
            self.Train.HeadBlock.IsHeadBlock()
        if self.Cons[self.switchpos+1].Object != None and self.Cons[self.switchpos+1].Object.HeadBlock != None:
            self.Cons[self.switchpos+1].Object.HeadBlock.IsHeadBlock()
        

    def SetHand(self, hand):
        if hand in ('left', LEFTHAND):
            self.hand = LEFTHAND
        else:
            self.hand = RIGHTHAND

    def SetWidth(self, width):
        width=int(width)
        self.width=width

    def SetNumcxn(self, numcxn):
        self.numcxn=int(numcxn)

    def GState(self, connection):
        # Return status of connection ObjCon
##        return self.occstatus[ObjCon], self.actstatus[ObjCon]
        if connection==0 or self.switchpos+1==connection:
            return self.OccStatus, self.ActStatus, self.Train
        else:
            return UNOCC, INACC, None

    def FindColor(self, connection=None):
        if connection in (None, 0, self.switchpos+1) and self.ActStatus!=INACC:
            return self.Color
        else:
            return blkcolor[INACC][UNOCC]

    def FindLabelColor(self):
        if self.offline:
            return offlinecolor
        elif self.outofservice:
            return outofservicecolor
        else:
            return slabelcolor['bg']
        
class CompactSwitchDisplay:
    def __init__(self, switch, frame):

        self.Switch=switch
        self.Frame=frame

        self.LeftLabel=Label(self.Frame, text='0', bg=sigcolor[self.Switch.Cons[0].Signal])
        self.LeftLabel.pack(side=LEFT, padx=pad, pady=pad)
        self.NameButton=Button(self.Frame, command=self.Clicked, text=self.Switch.name, bg=throwbgcolor[self.Switch.switchpos], fg=throwtxcolor[self.Switch.switchpos], padx=0, pady=0, bd=0)
        self.NameButton.pack(side=LEFT, padx=pad, pady=pad)
        self.RightLabel=Label(self.Frame, text='1', bg=sigcolor[self.Switch.Cons[1].Signal])
        self.RightLabel.pack(side=LEFT, padx=pad, pady=pad)
        self.RRightLabel=Label(self.Frame, text='2', bg=sigcolor[self.Switch.Cons[2].Signal])
        self.RRightLabel.pack(side=LEFT, padx=pad, pady=pad)

        self.Number=self.Switch.AddDisplayObject(self)
        self.UpdateStatus()

    def Disconnect(self):
        self.Switch.DelDisplayObject(self)

    def Clicked(self, event=None):
        self.Switch.ThrowSwitch(event)

    def OutOfService(self, event=None):
        self.Switch.OutOfService(event)

    def UpdateStatus(self):
       
        self.NameButton.config(bg=throwbgcolor[self.Switch.switchpos], fg=throwtxcolor[self.Switch.switchpos])
        color0=self.Switch.SignalColor(0)
        color1=self.Switch.SignalColor(1)
        color2=self.Switch.SignalColor(2)
        self.LeftLabel.config(bg=color0)
        self.RightLabel.config(bg=color1)
        self.RightLabel.config(bg=color2)

class CompactSwitchDisplayWindow:
    def __init__(self, master):
        self.Master=master

        self.SwitchWindow=Toplevel(self.Master.root)
        self.SwitchWindow.title('Switch List')
        self.SwitchWindow.protocol("WM_DELETE_WINDOW", self.CloseWindow)
        self.SwitchWindow.resizable(0,0)
        self.SwitchWindow.transient(self.Master.root)

        self.SwitchDisplays=[]
        
        SlistKeys=self.Master.Slist.keys()
        SlistKeys.sort()
        switch=0
        row=0
        column=0
        while switch<len(SlistKeys):
            fm=Frame(self.SwitchWindow, relief='raised', borderwidth=2, bg='White')
            self.SwitchDisplays+=[CompactSwitchDisplay(self.Master.Slist[SlistKeys[switch]], fm)]
            fm.grid(row=row, column=column)
            switch=switch+1
            column=column+1
            if column==8:
                column=0
                row=row+1
                
    def CloseWindow(self, event=None):
        for SwitchDisplay in self.SwitchDisplays:
            SwitchDisplay.Disconnect()
        self.SwitchWindow.destroy()
        del self.Master.SwitchWindow
