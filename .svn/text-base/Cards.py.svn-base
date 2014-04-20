# Thomas O'Reilly, 16 June 2002
# TMRC System 3 display block and switch card object definitions

switchnum=8
blocknum=8

from Tkinter import *
import Pmw

class CardEditor:
    def __init__(self, master, type):
        self.master=master
        if type=='switchcard':
            self.dtype='SwitchCard'
            self.type='switchcard'
            self.eltype='switches'
            self.seltype='switch'
            self.List=self.master.SCList
            self.ItemList=self.master.Slist
            self.num=switchnum
        else:
            self.dtype='BlockCard'
            self.type='blockcard'
            self.eltype='blocks'
            self.seltype='block'
            self.List=self.master.BCList
            self.ItemList=self.master.Blist
            self.num=blocknum

        self.EditWindow=Toplevel(self.master.root)
        self.EditWindow.title('Edit '+self.type+' assignments')
        self.EditWindow.protocol("WM_DELETE_WINDOW", self.DoneEditing)
        self.EditWindow.resizable(0,0)
        self.EditWindow.transient(self.master.root)
        self.cards=len(self.List)
        self.cardnames=self.List.keys()
        self.cardnames.sort()
        self.newstate=[[None]*self.num]
        for i in range(1,self.cards):
            self.newstate=self.newstate+[[None]*self.num]
        if self.type=='switchcard':
            self.inputs=[None]*self.cards
            self.signals=[None]*self.cards
            for i in range(self.cards):
                self.inputs[i]=StringVar()
                self.signals[i]=StringVar()

        topframe=Frame(self.EditWindow)
        topframe.pack(side=TOP)
        Label(topframe, text='Card Number').grid(row=0, column=0)
        for j in range(self.num):
            Label(topframe, text='Slot '+str(j)).grid(row=0, column=j+1)
            if self.type=='switchcard':
                Label(topframe, text='Input String').grid(row=0, column=self.num+1)
                Label(topframe, text='Signal String').grid(row=0, column=self.num+2)
        for i in range(self.cards):
            Label(topframe, text=str(self.List[self.cardnames[i]].number), justify='right').grid(row=i+1, column=0)
            for j in range(self.num):
                self.newstate[i][j]=StringVar()
                Entry(topframe, textvariable=(self.newstate[i][j]), relief='raised', borderwidth=2, bg='White', width=8).grid(row=i+1, column=j+1, padx=2, pady=2)
                self.newstate[i][j].set(self.List[self.cardnames[i]].cardlist[j])
            if self.type=='switchcard':
                self.inputs[i]=StringVar()
                self.inputs[i].set(self.List[self.cardnames[i]].input)
                self.signals[i]=StringVar()
                self.signals[i].set(self.List[self.cardnames[i]].signal)
                Entry(topframe, textvariable=(self.inputs[i]), relief='raised', borderwidth=2, bg='White', width=25).grid(row=i+1, column=self.num+1, padx=2, pady=2)
                Entry(topframe, textvariable=(self.signals[i]), relief='raised', borderwidth=2, bg='White', width=25).grid(row=i+1, column=self.num+2, padx=2, pady=2)
            
        self.freeitems='Unassigned '+self.eltype+': '
        self.items=self.ItemList.keys()
        self.items.sort()
        for item in self.items:
            if self.ItemList[item].card==None:
                self.freeitems=self.freeitems+item+' '
        self.NewCard=StringVar()

        bottomframe=Frame(self.EditWindow)
        bottomframe.pack(side=TOP)
        Button(bottomframe, text='Add', command=self.AddCard).grid(row=0, column=1)
        self.newcard=Pmw.Counter(bottomframe, labelpos='w', label_text='New card number:',  entry_width=4,
                                entryfield_value=0, entryfield_validate={'validator':'integer'})
        self.newcard.grid(row=0, column=3, columnspan=3, padx=2, pady=2)
        Button(bottomframe, text='Delete', command=self.DeleteCard).grid(row=0, column=7)
        self.freeLabel=Label(bottomframe, text=self.freeitems, wraplength=250, borderwidth=2, relief='raised')
        self.freeLabel.grid(row=1, column=3, columnspan=5, padx=2, pady=2)
        Button(bottomframe, text='Update Assignments', command=self.Update).grid(row=2, column=1, columnspan=3)
        Button(bottomframe, text='Finished', command=self.DoneEditing).grid(row=2, column=5, columnspan=3)

    def DoneEditing(self, event=None):
        self.EditWindow.destroy()

    def Update(self, event=None):
        for i in range(self.cards):
            for j in range(self.num):
                if (self.newstate[i][j]).get()!=self.List[self.cardnames[i]].cardlist[j]:
                    self.List[self.cardnames[i]].SetCards([(self.newstate[i][j]).get()], j)
        for i in range(self.cards):
            for j in range(self.num):
                (self.newstate[i][j]).set(self.List[self.cardnames[i]].cardlist[j])
        self.items=self.ItemList.keys()
        self.items.sort()
        self.freeitems='Unassigned '+self.eltype+': '
        for item in self.items:
            if self.ItemList[item].card==None:
                self.freeitems=self.freeitems+item+' '
        self.freeLabel.configure(text=self.freeitems)

    def AddCard(self, event=None):
        if not self.List.has_key( int(self.newcard.get()) ):
            self.List[int(self.newcard.get())]=Card(self.master, int(self.newcard.get()), self.type)
            CardEditor(self.master, self.type)
            self.DoneEditing()
        
    def DeleteCard(self, event=None):
        if self.List.has_key( int(self.newcard.get()) ):
            for item in self.List[int(self.newcard.get())].cardlist:
                if item!=None:
                    self.ItemList[item].card=None
            del self.List[int(self.newcard.get())]
            CardEditor(self.master, self.type)
            self.DoneEditing()

