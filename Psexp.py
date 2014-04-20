# Thomas O'Reilly, 2 March 2002
#
# TMRC system 3 display software component: Psexp.py
#
# Basic class to hold data from parsed s-expressions.  Only the command name variable is
# declared here.  The others are filled in as needed.
class ParsedSexp:
    command=''
    sexp=''

def makeToken(s):
    if s == '#t':
        return True
    if s == '#f':
        return False
    if s == 'nil':
        return None
    
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return Symbol(s)
    
class Symbol(str):
    __slots__=[]

    def __new__(self, s):
        return str.__new__(self, s.lower())

    def __repr__(self):
        return self
    
class _Notifier:
    def __init__(self, fun):
        self.fun = fun
        
    def append(self, obj):
        self.fun(obj)

nonatomchars=' \n\r\t()"{}'

NORMAL, IN_TOKEN, IN_QUOTE = range(3)

class Parser:
    def __init__(self, sexpFinished):
        self.partials = []
        self.state=NORMAL
        self.partialstr=""

        # Trying to append to the toplevel actually triggers the
        # callback function, instead of appending anything.
        self.partials.append(_Notifier(sexpFinished))
        
    def parse(self, data):
        """Incrementally parse data, which is a string containing some part of
        a stream of S-exprs. When a full sexpr is matched, call the
        sexprFinished method passed into __init__.

        This uses a state machine to keep track of where in the parsing it is.
        """
        
        for c in data:
            if self.state == IN_QUOTE:
                if c=='"':
                    self.partials[-1].append(self.partialstr)
                    self.partialstr=''
                    self.state=NORMAL
                else:
                    self.partialstr+=c
            elif self.state == IN_TOKEN:
                if c in nonatomchars:
                    self.partials[-1].append(makeToken(self.partialstr))
                    self.partialstr=''
                    self.state=NORMAL
                    self.parse(c) # reparse in new state
                else:
                    self.partialstr+=c
            else:
                if c == '(':
                    self.partials.append([])
                elif c == ')':
                    if len(self.partials) == 1:
                        raise Exception("Extra closing paren.")
                    sexp = self.partials.pop()
                    self.partials[-1].append(sexp)
                elif c == '"':
                    self.state=IN_QUOTE
                elif c in ' \t\n\r':
                    pass
                elif c not in nonatomchars:
                    self.state=IN_TOKEN
                    self.parse(c) # reparse in new state
                else:
                    raise Exception("Unknown character '%s' parsing sexp", c)
    
