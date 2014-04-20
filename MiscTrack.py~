# Thomas O'Reilly, 26 March 2002
# Assorted objects and other definitions for block and switch displays

# Track and switch related constants
RIGHTHAND=0; LEFTHAND=1 # Switch handedness
OCC=0; UNOCC=1; OWNED=2; ADVBLOCK=3; LOCO=4 # Occupancy status for display purposes
OFFLINE=0; OUTOFSERVICE= 1; ONLINE=2; INACC=3 # Block online/offline/inaccessible for display purposes

offlinecolor = '#806060'
outofservicecolor = '#8888FF'

# Display Colors
blkcolor={ONLINE :{OCC:'#448844', UNOCC:'#FFFFFF', LOCO:'#88FF88', OWNED:'#FF0000', ADVBLOCK:'#FF8888'},
          OUTOFSERVICE:{OCC:outofservicecolor, UNOCC:outofservicecolor, LOCO:outofservicecolor, OWNED:outofservicecolor, ADVBLOCK:outofservicecolor},
          INACC  :{OCC:'#707070', UNOCC:'#707070', LOCO:'#707070', OWNED:'#707070', ADVBLOCK:'#707070'},
          OFFLINE  :{OCC:offlinecolor, UNOCC:offlinecolor, LOCO:offlinecolor, OWNED:offlinecolor, ADVBLOCK:offlinecolor}}

# Signal colors
sigcolor={'stop':'Red', 'restrict':'Yellow', 'go':'Green',
          'clear':'Green', 'app-med':'Green', 'app-slow':'Green',
          'med-clear':'Green', 'med-app-med':'Green', 'med-app-slow':'Green',
          'app':'Yellow', 'med-app':'Yellow', 'slow-clear':'Yellow',
          'restrict':'Yellow', 'unknown': 'White'}

# Label colors
slabelcolor={'text':'Black', 'bg':'White', 'ol':'Black', 'ext':'White'}
blabelcolor={'text':'White', 'bg':'Black', 'ol':'White', 'ext':'White'}

labelrad=10
labelextlen=5

# Definitions of stuff for block definition process
END0=0; END1=1; TWOPOINT=2; EXPOINT=3
EAST=0; EASTEAST=2; WEST=1; WESTWEST=3

# Stuff for display line styles
SMOOTH=False

# Initial and minimum sizes for stuff
basescale=25

basesizedic={ONLINE:7, OFFLINE:7, INACC:3,
             'labelsize':25, 'borderspace':2, 'borderwidth':0}

minsizedic={ONLINE:1, OFFLINE:1, INACC:1,
            'labelsize':10, 'borderspace':1, 'borderwidth':0}

maxsizedic={ONLINE:7, OFFLINE:7, INACC:3,
            'labelsize':25, 'borderspace':2, 'borderwidth':0}

# Line width definitions
activewidth=4
inactivewidth=1

# Text size definitions
blocklabeltext=18
blocklabelfont='Arial'
blocklabelstyle='bold'
switchlabeltext=18
switchlabelfont='Arial'
switchlabelstyle='bold'

# Assorted data holding structures
class ConObj:
    def __init__(self):
        self.Signal='stop'
        self.Object=None
        self.ObjType=None
        self.ObjCon=-1
        self.magic=False
        self.gap=False

    def SetGap(self, gap):
        if gap in ('#t', True):
            self.gap=True
        elif gap in ('#f', False):
            self.gap=False
        else:
            print 'Confusion reigns in MiscTrack, SetGap', gap
