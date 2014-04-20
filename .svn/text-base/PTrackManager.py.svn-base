from Tkinter import *
import math
import random
import Pmw

import PBlock
import PSwitch
import PCrossing
import PTurnTable
from PLineManager import *
from PTurnTableCircle import *
from PTrack import *
from PTextPoint import *
from PCenterPoint import *
from PTurnTablePoint import *
from PTrackPoint import *
from PPoint import *
from PFunc import *

class PTrackManager(PLineManager):
    def __init__(self, master, DM, cv):
        PLineManager.__init__(self, cv)
        self.Master=master
        self.DM=DM
        self.MinLabelScale=0.2
        self.MinPointScale=0.2
        self.SnapInc=10

        self.Clickable=True
        self.Mode='Run'
        self.scv=self.cv
        self.cv=self.scv.interior()
        self.cv.config(bg='Black')

        self.Objects={}
        self.textpointnum=0
        self.PTextPoints={}

    def SetClickable(self, clickable=None):
        if clickable==None and self.Clickable==True:
            self.Clickable=False
        elif clickable==None and self.Clickable==False:
            self.Clickable=True
        elif clickable in (True, False):
            self.Clickable=clickable

    def AddTrack(self):
        self.lines[self.linenum]=PTrack(self, self.linenum)
        self.linenum+=1
        return self.lines[self.linenum-1]

    def AddTrackPoint(self, coord):
        self.points[self.pointnum]=PTrackPoint(self, coord, self.pointnum)
        self.pointnum+=1
        return self.points[self.pointnum-1]

    def AddTrackPointToLine(self, coord, line, index=None):
        point=self.AddTrackPoint(coord)
        self.lines[line].InsertPoint(point, index)

    def AddTextPoint(self, event=None):
        coord=(0, 0)
        width=self.cv.winfo_width()
        height=self.cv.winfo_height()
        canvasx=(self.cv.canvasx(0)+int(width/2))*self.Scale
        canvasy=(self.cv.canvasy(0)+int(height/2))*self.Scale
        self.points[self.pointnum]=PTextPoint(self, (canvasx, canvasy), self.pointnum)
        self.pointnum+=1

    def ExtendLayout(self, object, end, point, connect):
        if self.Master.Blist.has_key(object.name):
            self.AddBlock(object, end, point, connect)
        elif self.Master.Slist.has_key(object.name):
            self.AddSwitch(object, end, point, connect)
        elif self.Master.Clist.has_key(object.name):
            self.AddCrossing(object, end, point, connect)
        self.scv.resizescrollregion()
        self.Restack()

    def DeleteSelected(self, group):
        if group==0:
            pointgroup=self.PickedPoints0
        else:
            pointgroup=self.PickedPoints1

        ownerlist=[]
        for point in pointgroup:
            if point.Type=='PTextPoint':
                self.DeletePoint(point)
            else:
                linedic=point.TellOwners()
                for line in linedic.values():
                    newowner=line.TellOwner()
                    if newowner not in ownerlist:
                        ownerlist+=[newowner]

        for owner in ownerlist:
            self.DeleteObject(owner)
                
    def DeleteObject(self, object):
        object.DeleteAllInstances()
        del self.Objects[object.Name]
    
    def DeleteAll(self):
        for objectname in self.Objects.keys():
            self.DeleteObject(self.Objects[objectname])
        for pointnum in self.points.keys():
            self.points[pointnum].Undraw()
            del self.points[pointnum]
        self.linenum=0
        self.pointnum=0

    def AddCrossing(self, crossing, end, point, connect):
        if not self.Objects.has_key(crossing.name):
            self.Objects[crossing.name]=PCrossing.PCrossing(self, crossing)

        track0 = self.AddTrack()
        track1 = self.AddTrack()

        self.Objects[crossing.name].AddLine(track0, track1)
      
        if point is None:
            basex=200
            basey=200
            width=50
            height=50
            pointv = [None]*5
            pointv[0]=self.AddTrackPoint((basex-width, basey))
            pointv[1]=self.AddTrackPoint((basex+width, basey))
            pointv[2]=self.AddTrackPoint((basex, basey-height))
            pointv[3]=self.AddTrackPoint((basex, basey+height))
            pointv[4]=self.AddTrackPoint((basex, basey))

            track0.InsertPoint(pointv[0], None)
            track0.InsertPoint(pointv[4], None)
            track0.InsertPoint(pointv[2], None)
            track1.InsertPoint(pointv[1], None)
            track1.InsertPoint(pointv[4], None)
            track1.InsertPoint(pointv[3], None)

        else:
            owners=point.Owners.keys()
            currenttrack=point.Owners[owners[0]]
            angle=currenttrack.TellAngle(point)[0]
            existingcoord=point.TellCoord()

            points = []

            for n in range(4):
                nextobj, nextcon = self.Objects[crossing.name].Connection(n)
                if self.Objects.has_key(nextobj.name):
                    points.append(self.Objects[nextobj.name].TellPoints(nextcon))
                else:
                    points.append([])
                
            midcoord=(existingcoord[0]+math.cos(angle)*50, existingcoord[1]+math.sin(angle)*50)
            pointcoord = [0,
                (midcoord[0]+math.cos(angle+math.pi/2.0)*50, midcoord[1]+math.sin(angle+math.pi/2.0)*50),
                (midcoord[0]+math.cos(angle)*50, midcoord[1]+math.sin(angle)*50),
                (midcoord[0]+math.cos(angle-math.pi/2.0)*50, midcoord[1]+math.sin(angle-math.pi/2.0)*50)]

            pointv = [[], [], [], []]
            pointv[end] = point

            for i in range(1, 4):
                if points[(end+i)%4] and connect is True:
                    pointv[(end+i)%4]=points[(end+i)%4][0]
                else:
                    pointv[(end+i)%4]=self.AddTrackPoint(pointcoord[i])
 
            midpoint=self.AddTrackPoint(midcoord)

            track0.InsertPoint(pointv[0], None)
            track0.InsertPoint(midpoint, None)
            track0.InsertPoint(pointv[2], None)
            track1.InsertPoint(pointv[1], None)
            track1.InsertPoint(midpoint, None)
            track1.InsertPoint(pointv[3], None)

        self.Objects[crossing.name].UpdateStatus()


    def AddBlock(self, block, end, point, connect):
        if not self.Objects.has_key(block.name):
            self.Objects[block.name]=PBlock.PBlock(self, block)

        track=self.AddTrack()
        self.Objects[block.name].AddLine(track)
        
        if point==None:
            point0=self.AddTrackPoint((50, 50))
            point1=self.AddTrackPoint((250, 50))
            
            if end==1:
                track.InsertPoint(point1, None)
                track.InsertPoint(point0, None)
            else:
                track.InsertPoint(point0, None)
                track.InsertPoint(point1, None)

        else:
            owners=point.Owners.keys()
            currenttrack=point.Owners[owners[0]]

            if end==0:
                nextobj, nextcon = self.Objects[block.name].Connection(1)
            else:
                nextobj, nextcon = self.Objects[block.name].Connection(0)

            if nextobj==None:
                connect=False
            else:
                if nextobj.name not in self.Objects.keys():
                    connect=False
                    
            if connect==True:
                points=self.Objects[nextobj.name].TellPoints(nextcon)
                newpoint=points[0]
            else:
                angle=currenttrack.TellAngle(point)[0]
                existingcoord=point.TellCoord()
                newpointcoord=(existingcoord[0]+math.cos(angle)*50, existingcoord[1]+math.sin(angle)*50)
                newpoint=self.AddTrackPoint(newpointcoord)

            if end==1:
                track.InsertPoint(newpoint, None)
                track.InsertPoint(point, None)
            else:     
                track.InsertPoint(point, None)
                track.InsertPoint(newpoint, None)

        self.Objects[block.name].UpdateStatus()

    def AddSwitch(self, switch, end, point, connect):

        if not self.Objects.has_key(switch.name):
            self.Objects[switch.name]=PSwitch.PSwitch(self, switch)

        track0=self.AddTrack()
        track1=self.AddTrack()

        self.Objects[switch.name].AddLine(track0, track1)
        hand=switch.hand
      
        if point==None:
            
            if end==0:
                point0=self.AddTrackPoint((150, 75))
                point1=self.AddTrackPoint((250, 50))
                point2=self.AddTrackPoint((250, 100))
            else:
                point0=self.AddTrackPoint((250, 75))
                point1=self.AddTrackPoint((150, 50))
                point2=self.AddTrackPoint((150, 100))

            track0.InsertPoint(point0, None)
            track1.InsertPoint(point0, None)
            if hand==0:
                track0.InsertPoint(point2, None)
                track1.InsertPoint(point1, None)
            else:
                track0.InsertPoint(point1, None)
                track1.InsertPoint(point2, None)

        else:
            owners=point.Owners.keys()
            currenttrack=point.Owners[owners[0]]
            angle=currenttrack.TellAngle(point)[0]
            existingcoord=point.TellCoord()

            points0=[]
            points1=[]
            points2=[]

            nextobj0, nextcon0 = self.Objects[switch.name].Connection(0)
            if nextobj0!=None:
                if self.Objects.has_key(nextobj0.name):
                    points0=self.Objects[nextobj0.name].TellPoints(nextcon0)
            nextobj1, nextcon1 = self.Objects[switch.name].Connection(1)
            if nextobj1!=None:
                if self.Objects.has_key(nextobj1.name):
                    points1=self.Objects[nextobj1.name].TellPoints(nextcon1)
            nextobj2, nextcon2 = self.Objects[switch.name].Connection(2)
            if nextobj2!=None:
                if self.Objects.has_key(nextobj2.name):
                    points2=self.Objects[nextobj2.name].TellPoints(nextcon2)

            if end==0:
                rpointcoord=(existingcoord[0]+math.cos(angle+math.pi/8.0)*50, existingcoord[1]+math.sin(angle+math.pi/8.0)*50)
                lpointcoord=(existingcoord[0]+math.cos(angle-math.pi/8.0)*50, existingcoord[1]+math.sin(angle-math.pi/8.0)*50)

                point0=point

                if points1!=[] and connect==True:
                    point1=points1[0]
                else:
                    if hand==0:
                        point1=self.AddTrackPoint(lpointcoord)
                    else:
                        point1=self.AddTrackPoint(rpointcoord)

                if points2!=[] and connect==True:
                    point2=points2[0]
                else:
                    if hand==0:
                        point2=self.AddTrackPoint(rpointcoord)
                    else:
                        point2=self.AddTrackPoint(lpointcoord)

            elif end==1:
                point0coord=(existingcoord[0]+math.cos(angle)*50, existingcoord[1]+math.sin(angle)*50)

                if hand==0:
                    deltaangle=math.pi*5.0/4.0
                else:
                    deltaangle=math.pi*3.0/4.0
                    
                point2coord=(point0coord[0]+math.cos(angle+deltaangle)*50, point0coord[1]+math.sin(angle+deltaangle)*50)

                if points0 != [] and connect==True:
                    point0=points0[0]
                else:
                    point0=self.AddTrackPoint(point0coord)
                point1=point
                if points2 != [] and connect==True:
                    point2=points2[0]
                else:
                    point2=self.AddTrackPoint(point2coord)

            elif end==2:
                point0coord=(existingcoord[0]+math.cos(angle)*50, existingcoord[1]+math.sin(angle)*50)

                if hand==0:
                    deltaangle=math.pi*3.0/4.0
                else:
                    deltaangle=math.pi*5.0/4.0
                    
                point1coord=(point0coord[0]+math.cos(angle+deltaangle)*50, point0coord[1]+math.sin(angle+deltaangle)*50)

                if points0 != [] and connect==True:
                    point0=points0[0]
                else:
                    point0=self.AddTrackPoint(point0coord)
                if points1 != [] and connect==True:
                    point1=points1[0]
                else:
                    point1=self.AddTrackPoint(point1coord)
                point2=point

            track0.InsertPoint(point0, None)
            track1.InsertPoint(point0, None)
            track0.InsertPoint(point1, None)
            track1.InsertPoint(point2, None)

        self.Objects[switch.name].UpdateStatus()

    def Refresh(self):
        self.scv.resizescrollregion()
        for point in self.points.keys():
            self.points[point].UpdateShape()
        self.Restack()

    def ReMapCircles(self):
        circles=self.circles.keys()
        circles.sort()
        return circles

    def ReMapLines(self):
        lines=self.lines.keys()
        lines.sort()
        return lines

    def ReMapPoints(self):
        points=self.points.keys()
        points.sort()
        return points

    def LoadDisplay(self, filename=None):
        if filename==None:
            filename=tkFileDialog.askopenfilename()
        try:
            file=open(filename)
        except TypeError:
            return
        self.DeleteAll()

        plist=self.points.keys()
        llist=self.lines.keys()
        clist=self.circles.keys()
        if len(plist)>0:
            poffset=max(self.points.keys())
        else:
            poffset=0
        if len(llist)>0:
            loffset=max(self.lines.keys())
        else:
            loffset=0
        if len(clist)>0:
            coffset=max(self.circles.keys())
        else:
            coffset=0

        lines=file.readlines()
        for line in lines:
            tokens=line.split('||')
            if tokens[0] in ('PPoint', 'PTrackPoint', 'PTextPoint', 'PCenterPoint', 'PTurnTablePoint'):
                self.LoadPoint(tokens, poffset)
            elif tokens[0] in ('PCircle', 'PTurnTableCircle'):
                self.LoadCircle(tokens, poffset, coffset)
            elif tokens[0] in ('PLine', 'PTrack'):
                self.LoadLine(tokens, poffset, loffset)
            elif tokens[0] in ('PBlock', 'PSwitch', 'PCrossing','PTurnTable'):
                self.LoadObject(tokens, poffset, loffset, coffset)
        
        self.Refresh()
        self.SetMode(mode=self.Mode)

    def LoadPoint(self, tokens, poffset):
        coord=(0,0)

        pointclass=eval(tokens[0])

        for token in tokens[1:]:
            stoken=token.split('|')
            exec(stoken[0]+'='+stoken[1])
            
        self.points[num+poffset]=pointclass(self, coord, num+poffset, tokens)
        self.pointnum=num+poffset+1

    """def LoadTextPoint(self, tokens):
        coord=(0,0)

        pointclass=eval(tokens[0])
        textsize=28
        text='Foo'

        for token in tokens[1:]:
            stoken=token.split('|')
            exec(stoken[0]+'='+stoken[1])
            
        self.points[self.pointnum]=pointclass(self, coord, self.textpointnum, text)
        self.textpointnum+=1"""

    def LoadLine(self, tokens, poffset, loffset):
        labelpos=0.5
        pointlist=[]

        lineclass=eval(tokens[0])

        for token in tokens[1:]:
            stoken=token.split('|')
            exec(stoken[0]+'='+stoken[1])
            
        self.lines[num+loffset]=lineclass(self, num+loffset)
        self.linenum=num+loffset+1

        for point in points:
            self.lines[num+loffset].InsertPoint(self.points[point+poffset], hold=True)
        self.lines[num+loffset].UpdatePoints() 

        if labelpos!=0.5:
            self.lines[num+loffset].SetLabelPos(labelpos)

    def LoadCircle(self, tokens, poffset, coffset):
        circleclass=eval(tokens[0])

        for token in tokens[1:]:
            stoken=token.split('|')
            exec(stoken[0]+'='+stoken[1])
            
        self.circles[num+coffset]=circleclass(self, num+coffset, self.points[center+poffset],radius)
        self.circlenum=num+coffset+1

        for point in points:
            self.points[point+poffset].SetCircle(self.circles[num+coffset])
        self.circles[num+coffset].UpdatePoints() 


    def LoadObject(self, tokens, poffset, loffset, coffset):
        name=None

        objectclass=eval(tokens[0])

        for token in tokens[1:]:
            stoken=token.split('|')
            exec(stoken[0]+'='+stoken[1])
            
        if tokens[0]=='PBlock':
            block=self.Master.Blist[name]
            self.Objects[block.name]=PBlock.PBlock(self, block)
            for i in range(len(lines)):
                self.Objects[block.name].AddLine(self.lines[lines[i]+loffset])

            self.Objects[block.name].UpdateStatus()
        elif tokens[0]=='PSwitch':
            switch=self.Master.Slist[name]
            self.Objects[switch.name]=PSwitch.PSwitch(self, switch)
            for i in range(len(lines0)):
                self.Objects[switch.name].AddLine(self.lines[lines0[i]+loffset], self.lines[lines1[i]+loffset])

            self.Objects[switch.name].UpdateStatus()
        elif tokens[0]=='PCrossing':
            crossing=self.Master.Clist[name]
            self.Objects[crossing.name]=PCrossing.PCrossing(self, crossing)
            for i in range(len(lines0)):
                self.Objects[crossing.name].AddLine(self.lines[lines0[i]+loffset], self.lines[lines1[i]+loffset])

            self.Objects[crossing.name].UpdateStatus()
        elif tokens[0]=='PTurnTable':
            table=self.Master.TTlist[name]
            self.Objects[table.name]=PTurnTable.PTurnTable(self, table)
            for i in range(len(lines)):
                newlines=[self.lines[lin + loffset] for lin in lines[i]]
                self.Objects[table.name].AddCircle(self.circles[circles[i]+coffset],newlines)

            self.Objects[table.name].UpdateStatus()

    def SaveDisplay(self, file=None):
        if file==None:
            file=tkFileDialog.asksaveasfile()
        self.SavePoints(file)
        self.SaveLines(file)
        self.SaveCircles(file)
        self.SaveObjects(file)
        file.close()

    def SavePoints(self, file):
        pointmap=self.ReMapPoints()
        for index, pointnum in zip(range(len(pointmap)), pointmap):
            string=self.points[pointnum].SaveString(str(index))
            file.write(string)

    def SaveLines(self, file):
        pointmap=self.ReMapPoints()
        linemap=self.ReMapLines()
        for index, linenum in zip(range(len(linemap)), linemap):
            type=self.lines[linenum].Type
            pointlist=self.lines[linenum].TellPointList()
            newpointlist=[0]*len(pointlist)
            for i in range(len(pointlist)):
                newpointlist[i]=pointmap.index(pointlist[i].Number)
            pointsstring=str(newpointlist)
            labelpos=str(self.lines[linenum].TellLabelPos())
            string=type+'||num|'+str(index)+'||labelpos|'+labelpos+'||points|'+pointsstring+'\n'
            file.write(string)

    def SaveCircles(self, file):
        pointmap=self.ReMapPoints()
        circlemap=self.ReMapCircles()
        for index, circlenum in zip(range(len(circlemap)), circlemap):
            type=self.circles[circlenum].Type
            center=self.circles[circlenum].TellCenter()
            newcenter=pointmap.index(center.Number)
            pointlist=self.circles[circlenum].TellCircumferencePointList()
            newpointlist=[0]*len(pointlist)
            for i in range(len(pointlist)):
                newpointlist[i]=pointmap.index(pointlist[i].Number)
            pointsstring=str(newpointlist)
            string=type+'||num|'+str(index)+'||center|'+str(newcenter)+ '||radius|'+ str(self.circles[circlenum].TellRadius()) +'||points|'+pointsstring+'\n'
            file.write(string)

    def SaveObjects(self, file):
        objectlist=self.Objects.keys()
        objectlist.sort()
        linemap=self.ReMapLines()
        circlemap=self.ReMapCircles()
        for objectname in objectlist:
            type=self.Objects[objectname].Type
            name=self.Objects[objectname].Name
            if type=='PBlock':
                linelist=self.Objects[objectname].TellLines()
                newlinelist=[0]*len(linelist)
                for i in range(len(linelist)):
                    linelist[i]=linemap.index(linelist[i])
                linestr='lines|'+str(linelist)
            elif type=='PTurnTable':
                linelist=self.Objects[objectname].TellLines()
                newlinelist=[[linemap.index(line.Number) for line in lines] for lines in linelist]
                circlelist=self.Objects[objectname].TellCircles()
                newcirclelist=[circlemap.index(circle.Number) for circle in circlelist]
                linestr='circles|' + str(newcirclelist) + '||lines|' + str(newlinelist)
            else:
                linelist0, linelist1=self.Objects[objectname].TellLines()
                newlinelist0=[0]*len(linelist0)
                newlinelist1=[0]*len(linelist1)
                for i in range(len(linelist0)):
                    newlinelist0[i]=linemap.index(linelist0[i])
                for i in range(len(linelist1)):
                    newlinelist1[i]=linemap.index(linelist1[i])
                linestr='lines0|'+str(newlinelist0)+'||lines1|'+str(newlinelist1)
            string=type+'||name|"'+name+'"||'+linestr+'\n'
            file.write(string)

    def SetMode(self, event=None, mode=None):
        if mode==None:
            if self.Mode=='Run':
                self.Mode='Edit'
            elif self.Mode=='Edit':
                self.Mode='Run'
        else:
            self.Mode=mode

        for pointname in self.points.keys():
            self.points[pointname].SetMode()
        for objectname in self.Objects.keys():
            self.Objects[objectname].SetMode()

    def Restack(self):
