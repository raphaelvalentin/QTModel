## Benches

from lib.inductor.rf2 import sp as Sp
from lib.inductor.rf2 import ytoz, ztoy, dB
from libarray import array


from syntax import *


@Bench(name='sp1')
class sp1():
    def __init__(self, **parameters):
        ls = parameters.get('ls', 1e-9)
        rs = parameters.get('rs', 1.0)
        cp = parameters.get('cp', 150e-15)
        cs1 = parameters.get('cs1', 30e-15)
        cs2 = parameters.get('cs2', 30e-15)
        cs3 = parameters.get('cs3', 30e-15)
        rac = parameters.get('rac', 1)
        ldc = parameters.get('ldc', 1e-9)
        k1 = parameters.get('k1', 0.9)
        k2 = parameters.get('k2', 0.1)
        k3 = parameters.get('k3', 0.1)
        rsub = parameters.get('rsub', 1)
        rpattern = parameters.get('rpattern', 1)
        cp2 = parameters.get('cp2', 1.0e-15)
        rsubp2 = parameters.get('rsubp2', 65)

        outerdiameter = parameters.get('outerdiameter', 200.0)
        width = parameters.get('width', 9.99)
        spacing = parameters.get('spacing', 2.01)

        freq = linspace(0.1e9, 15e9, 101)
        
        lib = myinductor(name='myinductor', rs=rs, ls=ls, cp=cp, cs1=cs1, cs2=cs2, cs3=cs3, rac=rac, ldc=ldc, 
                                            k1=k1, k2=k2, k3=k3, rpattern=rpattern, rsub=rsub, cp2=cp2, 
                                            rsubp2=rsubp2, outerdiameter=outerdiameter, width=width, spacing=spacing)
        dev = Device(model='myinductor', nodes=('plus', 'minus', '0'))
        cir1 = Sp(library=lib, device=dev, freq=freq, withline=True)
        cir1.simulate(verbose=True)

        y11, y12, y21, y22 = cir1.Y()
        z11, z12, z21, z22 = cir1.Z()
        freq = array(freq)


        self.freq = freq
        self.l11 = (1.0/y11).imag/(2.0*pi*freq)
        self.r11 = (1.0/y11).real
        self.q11 = (1.0/y11).imag/(1/y11).real
        self.l22 = (1.0/y22).imag/(2.0*pi*freq)
        self.r22 = (1.0/y22).real
        self.q22 = (1.0/y22).imag/(1/y22).real

        zdiff = z11 - z12 - z21 + z22
        self.ldiff = zdiff.imag/(2.0*pi*freq)
        self.rdiff  = zdiff.real
        self.qdiff = zdiff.imag/zdiff.real

        # When terminal1 and terminal2 share the same port (extract CAP from metal lines to Substrate)	
        ycap = y11 + y12 + y21 + y22
        self.c11 = -1.0/(2.0*pi*freq*(1.0/ycap).imag)
        self.r11b = (1.0/ycap).real
        self.dbs11 = dB( (1.0 - ycap*50.)/(1.0 + ycap*50.) )

      


@Bench(name='sp2')
class sp2():
    def __init__(self, **parameters):
        freq = linspace(0.1e9, 15e9, 101)
        
        from doe import data
        nturn = 2; diameter = parameters.get('outerdiameter', 200.0); 
        width = parameters.get('width', 10.0); spacing = parameters.get('spacing', 2); 
        for row in data:
             if float(row['nturn']) == float(nturn):
                 if float(row['diameter']) == float(diameter):
                     if -0.02<float(row['width'])-float(width)<0.02:
                         if -0.02<float(row['spacing'])-float(spacing)<0.02:
                             filename = row['filename']
        path = './Projects/Stacked-Ass/s2p/'
        dev = Nport(nodes=('plus', '0', 'minus', '0'), file=path+filename)
        cir1 = Sp(device=dev, freq=freq)
        cir1.simulate(verbose=True)
        y11, y12, y21, y22 = cir1.Y()
        z11, z12, z21, z22 = cir1.Z()
        freq = array(freq)


        self.freq = freq
        self.l11 = (1.0/y11).imag/(2.0*pi*freq)
        self.r11 = (1.0/y11).real
        self.q11 = (1.0/y11).imag/(1/y11).real
        self.l22 = (1.0/y22).imag/(2.0*pi*freq)
        self.r22 = (1.0/y22).real
        self.q22 = (1.0/y22).imag/(1/y22).real

        zdiff = z11 - z12 - z21 + z22
        self.ldiff = zdiff.imag/(2.0*pi*freq)
        self.rdiff  = zdiff.real
        self.qdiff = zdiff.imag/zdiff.real

        # When terminal1 and terminal2 share the same port (extract CAP from metal lines to Substrate)	
        ycap = y11 + y12 + y21 + y22
        self.c11 = -1.0/(2.0*pi*freq*(1.0/ycap).imag)
        self.r11b = (1.0/ycap).real
        self.dbs11 = dB( (1.0 - ycap*50.)/(1.0 + ycap*50.) )

           
        



