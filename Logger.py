# TMRC System 3 Display Software
# Message logging functions
# Thomas O'Reilly, 15 June 2002

logcolors={'server':'#00ff00', 'scab':'#0000ff', 'warning':'#ff0000'}

# Message importance levels
LOW=1
MED=2
HIGH=3
NONE=4

# Length of logs
LOGLEN=250
from Tkinter import *

class Logger:
    """Class to log messages from various functions and display them."""

    def __init__(self, master):
        """Logger initialization."""
        self.ServerLog=()
        self.SCabLog=()
        self.WarnLog=()
        self.FullLog=()
        self.FileLog=()
        self.LogSource=()
        self.master=master

    def LogAllMsg(self, message, source, level):
        """Log all messages.

        This function is not called directly, but will
        be called by the functions that log server, SCab and
        warning messages"""
        if len(self.FullLog)<LOGLEN:
            self.FullLog=self.FullLog+(message,)
            self.LogSource=self.LogSource+(source,)
        else:
            self.FullLog=self.FullLog[1:]+(message,)
            self.LogSource=self.LogSource[1:]+(source,)

    def LogServerMsg(self, message, level=MED):
        """Log messages for server messages.

        This function is used to handle messages that have been
        sent to the display program by the server."""
        if level>=self.master.opts.loglevel:
            print ' Server: '+message
        if len(self.ServerLog)<LOGLEN:
            self.ServerLog=self.ServerLog+(message,)
        else:
            self.ServerLog=self.ServerLog[1:]+(message,)
        self.LogAllMsg(message, 'server', level)

    def LogSCabMsg(self, message, level=MED):
        """Log messages for display system messages.

        This function is used to handle messages that have been
        sent to the display program by the server."""
        if level>=self.master.opts.loglevel:
            print '   SCab: '+message
        if len(self.SCabLog)<LOGLEN:
            self.SCabLog=self.SCabLog+(message,)
        else:
            self.SCabLog=self.SCabLog[1:]+(message,)
        self.LogAllMsg(message, 'scab', level)

    def LogWarnMsg(self, message, level=HIGH):
        """Log warning messages from display system.

        This function handles warning messages and exceptions
        in the SCab program."""
        if level>=self.master.opts.loglevel:
            print 'Warning: '+str(message)
        if len(self.WarnLog)<LOGLEN:
            self.WarnLog=self.WarnLog+(message,)
        else:
            self.WarnLog=self.WarnLog[1:]+(message,)
        self.LogAllMsg(message, 'warning', level)

    def LogFileMsg(self, message, level=LOW):
        """Log warning messages from display system.

        This function handles warning messages and exceptions
        in the SCab program."""
        if level>=self.master.opts.loglevel:
            print '   File: '+message
        if len(self.FileLog)<LOGLEN:
            self.FileLog=self.FileLog+(message,)
        else:
            self.FileLog=self.FileLog[1:]+(message,)
        self.LogAllMsg(message, 'file', level)

