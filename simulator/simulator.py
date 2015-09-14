__version__ = '0.0.1'

import os, time, re
#import tempfile
from function import tempfile
from ngspice.spice3f5 import rawspice
from subprocess import Popen, PIPE, STDOUT
from function import find, removedirs, source
from config import *


class ngspice(object):
    
    __parameters__ = { 'log':'ngspice.log', 'path':'', 'filename':'ngspice.cir',
                       'debug':False, 'verbose':True}
    try: __parameters__['version'] = VERSION
    except: pass
    source('/home/vraphael/.vraphael/ngspice.tcshrc')

    def __init__(self, netlist='', **parameters):
	self.t0=time.time()
        self.raw = {}
        self.netlist = netlist
        self.__parameters__.update(parameters)
        tempfile.tempdir = TMP
        self.__parameters__['path'] = parameters.get('path', tempfile.mkdtemp(prefix=PREFIX, suffix='/'))

    def run(self):
        filename = os.path.join(self.__parameters__['path'], self.__parameters__['filename'])
        with open(filename,'w') as f:
            f.write(str(self.netlist))
        if self.__parameters__['debug']:
            Popen("{text_editor} {filename}".format(text_editor=TEXT_EDITOR, filename=filename), stdout=PIPE, stderr=STDOUT, shell=True).communicate()
        if self.__parameters__['verbose']: 
	    print '** NgSpice circuit Simulator is running at {time}...'.format(time=time.strftime("The %b %d %Y at %H:%M:%S"))
	    print '**     Simulating {filename} - `{title}`'.format(filename=filename, title=str(self.netlist).splitlines()[0][2:])
	cmd = ["cd %s;"%(self.__parameters__['path']), NGSPICE, '-b']
        if self.__parameters__['log']:
	    log = self.__parameters__['log']
            cmd.append('-o {log}'.format(log=log))
        cmd.append(filename)
        start = time.time()
        p = Popen(" ".join(cmd), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, env=os.environ)
        stdout = p.communicate()[0]
        end = time.time()
	with open(os.path.join(self.__parameters__['path'], log)) as f:
	    stdlog = f.read().lower()
	if 'error' in stdlog or 'error' in stdout:
	    raise Exception("NgSpice was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], log))
        if self.__parameters__['verbose']: 
	    print '** NgSpice  completes the simulation in {time:.2f}s.'.format(time=(end-start))
        if hasattr(self.netlist, 'getRawFiles'):
            for pattern in self.netlist.getRawFiles():
	        outfile = os.path.join(self.__parameters__['path'], pattern)
	        if not os.path.isfile(outfile):
		    raise Exception("NgSpice was terminated due to a fatal error. \n           Please check the logfile : %s"%os.path.join(self.__parameters__['path'], log))
                self.raw[pattern] = rawspice(outfile).read()
        if hasattr(self.netlist, 'postSimulation'):
	    self.netlist.postSimulation(self)
        if self.__parameters__['verbose']:
	    print '** NgSpice Raw files has been succefully extracted.'
	    print
        return self



