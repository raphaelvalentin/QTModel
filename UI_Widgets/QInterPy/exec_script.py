#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from math import *
from ngspice.syntax import *
from ngspice.simulator import *
from syntax import *

ENVIRON = {k:v for k,v in globals().iteritems()}

import code
from cStringIO import StringIO

__all__= ['Interpy']

class Interpy(code.InteractiveInterpreter):

    ENVIRON = ENVIRON
    
    def __init__(self, locals={}):
        ENVIRON = Interpy.ENVIRON
        if isinstance(locals, dict):
            ENVIRON.update(locals)
        code.InteractiveInterpreter.__init__(self, locals=ENVIRON)

    def runcode(self, code):
        try:
            exec code in self.locals
        except:
            self.showtraceback() 

 
