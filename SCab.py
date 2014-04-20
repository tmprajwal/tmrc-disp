# This class defines the functions associated with SCab windows.  It includes
# an initialiaztion function and callbacks associated with SCab widgets
'''
Modified by Prajwal Mohanmurthy (prajwal@mohanmurthy.com)
'''

import time
from Tkinter import *

MAXSPEED=100

from MiscTrack import *
dirlabel={1:'Eastbound', 0:'Westbound', None: 'Nowherebound'}
dircolor={0:'#FFBBBB', 1:'#BBFFBB'}
paddingY=0
paddingX=0

class LabelButton(Label):
    def __init__(self, frame, Command1=None, Command2=None, Command3=None):
        Label.__init__(self, frame)
        self.Command1=Command1
        self.Command2=Command2
        self.Command3=Command3
        self.inside=0

        self.SetActive()
        self.bgoriginal=self.cget('bg')

        for eventname in ('<Enter>', '<Leave>', '<Button-1>', '<Button-2>',
                      '<Button-3>', '<ButtonRelease-1>', '<ButtonRelease-2>',
                      '<ButtonRelease-3>'):
            self.bind(eventname, lambda event=None, name=eventname: self.Action(name))
        
    def SetActive(self):
        self.active=1
        self.config(fg='black')

    def SetInactive(self):
        self.active=0
        self.config(fg='grey')

    def Action(self, event):
        if self.active==1:
            if event=='<Enter>':
                self.configure(relief=RAISED)
                self.inside=1
            elif event=='<Leave>':
                self.configure(relief=FLAT, bg=self.bgoriginal)
                self.inside=0
            elif event == '<Button-1>' and self.Command1!=None:
                self.configure(bg='white')
            elif event == '<Button-2>' and self.Command2!=None:
                self.configure(bg='white')
            elif event == '<Button-3>' and self.Command3!=None:
                self.configure(bg='white')
            elif event == '<ButtonRelease-1>' and self.Command1!=None and self.inside==1:
                self.configure(bg=self.bgoriginal)
                self.Command1()
            elif event == '<ButtonRelease-2>' and self.Command2!=None and self.inside==1:
                self.configure(bg=self.bgoriginal)
                self.Command2()
            elif event == '<ButtonRelease-3>' and self.Command3!=None and self.inside==1:
                self.configure(bg=self.bgoriginal)
                self.Command3()

class Train:
    def __init__(self, master, name, owned):

        self.Type='Train'
        self.Speed=0
        self.ReqSpeed=0
        self.Direction=0
        self.Heading=1
        self.Feedback=0
        self.Signal='unknown'
        self.Tracks=[]
        self.Advance=[]
        self.HeadBlock=None
        self.Block=None
        
        self.owned=owned
        self.Master=master
        self.HCab=None
        self.Name=name

        self.SCabs=[]

        self.Commands={'Stop':self.Stop,
                       'Reverse':self.Reverse,
                       'CallOn':self.CallOn,
                       'DropBehind':self.DropBehind,
                       'StealAhead':self.StealAhead,
                       'DropOut':self.DropOut,
                       'Coupler':self.Coupler,
                       'Controls':self.Controls}

        self.ServerCommands={'speed':self.SetSpeed,
                             'reqspeed': self.SetReqSpeed,
                             'direction': self.SetDirection,
                             'feedback': self.SetFeedback,
                             'signal': self.SetSignal,
                             'tracks': self.SetTracks,
                             'advance': self.SetAdvance}
        
                       
    def TellInfo(self, info):
        return getattr(self, info)

    def ProcSexp(self, Psexp):
        """Process parsed s-expressions

        Looks at parsed s-expressions sent from Picker.py
        and calls the appropriate functions."""
        if Psexp.tokens[2] in self.ServerCommands.keys():
            self.ServerCommands[Psexp.tokens[2]](Psexp.tokens[3])
        else:
            print 'Unparsed S-exp: '+Psexp.sexp
            print 'SCab object variable type "'+Psexp.tokens[2]+'" unknown and ignored'

    def UpdateSCabs(self, update=None):
        for scab in self.SCabs:
            scab.UpdateStatus(update)

# Change displayed speed in response to server data
    def SetSpeed(self, speed):
        self.Speed=int(speed)
        self.UpdateSCabs('Speed')

# Change displayed requested speed in response to server data
    def SetReqSpeed(self, reqspeed):
        self.ReqSpeed=int(reqspeed)
        self.UpdateSCabs('ReqSpeed')

# Change feedback value in response to server data
    def SetFeedback(self, feedback):
        self.Feedback=int(feedback)
        self.UpdateSCabs('Feedback')

    def SetDirection(self, direction=None):
        self.SetHeading()

# Change direction in response to server messages
    def SetHeading(self, heading=None):
        if self.HeadBlock!=None:
            blockdir=self.HeadBlock.direction
            direction=self.HeadBlock.LogicalDirection
            if direction in ('east', 'west'):
                if blockdir==0:
                    if direction=='east':
                        self.Heading=1
                    elif direction=='west':
                        self.Heading=0
                elif blockdir==1:
                    if direction=='east':
                        self.Heading=0
                    elif direction=='west':
                        self.Heading=1
                else:
                    self.Heading=None
            elif direction=='easteast':
                self.Heading=1
            elif direction=='westwest':
                self.Heading=0
            else:
                self.Heading=None

##            print self.Heading, blockdir, direction
        self.UpdateSCabs('Heading')
        
# Change signal in response to server messages
    def SetSignal(self, signal):
        self.Signal=signal
        self.UpdateSCabs('Signal')    

