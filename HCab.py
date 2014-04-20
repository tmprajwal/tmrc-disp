# TMRC System 3 Software Cab
# Thomas O'Reilly, 4 May 2002

class HCab:
    """Class to hold information related to hardware cabs.

    Objects of this type are created by the main Picker object
    in response to add commands from the server."""
    def __init__(self, master, name):
        """Initialization function

        Requires the name of the hardware cab (provided by the
        server) and a reference to the main Picker object."""
        self.Owner=None
        self.Master=master
        self.Name=name

    def SetOwner(self, owner=None):
        """Owner setting method.

        Is used to assign an owner (train) to the hardware cab in response
        to server messages.  Also calls the SCab object corresponding to the
        train, to let it know that a HCab has been assigned."""
        if owner==None:
            if self.Owner!=None:
                self.Owner.NewHCab(None)
                self.Owner=None
        elif self.Master.TrainList.has_key(owner):
            owner=self.Master.TrainList[owner]
            self.Owner=owner
            self.Owner.NewHCab(self)
        else:
            print 'Failed to set HCab ', self.Name, 'owner to unknown train ', owner

    def Delete(self):
        """HCab deletion method.

        This should be called before an HCab is deleted to let the associated
        SCab, if any, know that the HCab has been deleted."""
        if self.Owner!=None:
            self.Owner.NewHCab(None)

    def ProcSexp(self, Psexp):
        """S-expression processing method.

        This method is used to process all server messages dealing with this
        HCab (except add and delete messsges).  The only type of message it
        can currently handle is messages to set the owner."""
        if Psexp.tokens[2]=='train':
            if Psexp.tokens[3]=='nil':
                self.SetOwner(None)
            else:
                self.SetOwner(Psexp.tokens[3][1])
        else:
            print 'Unparsed S-exp: '+Psexp.sexp
            print 'HCab object variable type "'+Psexp.tokens[2]+'" unknown and ignored'
