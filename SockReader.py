# Thomas O'Reilly, 2 March 2002
#
# TMRC system 3 display component: SockReader.py

import threading
import select
import time
import socket

import Psexp

HOST='tmrc.mit.edu'
PORT=8888
USER='tmrc'

class SockReader(threading.Thread):
    """Main class to read and parse messages from the server

    This defines a class to read a socket connection in a separate thread from
    the main process of the program.  This should keep it from blocking and
    taking up all the time of the program."""

    def __init__(self, master):
        """Initialization method

        This method initializes the thread, and the run method is
        called automatically."""
        threading.Thread.__init__(self)
        self.master=master
        self.ReadQueue=master.ReadQueue
        self.parser = Psexp.Parser(self.sexpFinished)
        self.tries=0

    def sexpFinished(self, sexp):
        self.ReadQueue.put(sexp)
        
    def run(self):
        """Socket reader loop method

        This happy little function uses the select method to determine
        if data is available to be read from the socket connection to the
        server.  If data is available, it is read in 128 byte chunks.  As
        each chunk is read, the program looks to break the incoming data into
        s-expressions by matching parentheses.  When a complete s-exp is
        identified, it is passed to the parser, and the parsed s-exp is
        passed back to the main s-expression handling method in the Picker
        object.

        The select method times out after 0.5 seconds.  The loop runs until
        the Picker object sets StopVar to 0.  The loop the terminates, and
        the StopVar is set to -1, which lets the main routine know that the
        reader thread has stopped, and that the socket may safely be closed.
        The thread should die when this method returns.

        Aside from the two messages involved in the server login process,
        this is the only method to read data from the socket."""
        count=14
        while self.master.StopVar==1:
            if self.master.Sock!=None:
                count=0
                self.read()
            else:
                count+=1
                if count==15:
                    count=0
                    self.OpenSock()
                if self.master.Sock==None:
                    time.sleep(1)

        self.SockClose('requested')
        self.master.StopVar=-1

    def read(self):
        """Socket reader loop method

        This happy little function uses the select method to determine
        if data is available to be read from the socket connection to
        the server.  If data is available, it is read in 1024 byte
        chunks and passed to the sexp parser.  When a complete s-exp
        is identified, it is passed to the parser, the parsed s-exp is
        passed back to the main s-expression handling method in the
        Picker object through ReadQueue.

        The select method times out after 0.5 seconds.  The loop runs until
        the Picker object sets StopVar to 0.  The loop the terminates, and
        the StopVar is set to -1, which lets the main routine know that the
        reader thread has stopped, and that the socket may safely be closed.
        The thread should die when this method returns.

        Aside from the two messages involved in the server login process,
        this is the only method to read data from the socket."""
        rlist, wlist, elist = select.select([self.master.Sock], [], [self.master.Sock], 0.2)
        if len(rlist)==1:
            newlyread=self.master.Sock.recv(1024)
            if len(newlyread)==0:
                self.SockClose('lost')
                self.tries=0
            else:
                try:
                    self.parser.parse(newlyread)
                except:
                    self.SockClose('lost')
                
    def OpenSock(self):
        """Initiates connection to sys3 server using socket interface
        
        Opens a socket connection to the server and logs in.  Then it creates
        a SockReader object which runs in a different thread and starts it. 
        Then it calls the main thread function that handles the messages read
        by the socket reader.
        
        Generally used as a callback, but does not use the 'event' argument"""
        if self.master.Sock!=None:
            self.SockClose()
        try:
            self.tries+=1
            self.master.Sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.master.Sock.connect((HOST,PORT))
            self.master.Sock.setblocking(1)
            recstr=self.master.Sock.recv(0)
#            self.master.SockWrite("tmrc\n")
            self.ReadQueue.put([Psexp.makeToken('socketOpened')])
        except socket.error, msg:
            self.ReadQueue.put([Psexp.makeToken('socketOpenfailed'), self.tries])
            self.master.Sock=None

    def SockClose(self, reason):
        """Stops socket reader thread and closes socket connection.

        If the socket thread is running, this sets variable self.StopVar to
        zero.  The socket reader thread checks this variable occasionally, and
        when it is set to zero (it is normally equal to 1) the thread function
        changes the variable to -1 and exits.  The socket is then closed and set
        to None.

        Generally used as a callback, but does not use the 'event' argument"""
        if self.master.Sock!=None:
            self.master.Sock.close()
            self.master.Sock=None
            if reason=='requested':
                self.ReadQueue.put([Psexp.Symbol('socketClosed')])
            if reason=='lost':
                self.ReadQueue.put([Psexp.Symbol('socketLost')])
            
            