# Set owned tracks
    def SetTracks(self, tracks=None):
        blocks=self.Master.Blist.keys()
        for track in self.Tracks:
            if track not in tracks[1:] and track[1] in blocks:
                self.Master.Blist[track[1]].SetTrain(None)
        for track in tracks[1:]:
            if track not in self.Tracks and track[1] in blocks:
                self.Master.Blist[track[1]].SetTrain(self)
        self.Tracks=tracks[1:]
        self.UpdateHeadBlock()

# Set advance blocks
    def SetAdvance(self, advance=None):
        self.advance=advance[1:]
        self.UpdateHeadBlock()

    def UpdateHeadBlock(self):
        if len(self.Tracks) != 0:
            newheadblockname = self.Tracks[-1][1]
            NewHeadBlock=self.Master.Blist[self.Tracks[-1][1]]
            if NewHeadBlock!=self.HeadBlock and 'UHB' not in dir(self):
                self.UHB=True
                if self.HeadBlock!=None:
                    self.HeadBlock.IsHeadBlock(False)
                    self.HeadBlock.DelDisplayObject(self)
                    
                self.HeadBlock=NewHeadBlock
                self.HeadBlock.IsHeadBlock(True)
                self.HeadBlock.AddDisplayObject(self)
                self.Block=self.HeadBlock.DName
                del self.UHB
        else:
            if self.HeadBlock!=None:
                    self.HeadBlock.IsHeadBlock(False)
                    self.HeadBlock.DelDisplayObject(self)
            self.HeadBlock = None

        self.SetDirection()
        self.UpdateSCabs('Block')

    def UpdateStatus(self, update=None):
        self.UpdateHeadBlock()

    def SetDName(self, dname):
        self.Block=dname
        self.UpdateSCabs('Block')

    def Command(self, command):
        if command in self.Commands.keys():
            self.Commands[command]()
        else:
            print 'Error processing Train command'

    def Controls(self, event=None):
        self.Master.SCabManager.AddControls(self)

    def DropOut(self, event=None):
        """Drop out the train

        Sends a message to the server asking it to drop out
        the current train.

        Format: (delTrain (obj "TrainName")) """
        OutStr='(delTrain (obj "'+self.Name+'"))'
        self.Master.SockWrite(OutStr)
    
    def Reverse(self, event=None):
        """Reverse the current train

        Tells the server to reverse the current train.

        Format: (reverse (obj "TrainName")) """
        OutStr='(reverse (obj "'+self.Name+'"))'
        self.Master.SockWrite(OutStr)

    def Stop(self, event=None):
        """Stop the current train

        Tells the server to set the speed of the current
        train to zero.

        Format: (speed (obj "TrainName") 0) """
        OutStr='(speed (obj "'+self.Name+'") 0)'
        self.Master.SockWrite(OutStr)


    def CallOn(self, event=None):
        """Call on for the current train

        Sends the server a call on message for the current
        train.

        Format: (callOn (obj "TrainName")) """
        OutStr='(callOn (obj "'+self.Name+'"))'
        self.Master.SockWrite(OutStr)

    def DropBehind(self, event=None):
        """Drop the last block of a train

        Sends the server a request to drop the end of the
        train.  This might be necessary due to occupancy
        problems or dropped cabeese.

        Format: (dropBehind (obj "TrainName")) """
        OutStr='(dropBehind (obj "'+self.Name+'"))'
        self.Master.SockWrite(OutStr)

    def StealAhead(self, event=None):
        """Take ownership of the next block ahead

        Sends the server a request to assign the next block
        to the current train.  This might be needed due to
        occupancy related problems, or to couple to
        occupying cars in the next block.

        Format: (stealAhead (obj "TrainName")) """
        OutStr='(stealAhead (obj "'+self.Name+'"))'
        self.Master.SockWrite(OutStr)

    def FindPath(self, event=None):
        """Start the path finding process

        Tells the display builder to enter pathfinder mode.
        Eventually, a block name should be returned to the
        SCab object."""
        if self.Master.DB.mode=='active':
            self.Master.DB.PathFind(self.Name)
            
    def Coupler(self, event=None):
        '''
        Helps couple to cabs in next block
        '''
        self.StealAhead(self)
        time.sleep(5)
        self.Reverse(self)
        OutStr='(speed (obj "'+self.Name+'") 30)'
        self.Master.SockWrite(OutStr)
        print('DONE')

    def SetDestination(self, block):
        """Report destination block

        Used by the display builder to tell the SCab object
        the desination for the path finder routine.  Calls
        the command to the server to find the path.

        Format: (findpath (obj "TrainName") (obj "Block"))"""
        OutStr='(findpath (obj "'+self.Name+'") (obj "'+block+'"))'
        self.Master.SockWrite(OutStr)

    def ReqSpeedChange(self, reqspeed):
        OutStr='(speed (obj "'+self.Name+'") '+str(reqspeed)+')'
        self.Master.SockWrite(OutStr)
        
    def NewHCab(self, newhcab):
        if newhcab!=None:
            self.HCab=newhcab.Name
        else:
            self.HCab=None
        self.UpdateSCabs('HCab')

    def SetHCab(self, newhcab):
        if self.HCab!=newhcab:
            if self.HCab!=None:
                OutStr='(releasecab (Obj "'+str(self.HCab)+'"))'
                self.Master.SockWrite(OutStr)
            if newhcab!='None':
                # Message format: (assigncab (Obj "Cab") (Obj "TrainName"))
                OutStr='(assigncab (Obj "'+newhcab+'") (Obj "'+self.Name+'"))'
                self.Master.SockWrite(OutStr)

    def AddSCab(self, scab):
        self.SCabs+=[scab]

    def DeleteSCab(self, scab):
        if scab in self.SCabs:
            index=self.SCabs.index(scab)
            del self.SCabs[index]

    def Delete(self, event=None):
        """Delete the current train

        Deletes the current train and associated SCab
        windows in response to message from the server."""
        if self.HeadBlock!=None:
            self.HeadBlock.IsHeadBlock(False)
            self.HeadBlock.DelDisplayObject(self)
        self.Master.SCabManager.DeleteTrain(self)

        blocks=self.Master.Blist.keys()
        for track in self.Tracks:
            if track[1] in blocks:
                self.Master.Blist[track[1]].SetTrain(None)

        del self.Master.TrainList[self.Name]

