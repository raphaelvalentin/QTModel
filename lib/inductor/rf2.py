from ngspice import *
from ngspice.syntax import Nport
from numpy import *
dB = lambda x: 20.*log10(abs(x))



class sp(Netlist):
    __name__ = "sparam"
    __type__ = "netlist"
    
    def __init__(self, name='sp', **parameters):
        # name of the netlist
        self.name = name
        # set default parameters
        
        # set parameters from mos
	self.library = parameters.get('library', Netlist())
        self.device    = parameters.get('device', Device(name='L0'))
        # set parameters from __init__
        self.freq   = parameters.get('freq', [1e9])

        self.withline   = parameters.get('withline', False)

	
        # default sparam netlist attached to the class
        self.append( Title(title='s-param curve'))
        self.append( Global(nodes=('0')) )
        self.append( self.library )
        self.append( self.device )

        if self.withline:
            GND1 = 'LINE1'
            GND2 = 'LINE2'
            # LINE1
            path = '/media/raphael/8013-D98E/Work/python-lib/optimize2/QToptim_x/Projects/Stacked-Ass/'
            self.append( Nport(nodes=(GND1, '0', '0', '0'), file=path+"line1.s2p") )
            self.append( Nport(nodes=(GND2, '0', '0', '0'), file=path+"line2.s2p") )
        else:
            GND1 = '0'
            GND2 = '0'


	
        self.append( Port(name='p1', nodes=('plus', GND1)) )
        self.append( Port(name='p2', nodes=('minus', GND2)) )
        self.append( Vsource(name='v0', nodes=('ct', '0'), dc=0) )
	
        self.append( Control() )
	for freqi in self.freq :
	    if isinstance(self.device, Nport):
	        self.append( self.device.alter(freqi) )
  	    self.append( Sp(name='sp1', ports=['p1', 'p2'], freq=freqi) )
        self.append( Endc() )
        self.append( End() )
	    
    
    def dBS11(self):
        x = self.raw['sp1.sp']
        return dB(x['s11'])
    
    def dBS12(self):
        x = self.raw['sp1.sp']
        return dB(x['s12'])

    def L11(self):
        x = self.raw['sp1.sp']
        return (1/x['y11']).imag/2.0/pi/x['freq']

    def R11(self):
        x = self.raw['sp1.sp']
        return (1/x['y11']).real

    def Q11(self):
        x = self.raw['sp1.sp']
        return (1/x['y11']).imag/(1/x['y11']).real

    def L22(self):
        x = self.raw['sp1.sp']
        return (1/x['y22']).imag/2.0/pi/x['freq']

    def R22(self):
        x = self.raw['sp1.sp']
        return (1/x['y22']).real

    def Q22(self):
        x = self.raw['sp1.sp']
        return (1/x['y22']).imag/(1/x['y22']).real


    def LDIFF(self):
        x = self.raw['sp1.sp']
        z11, z12, z21, z22 = x['z11'], x['z12'], x['z21'], x['z22']
        zdiff = z11-z12-z21+z22
        return zdiff.imag/2.0/pi/x['freq']

    def RDIFF(self):
        x = self.raw['sp1.sp']
        z11, z12, z21, z22 = x['z11'], x['z12'], x['z21'], x['z22']
        zdiff = z11-z12-z21+z22
        return zdiff.real

    def QDIFF(self):
        x = self.raw['sp1.sp']
        z11, z12, z21, z22 = x['z11'], x['z12'], x['z21'], x['z22']
        zdiff = z11-z12-z21+z22
        return zdiff.imag/zdiff.real

    # When terminal1 and terminal2 share the same port (extract CAP from metal lines to Substrate)	
    def C11(self):
        x = self.raw['sp1.sp']
        y11 = x['y11'] + x['y12'] + x['y21'] + x['y22']
        return -1.0/(2.0*pi*x['freq']*(1.0/y11).imag)

    def R11B(self):
        x = self.raw['sp1.sp']
        y11 = x['y11'] + x['y12'] + x['y21'] + x['y22']
        return (1.0/y11).real

    def dBS11(self, z0=50.):
        x = self.raw['sp1.sp']
        y11 = x['y11'] + x['y12'] + x['y21'] + x['y22']
        y0 = 1./z0
        s11 = (y0-y11)/(y0+y11) 
        return dB(s11)

    def S(self):
        x = self.raw['sp1.sp']
        s11, s12, s21, s22 = x['s11'], x['s12'], x['s21'], x['s22']
        return array([s11, s12, s21, s22])

    def Y(self):
        x = self.raw['sp1.sp']
        y11, y12, y21, y22 = x['y11'], x['y12'], x['y21'], x['y22']
        return array([y11, y12, y21, y22])

    def Z(self):
        x = self.raw['sp1.sp']
        z11, z12, z21, z22 = x['z11'], x['z12'], x['z21'], x['z22']
        return array([z11, z12, z21, z22])

def ytoz(Y):
    [y11, y12, y21, y22] = Y
    det = y11*y22 - y12*y21
    z11 = y22/det
    z12 = -y12/det
    z21 = -y21/det
    z22 = y11/det
    return array([z11, z12, z21, z22])

def ztoy(Z):
    [z11, z12, z21, z22] = Z
    det = z11*z22 - z12*z21
    y11 = z22/det
    y12 = -z12/det
    y21 = -z21/det
    y22 = z11/det
    return array([y11, y12, y21, y22])