##        self.cv.lower('Point') ## These go on top!
        self.cv.lower('LabelText')
        self.cv.lower('LabelMask')
        self.cv.lower('Arrow')
        self.cv.lower('Line')
        self.cv.lower('LabelBox')

class PTrackEditor:
    def __init__(self, master, filename=None):
        self.Master=master
        self.EditWindow=Toplevel(self.Master.root)
        self.EditWindow.protocol("WM_DELETE_WINDOW", self.CloseEditor)


        self.scv=Pmw.ScrolledCanvas(self.EditWindow, canvasmargin=100)
        self.scv.pack(side=TOP, fill='both', expand='true')
        self.scv.configure(hscrollmode='dynamic', vscrollmode='dynamic')

        self.cv=self.scv.interior()

        self.PTM=PTrackManager(self.Master, self, self.scv)
        self.PTM.SetMode(mode='Edit')

        self.Menubar=Menu(self.EditWindow)

        # File Menu
        self.FileMenu=Menu(self.Menubar, tearoff=0)
        self.FileMenu.add_command(label='Load Display', command=self.LoadDisplay)
        self.FileMenu.add_command(label='Save Display', command=self.SaveDisplay)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label='Exit', command=self.CloseEditor)
        self.Menubar.add_cascade(label="File", menu=self.FileMenu)

        # Edit Menu
        self.EditMenu=Menu(self.Menubar, tearoff=0)
        self.EditMenu.add_command(label='m, Change mode', command=self.PTM.SetMode)
        self.EditMenu.add_command(label='w, Select by box', command=self.PTM.DrawCross)
        self.EditMenu.add_command(label='r, Select by horizontal line', command=self.PTM.DrawHorizontal)
        self.EditMenu.add_command(label='e, Select by vertical line', command=self.PTM.DrawVertical)
        self.EditMenu.add_command(label='u, Unselect all points', command=self.PTM.Unselect)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label='Delete blue points', command=lambda event=None: self.PTM.DeleteSelected(0))
        self.EditMenu.add_command(label='Delete green points', command=lambda event=None: self.PTM.DeleteSelected(1))
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label='a, Increase scale', command=lambda event=None: self.PTM.ChangeScale(1.1))
        self.EditMenu.add_command(label='z, Decrease scale', command=lambda event=None: self.PTM.ChangeScale(1/1.1))
        self.Menubar.add_cascade(label="Edit", menu=self.EditMenu)

        self.EditWindow.config(menu=self.Menubar)

        self.EditWindow.bind('m', self.PTM.SetMode)
        self.EditWindow.bind('w', self.PTM.DrawCross)
        self.EditWindow.bind('r', self.PTM.DrawHorizontal)
        self.EditWindow.bind('e', self.PTM.DrawVertical)
        self.EditWindow.bind('u', self.PTM.Unselect)
        self.EditWindow.bind('i', self.PTM.AddTextPoint)
        self.EditWindow.bind('a', lambda x: self.PTM.ChangeScale(1.1))
        self.EditWindow.bind('z', lambda x: self.PTM.ChangeScale(1/1.1))
        self.Window=self.EditWindow

    def LoadDisplay(self):
        filename=tkFileDialog.askopenfilename(parent=self.EditWindow)
        self.PTM.LoadDisplay(filename=filename)

    def SaveDisplay(self):
        file=tkFileDialog.asksaveasfile(parent=self.EditWindow)
        if file!=None:
            self.PTM.SaveDisplay(file=file)

    def CloseEditor(self, event=None):
        self.PTM.DeleteAll()
        self.EditWindow.destroy()

if __name__=='__main__':
    root=Tk()
    cv=Canvas(root, bg='Black')
    cv.pack(side=TOP, fill=BOTH, expand=1)
    pm=PLineManager(cv)
    root.bind('a', lambda x: pm.ChangeScale(1.1))
    root.bind('z', lambda x: pm.ChangeScale(1/1.1))

    root.mainloop()