class SCab:
    """Superclass for all types of SCab Control display windows"""
    def __init__(self, master, manager, train):
        self.Displayed=False
        self.Master=master
        self.Manager=manager
        self.Train=train
        self.Train.AddSCab(self)
        self.Type='unknown'

        self.Name='None'
        self.HCab='None'
        self.Block='None'
        self.Heading='None'
        self.Signal='Unknown'

    def SetTrain(self, train):
        if self.Train!=None:
            self.Train.DeleteSCab(self)
        self.Train=train
        if self.Train!=None:
            self.Train.AddSCab(self)
        self.UpdateStatus()

    def Display(self):
        pass

    def UpdateStatus(self, update=None):
        pass

    def Undisplay(self):
        pass

class SCabWindow(SCab):
    def Display(self, frame):
        self.SCab=frame
        self.HCabWin=None
        
        if self.Train!=None:
            self.Name=self.Train.TellInfo('Name')
            self.HCab=self.Train.TellInfo('HCab')
            self.Block=self.Train.TellInfo('Block')
            self.Heading=self.Train.TellInfo('Heading')
            self.Signal=self.Train.TellInfo('Signal')
            self.Speed=self.Train.TellInfo('Speed')
            self.ReqSpeed=self.Train.TellInfo('ReqSpeed')
        else:
            self.Name='None'
            self.HCab=None
            self.Block='None'
            self.Heading='None'
            self.Signal='Unknown'
            self.Speed=0
            self.ReqSpeed=0
            
        topframe=Frame(self.SCab)
        topframe.grid(row=0, column=0, columnspan=2)
        
        Label(topframe, text='name:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=0, column=0, padx=0, pady=paddingY)
        self.NameLabel=Label(topframe, text=self.Name, font=('Arial', 16, 'bold'), anchor=SW, width=10)
        self.NameLabel.grid(row=0, column=1, padx=0, pady=paddingY, sticky=W)
        
        Label(topframe, text='block:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=1, column=0, padx=0, pady=paddingY)
        self.BlockLabel=Label(topframe, text=self.Block, font=('Arial', 12, 'bold'), anchor=SW)
        self.BlockLabel.grid(row=1, column=1, pady=paddingY, sticky=W)

        Label(topframe, text='heading:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=2, column=0, padx=0, pady=paddingY)
        self.HeadingLabel=Label(topframe, text=dirlabel[self.Heading], font=('Arial', 12, 'bold'), anchor=SW)
        self.HeadingLabel.grid(row=2, column=1, pady=paddingY, sticky=W)

        leftframe=Frame(self.SCab)
        leftframe.grid(row=1, column=0)

        bigframe=Frame(leftframe)
        bigframe.grid(row=0, column=0)

        self.RevBut=LabelButton(bigframe, lambda event=None, name='Reverse': self.Action(name))
        self.RevBut.configure(text='Reverse')

        self.StopBut=LabelButton(bigframe, lambda event=None, name='Stop': self.Action(name))
        self.StopBut.configure(text='Stop Train')

        self.CallOnBut=LabelButton(bigframe, lambda event=None, name='CallOn': self.Action(name))
        self.CallOnBut.configure(text='Call On')

        count=0
        for button in (self.RevBut, self.StopBut, self.CallOnBut):
            button.configure(font=('Arial', 12), width=9, anchor=E, bd=1, relief=FLAT)
            button.grid(row=count, sticky=NE, pady=5)
            count+=1

        smframe=Frame(leftframe)
        smframe.grid(row=1, column=0)

        self.DropBut=LabelButton(smframe, lambda event=None, name='DropOut': self.Action(name))
        self.DropBut.configure(text='Drop Out')

        self.StealBut=LabelButton(smframe, lambda event=None, name='StealAhead': self.Action(name))
        self.StealBut.configure(text='Steal Ahead')

        self.DropBehindBut=LabelButton(smframe, lambda event=None, name='DropBehind': self.Action(name))
        self.DropBehindBut.configure(text='Drop Behind')

        self.HCabBut=LabelButton(smframe, self.NewHCab)
        self.HCabBut.configure(text='HCab/'+str(self.HCab))

        self.PFBut=LabelButton(smframe, lambda event=None, name='FindPath': self.Action(name))
        self.PFBut.configure(text='Find Path')
        
        self.CoBut=LabelButton(smframe, lambda event=None, name='Coupler': self.Action(name))
        self.CoBut.configure(text='Coupler')

        count=0
        for button in (self.DropBut, self.StealBut, self.DropBehindBut, self.HCabBut, self.PFBut, self.CoBut):
            button.configure(font=('Arial', 10), width=11, anchor=E, bd=1, relief=FLAT)
            button.grid(row=count, sticky=E)
            count+=1

        rightframe=Frame(self.SCab)
        rightframe.grid(row=1, column=1, columnspan=2, padx=4)

        self.SignalLabel=Label(rightframe, image=self.Master.sigpic[self.Signal])
        self.SignalLabel.grid(row=0, column=0)

        self.SpeedLabel=Label(rightframe, text='Speed: '+str(self.Speed), font=('Arial', 12, 'bold'), width=10)
        self.SpeedLabel.grid(row=1, column=0)
    
        self.SpeedScale=Scale(rightframe, orient=VERTICAL, length=100, from_=MAXSPEED, to=0, tickinterval=0)
        self.SpeedScale.grid(row=2, column=0)

        if self.HCab!=None:
            self.SpeedScale.configure(state='disabled', fg='grey')

        self.SpeedScale.set(self.ReqSpeed)
        self.ReqSpeedChange()
        
        for key in ('Q', 'q', 'E', 'e', 'a', 'A', 'd', 'D', 's', 'S', 'c', 'C', 'r', 'R'):
            self.SCab.bind(key, self.SpdKeyControl)

        self.Displayed=True

    def SpdKeyControl(self, event):
        key = event.keysym.lower()
        if key in 'ad':
            roundoff=5
            speed=self.SpeedScale.get()
            speed=speed-(speed%roundoff)
            if key == 'a':
                speed+=roundoff
            elif key == 'd':
                speed-=roundoff
            self.SpeedScale.set(speed)
        elif key in 'qe':
            speed=self.SpeedScale.get()
            if key == 'q':
                speed+=1
            else:
                speed-=1
            self.SpeedScale.set(speed)
        elif key in 's' and self.Train!=None:
            self.Train.Stop()
        elif key == 'r' and self.Train!=None:
            self.Train.Reverse()
        elif key == 'c' and self.Train!=None:
            self.Train.CallOn()
        else:
            print event, event.type, dir(event)
            print event.keysym, event.keycode, event.keysym_num

    def UpdateStatus(self, update=None):
        if self.Displayed==True:
            if self.Train!=None:
                if update in ('Speed', None):
                    speed=self.Train.TellInfo('Speed')
                    if speed!=self.Speed:
                        self.Speed=speed
                        self.SpeedLabel.configure(text='Speed: '+str(self.Speed))

                if update in ('ReqSpeed', None):
                    reqspeed=self.Train.TellInfo('ReqSpeed')
                    if reqspeed!=self.ReqSpeed:
                        self.ReqSpeed=reqspeed
                        self.SpeedScale.set(reqspeed)

                if update in ('Block', None):
                    block=self.Train.TellInfo('Block')
                    if block!=self.Block:
                        self.Block=block
                        self.BlockLabel.configure(text=self.Block)

                if update in ('Signal', None):
                    signal=self.Train.TellInfo('Signal')
                    if signal!=self.Signal:
                        self.Signal=signal
                        self.SignalLabel.configure(image=self.Master.sigpic[self.Signal])

                if update in ('Heading', None):
                    heading=self.Train.TellInfo('Heading')
                    if heading!=self.Heading:
                        self.Heading=heading
                        self.HeadingLabel.configure(text=dirlabel[self.Heading])

                if update in ('Name', None):
                    name=self.Train.TellInfo('Name')
                    if name!=self.Name:
                        self.Name=name
                        self.NameLabel.configure(text=self.Name)

                if update in ('HCab', None):
                    hcab=self.Train.TellInfo('HCab')
                    if hcab!=self.HCab:
                        self.HCab=hcab
                        self.HCabBut.configure(text='HCab/'+str(self.HCab))
                    if self.HCab==None:
                        self.SpeedScale.configure(state='normal', fg='black')
                    else:
                        self.SpeedScale.configure(state='disabled', fg='grey')

            else:
                self.Name='None'
                self.HCab='None'
                self.Block='None'
                self.Heading='None'
                self.Signal='Unknown'
                self.Speed=0
                self.SpeedLabel.configure(text='Speed: '+str(self.Speed))
                self.BlockLabel.configure(text=self.Block)
                self.SignalLabel.configure(image=self.Master.sigpic[self.Signal])
                self.HeadingLabel.configure(text=dirlabel[self.Heading])
                self.NameLabel.configure(text=self.Name)
                self.HCabBut.configure(text='HCab/'+self.HCab)

    def Undisplay(self, event=None):
        if self.Train!=None:
            self.Train.DeleteSCab(self)
        self.SCab.destroy()

    def Action(self, action):
        if self.Train!=None:
            self.Train.Command(action)

    def ReqSpeedChange(self, event=None):
        delay=100 # Speed update delay in milliseconds
        if self.ReqSpeed!=self.SpeedScale.get() and self.HCab in ('None', None):
            self.Train.ReqSpeedChange(self.SpeedScale.get())

        self.SCab.after(delay, self.ReqSpeedChange)

    def NewHCab(self, event=None):
        if self.HCabWin==None:
            self.HCabWin=Toplevel(self.Master.root)
            self.HCabWin.resizable(0,0)
            self.HCabWin.protocol("WM_DELETE_WINDOW", self.SetHCab)
            self.HCabWin.title('Assign HCab')
            self.HCabWin.transient(self.Master.root)
            self.NewHCab=StringVar()
            self.NewHCab.set(self.HCab)
            Radiobutton(self.HCabWin, text='No HCab', value='None', variable=self.NewHCab).pack(side=TOP)
            HCabs=self.Master.HCabList.keys()
            HCabs.sort()
            for HCab in HCabs:
                if self.Master.HCabList[HCab].Owner==None or self.Master.HCabList[HCab].Owner==self.Train:
                    Radiobutton(self.HCabWin, text=str(HCab), value=HCab, variable=self.NewHCab).pack(side=TOP)
            Button(self.HCabWin, text='Assign HCab', command=self.SetHCab, width=12).pack(side=TOP)

    def SetHCab(self, event=None):
        newhcab=self.NewHCab.get()
        self.Train.SetHCab(newhcab)
        self.HCabWin.destroy()
        self.HCabWin=None

class SCabWindowShort(SCabWindow):
    def Display(self, frame):
        self.SCab=frame
        self.HCabWin=None
        
        if self.Train!=None:
            self.Name=self.Train.TellInfo('Name')
            self.HCab=self.Train.TellInfo('HCab')
            self.Block=self.Train.TellInfo('Block')
            self.Heading=self.Train.TellInfo('Heading')
            self.Signal=self.Train.TellInfo('Signal')
            self.Speed=self.Train.TellInfo('Speed')
            self.ReqSpeed=self.Train.TellInfo('ReqSpeed')
        else:
            self.Name='None'
            self.HCab=None
            self.Block='None'
            self.Heading='None'
            self.Signal='Unknown'
            self.Speed=0
            self.ReqSpeed=0
            
        topframe=Frame(self.SCab)
        topframe.grid(row=0, column=0, columnspan=2)
        
        Label(topframe, text='name:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=0, column=0, padx=0, pady=paddingY)
        self.NameLabel=Label(topframe, text=self.Name, font=('Arial', 16, 'bold'), anchor=SW, width=10)
        self.NameLabel.grid(row=0, column=1, padx=0, pady=paddingY, sticky=W)
        
        Label(topframe, text='block:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=1, column=0, padx=0, pady=paddingY)
        self.BlockLabel=Label(topframe, text=self.Block, font=('Arial', 12, 'bold'), anchor=SW)
        self.BlockLabel.grid(row=1, column=1, pady=paddingY, sticky=W)

        Label(topframe, text='heading:', font=('Arial', 10, 'bold'), anchor=SE, width=7).grid(row=2, column=0, padx=0, pady=paddingY)
        self.HeadingLabel=Label(topframe, text=dirlabel[self.Heading], font=('Arial', 12, 'bold'), anchor=SW)
        self.HeadingLabel.grid(row=2, column=1, pady=paddingY, sticky=W)

        leftframe=Frame(self.SCab)
        leftframe.grid(row=1, column=0)

        self.RevBut=LabelButton(leftframe, lambda event=None, name='Reverse': self.Action(name))
        self.RevBut.configure(text='Reverse')

        self.StopBut=LabelButton(leftframe, lambda event=None, name='Stop': self.Action(name))
        self.StopBut.configure(text='Stop Train')

        self.CallOnBut=LabelButton(leftframe, lambda event=None, name='CallOn': self.Action(name))
        self.CallOnBut.configure(text='Call On')

        count=0
        for button in (self.RevBut, self.StopBut, self.CallOnBut):
            button.configure(font=('Arial', 12), width=9, anchor=E, bd=1, relief=FLAT)
            button.grid(row=count, sticky=NE, pady=5)
            count+=1

        scaleframe=Frame(self.SCab)
        scaleframe.grid(row=0, column=2, rowspan=2)

        self.SpeedScale=Scale(scaleframe, orient=VERTICAL, length=100, from_=MAXSPEED, to=0, tickinterval=0)
        self.SpeedScale.pack()

        smframe=Frame(self.SCab)
        smframe.grid(row=0, column=3, rowspan=2)

        self.DropBut=LabelButton(smframe, lambda event=None, name='DropOut': self.Action(name))
        self.DropBut.configure(text='Drop Out')

        self.StealBut=LabelButton(smframe, lambda event=None, name='StealAhead': self.Action(name))
        self.StealBut.configure(text='Steal Ahead')

        self.DropBehindBut=LabelButton(smframe, lambda event=None, name='DropBehind': self.Action(name))
        self.DropBehindBut.configure(text='Drop Behind')

        self.HCabBut=LabelButton(smframe, self.NewHCab)
        self.HCabBut.configure(text='HCab/'+str(self.HCab))

        self.PFBut=LabelButton(smframe, lambda event=None, name='FindPath': self.Action(name))
        self.PFBut.configure(text='Find Path')
        
        self.CoBut=LabelButton(smframe, lambda event=None, name='Coupler': self.Action(name))
        self.CoBut.configure(text='Coupler')

        count=0
        for button in (self.DropBut, self.StealBut, self.DropBehindBut, self.HCabBut, self.PFBut, self.CoBut):
            button.configure(font=('Arial', 10), width=11, anchor=E, bd=1, relief=FLAT)
            button.grid(row=count, sticky=E)
            count+=1

        rightframe=Frame(self.SCab)
        rightframe.grid(row=1, column=1, columnspan=1, padx=4)

        self.SignalLabel=Label(rightframe, image=self.Master.sigpic[self.Signal])
        self.SignalLabel.grid(row=0, column=0)

        self.SpeedLabel=Label(rightframe, text='Speed: '+str(self.Speed), font=('Arial', 12, 'bold'), width=10)
        self.SpeedLabel.grid(row=1, column=0)
    
        if self.HCab!=None:
            self.SpeedScale.configure(state='disabled', fg='grey')

        self.SpeedScale.set(self.ReqSpeed)
        self.ReqSpeedChange()
        
        for key in ('Q', 'q', 'E', 'e', 'a', 'A', 'd', 'D', 's', 'S', 'c', 'C', 'r', 'R'):
            self.SCab.bind(key, self.SpdKeyControl)

        self.Displayed=True



class SCabSummary(SCab):
    def Display(self, frame):
        self.SCab=frame

        if self.Train!=None:
            self.Name=self.Train.TellInfo('Name')
            self.HCab=self.Train.TellInfo('HCab')
            nametext=self.Name+'/'+str(self.HCab)
            self.Block=self.Train.TellInfo('Block')
            self.Heading=self.Train.TellInfo('Heading')
            self.Signal=self.Train.TellInfo('Signal')
            self.Speed=self.Train.TellInfo('Speed')
        else:
            self.Name='None'
            self.HCab='None'
            nametext=self.Name+'/'+self.HCab
            self.Block='None'
            self.Heading='None'
            self.Signal='Unknown'
            self.Speed='None'

        self.CommBut=LabelButton(self.SCab, lambda event=None, name='Controls': self.Action(name))
        self.CommBut.configure(text=nametext, width=10, anchor=W, padx=5)
        self.BlockLabel=Label(self.SCab, text=self.Block, width=6, anchor=W)
        self.HeadingLabel=Label(self.SCab, text=dirlabel[self.Heading], width=9, anchor=W)
        self.SignalLabel=Label(self.SCab, image=self.Master.sigpicsmall[self.Signal], anchor=W)
        self.SpeedLabel=Label(self.SCab, text=str(self.Speed), width=6, anchor=W)
        
        self.RevBut=LabelButton(self.SCab, lambda event=None, name='Reverse': self.Action(name))
        self.RevBut.configure(text='Reverse', anchor=W)
        self.StopBut=LabelButton(self.SCab, lambda event=None, name='Stop': self.Action(name)) 
        self.StopBut.configure(text='Stop', anchor=W)
        self.DropBut=LabelButton(self.SCab, lambda event=None, name='DropOut': self.Action(name))
        self.DropBut.configure(text='Drop Out', anchor=W, padx=5)
        for widget in (self.SignalLabel, self.CommBut, self.BlockLabel, self.SpeedLabel, self.HeadingLabel, self.RevBut, self.StopBut, self.DropBut):
            widget.pack(side=LEFT)
        self.Displayed=True

    def UpdateStatus(self, update=None):
        if self.Displayed==True:
            if update in ('Speed', None):
                speed=self.Train.TellInfo('Speed')
                if speed!=self.Speed:
                    self.Speed=speed
                    self.SpeedLabel.configure(text=str(self.Speed))

            if update in ('Block', None):
                block=self.Train.TellInfo('Block')
                if block!=self.Block:
                    self.Block=block
                    self.BlockLabel.configure(text=self.Block)

            if update in ('Signal', None):
                signal=self.Train.TellInfo('Signal')
                if signal!=self.Signal:
                    self.Signal=signal
                    self.SignalLabel.configure(image=self.Master.sigpicsmall[self.Signal])

            if update in ('Heading', None):
                heading=self.Train.TellInfo('Heading')
                if heading!=self.Heading:
                    self.Heading=heading
                    self.HeadingLabel.configure(text=dirlabel[self.Heading])

            if update in ('Name', 'HCab', None):
                flag=False
                hcab=self.Train.TellInfo('HCab')
                if hcab!=self.HCab:
                    self.HCab=str(hcab)
                    flag=True
                name=self.Train.TellInfo('Name')
                if name!=self.Name:
                    self.Name=name
                    flag=True
                if flag:
                    self.CommBut.configure(text=self.Name+'/'+self.HCab)

    def Undisplay(self, event=None):
        if self.Train!=None:
            self.Train.DeleteSCab(self)
        self.SCab.destroy()

    def Action(self, action):
        if self.Train!=None:
            self.Train.Command(action)

class SCabSummarySmall(SCabSummary):
    def Display(self, frame):
        self.SCab=frame

        if self.Train!=None:
            self.Name=self.Train.TellInfo('Name')
            self.HCab=self.Train.TellInfo('HCab')
            nametext=self.Name+'/'+str(self.HCab)
            self.Block=self.Train.TellInfo('Block')
            self.Heading=self.Train.TellInfo('Heading')
            self.Signal=self.Train.TellInfo('Signal')
            self.Speed=self.Train.TellInfo('Speed')
        else:
            self.Name='None'
            self.HCab='None'
            nametext=self.Name+'/'+self.HCab
            self.Block='None'
            self.Heading='None'
            self.Signal='Unknown'
            self.Speed='None'

        self.CommBut=LabelButton(self.SCab, lambda event=None, name='Controls': self.Action(name))
        self.CommBut.configure(text=nametext, width=10, anchor=W, padx=5)
        self.BlockLabel=Label(self.SCab, text=self.Block, width=6, anchor=W)
        self.HeadingLabel=Label(self.SCab, text=dirlabel[self.Heading], width=9, anchor=W)
        self.SignalLabel=Label(self.SCab, image=self.Master.sigpicsmall[self.Signal], anchor=W)
        self.SpeedLabel=Label(self.SCab, text=str(self.Speed), width=6, anchor=W)
        
        for widget in (self.SignalLabel, self.CommBut, self.BlockLabel, self.SpeedLabel, self.HeadingLabel):
            widget.pack(side=LEFT)
        self.Displayed=True

class SCabManager:
    def __init__(self, master, scabframe=None, summaryframe=None):
        self.Master=master
        self.SCabFrame=scabframe
        self.SummaryFrame=summaryframe
        self.TrainSummary=None
        self.SummaryList=[]
        self.SummarySCabs=[]
        self.ControlList=[]
        self.ControlSCabs=[]

    def AddTrain(self, train, owned):
        self.AddSummary(train)
        if owned and train not in self.ControlList:
            self.AddControls(train)
            
    def DeleteTrain(self, train):
        if train in self.SummaryList:
            index=self.SummaryList.index(train)
            del self.SummaryList[index]
            self.SummarySCabs[index].Undisplay()
            del self.SummarySCabs[index]
            if len(self.SummaryList)==0:
                self.DeleteSummaryWindow()
        if train in self.ControlList:
            index=self.ControlList.index(train)
            del self.ControlList[index]
            self.ControlSCabs[index].Undisplay()
            del self.ControlSCabs[index]

    def AddSummary(self, train):
        if self.TrainSummary==None:
            if self.SummaryFrame==None:
                self.TrainSummary=Toplevel(self.Master.root)
                self.TrainSummary.resizable(0,0)
                self.TrainSummary.protocol("WM_DELETE_WINDOW", self.DeleteSummaryWindow)
                self.TrainSummary.title('Train Summary')
                self.TrainSummary.transient(self.Master.root)
            else:
                self.TrainSummary=Frame(self.SummaryFrame)
                self.TrainSummary.pack(side=TOP)
            summframe=Frame(self.TrainSummary, borderwidth=1, relief=SUNKEN)
            summframe.pack(side=TOP, fill='x', expand=1)
            self.SummaryHeadings(summframe)

        scabframe=Frame(self.TrainSummary)
        scabframe.pack(side=TOP)
        
        if self.SummaryFrame!=None:
            newscab=SCabSummarySmall(self.Master, self, train)
        else:
            newscab=SCabSummary(self.Master, self, train)
            
        newscab.Display(scabframe)
        self.SummaryList+=[train]
        self.SummarySCabs+=[newscab]

    def DeleteSummaryWindow(self, event=None):
        if self.TrainSummary!=None and len(self.SummarySCabs)==0:
            self.TrainSummary.destroy()
            self.TrainSummary=None

    def SummaryHeadings(self, frame):
        SignalLabel=Label(frame, image=self.Master.sigpicsmall['unknown'], anchor=W)
        CommLabel=Label(frame, text='Train/HCab', width=10, anchor=W, padx=5)
        BlockLabel=Label(frame, text='Block', width=6, anchor=W)
        HeadingLabel=Label(frame, text='Heading', width=9, anchor=W)
        SpeedLabel=Label(frame, text='Speed', width=6, anchor=W)
        
        for widget in (SignalLabel, CommLabel, BlockLabel, SpeedLabel, HeadingLabel):
            widget.pack(side=LEFT)
        

    def AddControls(self, train):
        if train not in self.ControlList:
            if self.SCabFrame==None:
                newwin=Toplevel(self.Master.root)
                newwin.resizable(0,0)
                newwin.title('SCab: '+train.Name)
                newwin.positionfrom('')
                newwin.transient(self.Master.root)

                newscab=SCabWindow(self.Master, self, train)
                newwin.protocol("WM_DELETE_WINDOW", lambda event=None, scab=newscab, deltrain=train: self.DeleteSCab(scab, deltrain))
                newscab.Display(newwin)
                self.ControlList+=[train]
                self.ControlSCabs+=[newscab]
            else:
                if self.ControlList==[]:
                    newframe=Frame(self.SCabFrame)
                    newframe.pack(side=TOP)
                    newscab=SCabWindowShort(self.Master, self, train)
                    newscab.Display(newframe)
                    self.ControlList=[train]
                    self.ControlSCabs=[newscab]
                else:
                    self.ControlSCabs[0].SetTrain(train)
                    self.ControlList=[train]

    def DeleteSCab(self, scab, train):
        if scab in self.SummarySCabs:
            scab.Undisplay()
            index=self.SummaryList.index(train)
            del self.SummaryList[index]
            index=self.SummarySCabs.index(scab)
            del self.SummarySCabs[index]
        if scab in self.ControlSCabs:
            scab.Undisplay()
            index=self.ControlList.index(train)
            del self.ControlList[index]
            index=self.ControlSCabs.index(scab)
            del self.ControlSCabs[index]

    def SpdKeyControl(self, event):
        if len(self.ControlSCabs)==1:
            self.ControlSCabs[0].SpdKeyControl(event)

class NewSCabPicker:
    def __init__(self, master, block):
        """Create window used to name trains and select hardware cabs

        This function is used as a callback based on mouse clicks on blocks.
        The event argument is not used by the function.  The function checks
        for the existence of another NewScab Window in the self.master level
        and destroys it if it exists.  It does this to ensure that no more
        than one train picker window is open at once.  This is a design choice,
        not a necessity.  This function then creates the window and all the
        associated widgets and so forth."""

        self.Master=master
        self.Block=block
        
        self.NSWindow=Toplevel(self.Master.root)
        self.NSWindow.title('Create new train')
        self.NSWindow.protocol("WM_DELETE_WINDOW",self.KillNSWindow)
        self.NSWindow.resizable(0,0)
        self.NSWindow.transient(self.Master.root)
        pad=2
        Label(self.NSWindow, text='Create new train', font=('Arial', 18, 'bold')).pack(side=TOP, padx=pad)
        self.blocklabel=Label(self.NSWindow, text='in block '+self.Block.DName, font=('Arial', 18, 'bold'))
        self.blocklabel.pack(side=TOP, padx=pad)

        entryframe=Frame(self.NSWindow)
        Label(entryframe, text='Train Name:').pack(side=LEFT)
        self.TrainName=StringVar()
        self.entertrain=Entry(entryframe, width=15, textvariable=self.TrainName)
        self.entertrain.pack(side=LEFT)
        self.entertrain.bind("<Return>", self.PickNewSCab)
        self.entertrain.focus_set()
        entryframe.pack(side=TOP, pady=pad)

        self.Direction=IntVar()
        dirframe=Frame(self.NSWindow, borderwidth=2, relief=GROOVE)
        if self.Block.LogicalDirection in ('east', 'west'):
            self.Direction.set(EAST)
            self.RB1=Radiobutton(dirframe, text='East bound',
                                                 value=EAST, variable=self.Direction)
            self.RB1.pack(side=LEFT)
            self.RB2=Radiobutton(dirframe, text='West bound',
                                                 value=WEST, variable=self.Direction)
            self.RB2.pack(side=LEFT)
        else:
            if self.Block.Cons[0].Object!=None:
                dir0=self.Block.Cons[0].Object.DName
            else:
                dir0='dead end'
            if self.Block.Cons[1].Object!=None:
                dir1=self.Block.Cons[1].Object.DName
            else:
                dir1='dead end'
            self.Direction.set(0)
            self.RB1=Radiobutton(dirframe, text='Into '+dir0,
                                                 value=0, variable=self.Direction)
            self.RB1.pack(side=LEFT)
            self.RB2=Radiobutton(dirframe, text='Into '+dir1,
                                                 value=1, variable=self.Direction)
            self.RB2.pack(side=LEFT)
        dirframe.pack(side=TOP, pady=pad, padx=pad, fill=X)

        self.HCab=StringVar()
        self.HCab.set(None)
        hcabframe=Frame(self.NSWindow, borderwidth=2, relief=GROOVE)
        Radiobutton(hcabframe, text='No HCab', value='None', variable=self.HCab).pack(side=TOP)
        HCabs=self.Master.HCabList.keys()
        for HCab in HCabs:
            if self.Master.HCabList[HCab].Owner==None:
                Radiobutton(hcabframe, text=str(HCab), value=HCab, variable=self.HCab).pack(side=TOP)
        hcabframe.pack(side=TOP, pady=pad, padx=pad, fill=X)

        self.PickButt=Button(self.NSWindow, text="Pick SCab",
                                             bg='#ffffff', command=self.PickNewSCab, width=15, font=('Arial', 12))
        self.PickButt.pack(side=TOP, pady=pad)

        self.NSWarn=Label(self.NSWindow, text='Please enter train name')
        self.NSWarn.pack(side=TOP, padx=pad, pady=pad)

    def UpdateBlock(self, block):
        self.block=block
        self.blocklabel.configure(text='in block '+self.block.name[1:])
        self.entertrain.bind("<Return>", self.PickNewSCab)
        self.PickButt.configure(command=self.PickNewSCab)
        if self.Block.LogicalDirection in ('east', 'west'):
            self.RB1.configure(text='East bound')
            self.RB2.configure(text='West bound')
        elif self.Block.LogicalDirection in ('easteast', 'westwest'):
            if self.Block.Cons[0].Object!=None:
                dir0=self.Block.Cons[0].Object.DName
            else:
                dir0='dead end'   
            if self.Block.Cons[1].Object!=None:
                dir1=self.Block.Cons[1].Object.DName
            else:
                dir1='dead end'
            self.RB1.configure(text='Into '+dir0)
            self.RB2.configure(text='Into '+dir1)

    def PickNewSCab(self, event=None):
        """Function to ask server to create new trains.

        This function checks to ensure that the selected train name is valid,
        issuing a warning if it is not.  Then it sends the server the command to
        create the train.  If the user has selected an HCab, the function checks
        to be sure the HCab is still available, and sends the server the message
        to assign it to the newly created train.  Finally, the window is detroyed,
        and some of the associated variables are deleted."""
        
        newname=self.TrainName.get()
        newname=newname.strip()
        if newname.find('"') > -1:
            self.Master.logger.LogWarnMsg('Train name may not contain double quote (") character')
            self.NSWarn.configure(text='Train name cannot include `"`', fg='Red')
            return
        if len(newname)==0:
            self.Master.logger.LogWarnMsg('You must enter a Train Identifier string')
            self.NSWarn.configure(text='Please enter train name', fg='Red')
            return
        if self.Master.SCabList.has_key(newname):
            self.Master.logger.LogWarnMsg('Cannot enter duplicate Train Identifier string')
            self.NSWarn.configure(text='Duplicate train name', fg='Red')
            return
        if self.Block.occstatus in (OWNED, ADVBLOCK):
            self.Master.logger.LogWarnMsg('Cannot make block there')
            self.NSWarn.configure(text='Train already in block', fg='Red')
            return
        self.Master.TrainQueue[newname]=1
        # Message format: (addTrain "TrainName" (Obj "BlockName"))
        OutStr='(addTrain "'+newname+'" (obj "'+self.Block.name+'"))'
        self.Master.SockWrite(OutStr)

        if (self.Direction.get()==0 and self.Block.LogicalDirection != 'east') or (self.Direction.get()==1 and self.Block.LogicalDirection == 'east'):
            OutStr='(reverse (obj "'+newname+'"))'
            self.Master.SockWrite(OutStr)

        if self.HCab.get()!='None' and self.Master.HCabList[self.HCab.get()].Owner==None:
            # Message format: (assigncab (Obj "Cab") (Obj "TrainName"))
            OutStr='(assigncab (Obj "'+self.HCab.get()+'") (Obj "'+newname+'"))'
            self.Master.SockWrite(OutStr)
        self.KillNSWindow()

    def KillNSWindow(self, event=None):
        """Function to destroy new scab window

        This function serves to destroy the new scab window and delete some
        associated variables.  It may be used as a callback when the close
        window button is clicked, or as a regular function when creating a
        new train.  The event argument is not used."""
        self.NSWindow.destroy()
        self.Master.NewSCabPicker=None
        
if __name__ == '__main__':
    root=Tk()
    root.mainloop()
    master=None
    SCab(master, root, 'Test', 0)