class Card:
    def __init__(self, master, number, type):
        self.master=master
        self.number=int(number)
        self.fdic={'blocks':self.SetCards,
                   'switches':self.SetCards,
                   'input':self.SetInput}
        if type=='switchcard':
            self.type='SwitchCard'
            self.eltype='switches'
            self.seltype='switch'
            self.cardlist=[None]*switchnum
            self.List=self.master.SCList
            self.signal=''
            self.input=''
        else:
            self.type='BlockCard'
            self.eltype='blocks'
            self.seltype='block'
            self.cardlist=[None]*blocknum
            self.List=self.master.BCList
        
    def SetCards(self, addlist, index=0):
#        print 'adding cards', addlist
        if index+len(addlist)>switchnum:
            self.master.logger.LogWarnMsg(type+' position out of bounds')
            return
        for n in range(len(addlist)):
            if addlist[n] in ('none', 'None', 'nil', 'Nil','', ' ', None):
                if self.cardlist[n+index]!=None:
                    self.master.Ddict[self.cardlist[n+index]].card=None
                    self.cardlist[n+index]=None
            else:
                # First, clear any existing block from the card
                # and slot about to be filled
                if self.cardlist[n+index]!=None:
                    self.master.Ddict[self.cardlist[n+index]].card=None
                # Then, clear the card and slot currently occupied by
                # the block about to be placed
                if self.master.Ddict.has_key(addlist[n]) and self.master.Ddict[addlist[n]].type==self.seltype:
                    if self.master.Ddict[addlist[n]].card!=None:
                        oldcard=self.master.Ddict[addlist[n]].card
                        oldslot=self.List[oldcard].cardlist.index(addlist[n])
                        self.List[oldcard].cardlist[oldslot]=None
                    # Then place the block in the appropriate slot
                    self.cardlist[n+index]=addlist[n]
                    self.master.Ddict[self.cardlist[n+index]].card=self.number
                else:
                    if not self.master.Ddict.has_key(addlist[n]):
                        self.master.logger.LogWarnMsg('Cannot associate non-existant '+self.seltype+
                                                      ' '+addlist[n]+' with '+self.type+' '+str(self.number))
                    elif  self.master.Ddict[addlist[n]].type!=self.seltype:
                        self.master.logger.LogWarnMsg('Cannot associate '+self.master.Ddict[addlist[n]].type+
                                                      ' '+addlist[n]+' with '+self.type+' '+str(self.number))
                    else:
                        self.master.logger.LogWarnMsg('Cannot figure out how to put '+self.master.Ddict[addlist[n]].type+
                                                      ' '+addlist[n]+' with '+self.type+' '+str(self.number))
                        
                        

    def SetInput(self, input):
        self.input=int(input)

    def ProcSexp(self, Psexp):
        if self.fdic.has_key(Psexp.tokens[2]):
            self.fdic[Psexp.tokens[2]](Psexp.tokens[3])
        else:
            self.master.logger.LogWarnMsg('Unknown variable '+Psexp.tokens[2]+' in '+self.type)
