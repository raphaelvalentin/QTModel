#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from math import *
from ngspice.syntax import *
from ngspice.simulator import *

__env__ = {k:v for k,v in globals().iteritems()}

import sys, os
import code
from cStringIO import StringIO

__all__= ['Interpy']

class Interpy(code.InteractiveInterpreter):

    __env__ = __env__

    def __init__(self, locals={}):
        env = Interpy.__env__
        if isinstance(locals, dict):
            env.update(locals)
        
        code.InteractiveInterpreter.__init__(self, locals=env)
        self.stdout = ""
        self.stderr = ""

    def runcode(self, code):

        sys.stdout = stdout = StringIO()
        sys.stderr = stderr = StringIO()
 
        try:
            exec code in self.locals
        except SystemExit:
            pass
        except:
            self.showtraceback() 
        finally:
            sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
            self.stdout = stdout.getvalue()
            self.stderr = stderr.getvalue()
            stdout.close()
            stderr.close()



    def context(self):
        return self.__dict__['locals']

       

