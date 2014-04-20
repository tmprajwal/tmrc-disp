# Thomas O'Reilly, 2 March 2002
# TMRC System 3 display software switch object definitions

from MiscTrack import *
from Tkinter import *
import TrackObj

pad=0
throwbgcolor=['White', 'Black']
throwtxcolor=['Black', 'White']

class TurnTableObj(TrackObj.TrackObj):
    def __init__(self, master, name):
# Initialize base class
        TrackObj.TrackObj.__init__(self, master, name)

        self.type='turntable'
        self.trackEnd = -1
        self.currentTrack = -1
        self.outofservice=0 #JYK
        self.offline=0
        self.moving=False
        self.initialized=False
        #self.expectedCxn = 3
        #self.Cons=[ConObj(), ConObj(), ConObj()]

# These are things related to the graphical display process
        #self.card=None
        #self.orient=None
        #self.hand=LEFTHAND
        #self.Swing=False
        self.HeadBlock=None
        self.HeadEnd=None

        self.OccStatus=UNOCC
        self.ActStatus=ONLINE
        self.Train=None
        self.editing=False
        self.Color='White'

    def ObjType(self):
        return 'turntable'

    def SignalColor(self, end):
        if not self.initialized or end not in range(self.numTracks + 2):
            return 'Purple'
        return sigcolor[self.Cons[end].Signal]

    def UpdateSignal(self, end, signal):
        if not self.initialized:
            return
        if end in range(self.numTracks + 2):
            self.Cons[end].Signal=signal
        else:
            self.master.logger.LogWarnMsg('Unknown switch position: '+str(end)+' in switch '+self.name)

    """def CheckSwing(self, swing=None):
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
                        print 'In switchobj.py, CheckSwing(), "crossing" type not handled intelligently'"""
                             

    #def IsSwing(self):
    #    return self.Swing

    def UpdateStatus(self, connect=None, callingobject=()):
        if not self.initialized:
            return
        occ=self.OccStatus
        act=self.ActStatus
        train=self.Train
        color=self.Color
        trackCon=self.Cons[self.numTracks + self.trackEnd]
        if trackCon.Object != None:
            occ, act, train=trackCon.Object.GState(trackCon.ObjCon)
            color=trackCon.Object.FindColor(trackCon.ObjCon)
        if self.moving:
            act=INACC
        
        if occ!=self.OccStatus or act!=self.ActStatus or train!=self.Train or color!=self.Color or connect==None:
            self.OccStatus=occ
            self.ActStatus=act
            self.Train=train
            self.Color=color
            
            for connum in range(len(self.Cons)):
                if self.Cons[connum].Object not in callingobject and self.Cons[connum].Object != None and self.Cons[connum].gap==False:
                    self.Cons[connum].Object.UpdateStatus(self.Cons[connum].ObjCon, callingobject+(self,))

            self.UpdateDisplayObjects()
            #print self.DisplayObjects

    def IsEndAccessible(self, end):
        if not self.initialized or self.moving:
            return False
        if end == self.currentTrack or (end == self.numTracks + self.trackEnd and self.trackEnd >= 0):
            return True
        return False

    def IsNotHead(self, block):
        if self.HeadBlock==block:
            self.HeadBlock=None
            self.HeadEnd=None
            self.UpdateStatus()

    def IsOppEndHead(self, end, block):
        if not self.initialized:
            return None
        if end < self.numTracks:
            oppend=self.numTracks + self.trackEnd
        else:
            oppend=self.currentTrack

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

    def Rotate(self, end, track, event=None):
        OutStr='(rotate (Obj "'+self.name+'") ' + str(end) + ' ' + str(track) +')'
        self.master.SockWrite(OutStr)

    def RotateToClosest(self, track, event=None):
        OutStr='(rotateToClosest (Obj "'+self.name+'") ' + str(track) +')'
        self.master.SockWrite(OutStr)

    def ProcSexp(self, Psexp):
        if Psexp.tokens[0]=='debug-info':
            self.ShowDebugInfo(Psexp.tokens[2])
        elif Psexp.tokens[0]=='set':
            if Psexp.tokens[1][0]=='obj':
                if Psexp.tokens[2]=='turntablepos':
                    self.SetTurnTablepos(Psexp.tokens[3])
                elif Psexp.tokens[2]=='moving':
                    self.SetMoving(Psexp.tokens[3])
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
    def SetTurnTablepos(self, pos):
        trackEnd = int(pos[0])
        currentTrack = int(pos[1])
        if self.trackEnd!=trackEnd or self.currentTrack!=currentTrack:
            self.trackEnd=trackEnd
            self.currentTrack=currentTrack
            if not self.initialized:
                return
            if self.Cons[currentTrack].Object != None and self.Cons[currentTrack].Object.HeadBlock != None:
                self.Cons[currentTrack].Object.HeadBlock.IsHeadBlock()
            if self.Cons[trackEnd+self.numTracks].Object != None and self.Cons[trackEnd+self.numTracks].Object.HeadBlock != None:
                self.Cons[trackEnd+self.numTracks].Object.HeadBlock.IsHeadBlock()
            self.UpdateStatus()

    def SetMoving(self, mov):
        if mov == '#f':
            moving = False
        else:
            moving = True
        if moving != self.moving:
            self.moving=moving
            if not self.initialized:
                return
            if self.Train != None:
                self.Train.HeadBlock.IsHeadBlock()
            self.UpdateStatus()

    def SetWidth(self, width):
        width=int(width)
        self.width=width

    def SetNumcxn(self, numcxn):
        self.numTracks=int(numcxn) - 2
        self.Cons=[ConObj() for x in range(int(numcxn))]
        self.initialized=True
        #self.UpdateStatus()
#        self.numcxn=int(numcxn)

    def GState(self, connection):
        # Return status of connection ObjCon
##        return self.occstatus[ObjCon], self.actstatus[ObjCon]
        if connection==self.currentTrack or connection==self.trackEnd + self.numTracks:
            return self.OccStatus, self.ActStatus, self.Train
        else:
            return UNOCC, INACC, None

    def FindColor(self, connection=None):
        if self.offline:
            return offlinecolor
        elif self.outofservice:
            return outofservicecolor
        if connection in (None, self.currentTrack, self.trackEnd + self.numTracks) and self.ActStatus!=INACC:
            return self.Color
        else:
            return blkcolor[INACC][UNOCC]

    def FindRimColor(self):
        if self.offline or self.moving:
            return offlinecolor
        elif self.outofservice:
            return outofservicecolor
        else:
            return slabelcolor['bg']
        
