from MiscTrack import *
import SwitchObj
import TrackObj

class CrossingObj(SwitchObj.SwitchObj):
    def __init__(self, master, name):
        SwitchObj.SwitchObj.__init__(self, master, name)
        self.type='crossing'
        self.expectedCxn = 4
        self.Cons=[ConObj(), ConObj(), ConObj(), ConObj()]

    def ObjType(self):
        return 'crossing'

    def SignalColor(self, end):
        if end not in (0, 1, 2, 3):
            print end, self.name
            return 'Purple'
        return sigcolor[self.Cons[end].Signal]

    def UpdateSignal(self, end, signal):
        if end in (0, 1, 2, 3):
            self.Cons[end].Signal=signal
        else:
            self.master.logger.LogWarnMsg('Unknown switch position: '+str(end)+' in switch '+self.name)

    def UpdateStatus(self, connect=None, callingobject=()):
        occ=self.OccStatus
        act=self.ActStatus
        train=self.Train
        color=self.Color
        if self.switchpos==0:
            if self.Cons[0].gap==False and self.Cons[0].Object!=None:
                occ, act, train=self.Cons[0].Object.GState(self.Cons[0].ObjCon)
                color=self.Cons[0].Object.FindColor(self.Cons[0].ObjCon)
            elif self.Cons[2].gap==False and self.Cons[2].Object!=None:
                occ, act, train=self.Cons[2].Object.GState(self.Cons[2].ObjCon)
                color=self.Cons[2].Object.FindColor(self.Cons[2].ObjCon)
        else:
            if self.Cons[1].gap==False and self.Cons[1].Object!=None:
                occ, act, train=self.Cons[1].Object.GState(self.Cons[1].ObjCon)
                color=self.Cons[1].Object.FindColor(self.Cons[1].ObjCon)
            elif self.Cons[3].gap==False and self.Cons[3].Object!=None:
                occ, act, train=self.Cons[3].Object.GState(self.Cons[3].ObjCon)
                color=self.Cons[3].Object.FindColor(self.Cons[3].ObjCon)

        if occ!=self.OccStatus or act!=self.ActStatus or train!=self.Train or color!=self.Color or connect==None:
            self.OccStatus=occ
            self.ActStatus=act
            self.Train=train
            self.Color=color
            for connum in  range(len(self.Cons)):
                if self.Cons[connum].Object not in callingobject and self.Cons[connum].Object != None and self.Cons[connum].gap==False:
                    self.Cons[connum].Object.UpdateStatus(self.Cons[connum].ObjCon, callingobject+(self,))

            self.UpdateDisplayObjects()

    def FindColor(self, connection=None):
        if connection==None or (connection in (0, 2) and self.switchpos==0) or (connection in (1, 3) and self.switchpos==1):
            return self.Color
        else:
            return blkcolor[INACC][UNOCC]

    def IsEndAccessible(self, end):
        if (end in (0, 2) and self.switchpos==1) or (end in (1, 3) and self.switchpos==0):
            return False
        else:
            return True

    def IsNotHead(self, block):
        if self.HeadBlock==block:
            self.HeadBlock=None
            self.HeadEnd=None
            self.UpdateStatus()

    def IsOppEndHead(self, end, block):
        oppend=(end+2)%4

        if self.IsEndHead(oppend):
            self.HeadEnd=oppend
            self.HeadBlock=block
            self.UpdateStatus()
            return self
        else:
            return self.Cons[oppend].Object.IsOppEndHead(self.Cons[oppend].ObjCon, block)

    def GState(self, connection):
        # Return status of connection ObjCon
##        return self.occstatus[ObjCon], self.actstatus[ObjCon]
        if connection==None or (connection in (0, 2) and self.switchpos==0) or (connection in (1, 3) and self.switchpos==1):
           return self.OccStatus, self.ActStatus, self.Train
        else:
            return UNOCC, INACC, None

    def RecalcHeadBlock(self):
        if self.Train != None:
            self.Train.HeadBlock.IsHeadBlock()
        for con in self.Cons:
            if con.Object != None and con.Object.HeadBlock != None:
                con.Object.HeadBlock.IsHeadBlock()

