#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from math import *
from ngspice.syntax import *
from ngspice.simulator import *
from syntax import Bench

ENVIRON = {k:v for k,v in globals().iteritems()}

import sys, os
import code
from cStringIO import StringIO

__all__= ['Interpy']

class Interpy(code.InteractiveInterpreter):

    ENVIRON = ENVIRON
    
    def __init__(self, locals={}):
        env = Interpy.__env__
        if isinstance(locals, dict):
            env.update(locals)
        code.InteractiveInterpreter.__init__(self, locals=env)

    def runcode(self, code):
        try:
            exec code in self.locals
        except:
            self.showtraceback() 

    def environ(self):
        return self.__dict__['locals']

       

