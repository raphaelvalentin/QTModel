# -*- type: bench -*-

from lib.inductor.rf import sp as Sp
from syntax import *

@setenv(type="bench", name='sp1')
class sp1():
    def __init__(self, **parameters):
        ls = parameters.get('ls', 1e-9)
        rs = parameters.get('rs', 2.0)
        cp = parameters.get('cp', 50e-15)
        cs = parameters.get('cs', 200e-15)
        rsub = parameters.get('rsub', 1000.)
        freq = linspace(0.1e9, 12e9, 101)
        
        lib = myinductor(name='myinductor', rs=rs, ls=ls, cp=cp, cs=cs, rsub=rsub)
        dev = Device(model='myinductor', nodes=('plus', 'minus'))
        cir1 = Sp(library=lib, device=dev, freq=freq)
        cir1.simulate(verbose=True)

        # output
        self.freq = freq
        self.l11 = cir1.L11()
        self.r11 = cir1.R11()
        self.q11 = cir1.Q11()


@setenv(type="bench", name='sp2')
class sp2():
    def __init__(self, **parameters):
        ls =  1e-9
        rs =  2.0
        cp =  50e-15
        cs =  200e-15
        rsub = 1000.
        freq = linspace(0.1e9, 12e9, 101)
        
        lib = myinductor2(name='myinductor', rs=rs, ls=ls, cp=cp, cs=cs, rsub=rsub)
        dev = Device(model='myinductor', nodes=('plus', 'minus'))
        cir1 = Sp(library=lib, device=dev, freq=freq)
        cir1.simulate(verbose=True)

        # output
        self.freq = freq
        self.l11 = cir1.L11()
        self.r11 = cir1.R11()
        self.q11 = cir1.Q11()