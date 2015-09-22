## Benches

from lib.inductor.rf import sp as Sp
from syntax import *
from functions.science import linspace

@setenv(type='bench', name='sp1')
class sp1():
    def __init__(self, **parameters):
        ls = parameters.get('ls', 1e-9)
        rs = parameters.get('rs', 1.0)
        cp = parameters.get('cp', 150e-15)
        cs = parameters.get('cs', 30e-15)
        rac = parameters.get('rac', 1)
        ldc = parameters.get('ldc', 1e-9)
        k1 = parameters.get('k1', 0.9)
        rsub = parameters.get('rsub', 1)

        freq = linspace(0.1e9, 15e9, 101)
        
        lib = myinductor(name='myinductor', rs=rs, ls=ls, cp=cp, cs=cs, rac=rac, ldc=ldc, 
                                            k1=k1, rsub=rsub)
        dev = Device(model='myinductor', nodes=('plus', 'minus', '0'))
        cir1 = Sp(library=lib, device=dev, freq=freq)
        cir1.simulate(verbose=True)
        y11, y12, y21, y22 = cir1.Y()

        self.freq = freq
        self.l11 = (1.0/y11).imag/(2.0*pi*freq)
        self.r11 = (1.0/y11).real
        self.q11 = (1.0/y11).imag/(1/y11).real

@setenv(type='bench', name='sp2')
class sp2():
    def __init__(self, **parameters):
        freq = linspace(0.1e9, 15e9, 101)
        dev = Nport(nodes=('plus', '0', 'minus', '0'), file='./examples/MyInductor/mydata.s2p')
        cir1 = Sp(device=dev, freq=freq)
        cir1.simulate(verbose=True)
        y11, y12, y21, y22 = cir1.Y()

        self.freq = freq
        self.l11 = (1.0/y11).imag/(2.0*pi*freq)
        self.r11 = (1.0/y11).real
        self.q11 = (1.0/y11).imag/(1/y11).real

