# TMRC System 3 Software Cab
# Thomas O'Reilly, 27 June 2002
# Program options and functions to handle them

class Options:
    """Class to handle program options

    This is supposed to handle whatever options a program may need
    to run properly and provide an easy way to manage them."""

    def __init__(self, master):
        self.master=master
        self.types={}
        self.desc={}
        self.defval={}
        self.SetDefs()

    def SetDefs(self):
        self.AddOpt('displaytype', 'dispatch', str, 'Type of display console')
        self.AddOpt('initialgeom', '800x600+100+100', str, 'Initial window geometry')
        self.AddOpt('bg', '#BBBBBB', str, 'Widget background color')
        self.AddOpt('fg', '#000000', str, 'Widget foreground color')
        self.AddOpt('loglevel', 3, int, 'Logging message level')
        self.AddOpt('enableinertia', 1, int, 'Show inertian controls')
        self.AddOpt('miniscab', 0, int, 'Make the SCab window small?')
        self.AddOpt('layoutfile', 'full.nlay', str, 'Layout file')
    
    def ProcSexp(self, Psexp):
        sexp = Psexp.new_sexp
        if sexp[0]=='set':
            self.SetOpt(sexp[1][1], sexp[2])
        else:
            self.master.logger.LogWarnMsg('Unknown option command :',sexp[0],
                                          ' in ', sexp)

    def AddOpt(self, optname, defval, valtype='string',
               desc='To be written'):
        """Add new option to option structure"""
        self.types[optname]=valtype
        self.desc[optname]=desc
        self.defval[optname] = defval
        setattr(self, optname, defval)

    def SetOpt(self, optname, value):
        """Set option value.

        Takes two arguments, both required, the name of option, which is a string,
        and the value, which may be a string or number, as appropriate.  If
        the value is a number, it can be passed as either a number or string."""
        if self.types.has_key(optname):
            valtype=self.types[optname]
            if not isinstance(value, valtype):
                self.master.logger.LogWarnMsg('Option value %s does not match '
                                              'declared type %s for option %s.' %
                                              (value_str, valtype, optname))
            else:
                setattr(self, optname, value)
        else:
            self.master.logger.LogWarnMsg('Unknown option '+optname)
