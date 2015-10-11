from ngspice import *
from ngspice.syntax import Nport
from libarray import *
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
	
        # default sparam netlist attached to the class
	self.append( Title(title='s-param curve'))
        self.append( Global(nodes=('0')) )
        self.append( self.library )
        self.append( self.device )
	
	self.append( Port(name='p1', nodes=('plus', '0')) )
	self.append( Port(name='p2', nodes=('minus', '0')) )
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
	return -(1/x['y12']).imag/2.0/pi/x['freq']
	return x['z11'].imag/2.0/pi/x['freq']
	
    def R11(self):
        x = self.raw['sp1.sp']
	return -(1/x['y12']).real

    def Q11(self):
        x = self.raw['sp1.sp']
	return (1/x['y12']).imag/(1/x['y12']).real
	
    def L22(self):
        x = self.raw['sp1.sp']
        return x['z22'].imag/2.0/pi/x['freq']
	
    def R22(self):
        x = self.raw['sp1.sp']
        return x['z22'].real 

    def Q22(self):
        x = self.raw['sp1.sp']
        return x['z22'].imag/x['z22'].real 

    def M12(self):
        x = self.raw['sp1.sp']
        return x['z12'].imag/sqrt(x['z11'].imag*x['z22'].imag) 
	
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


class sp2(Netlist):
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
	
        # default sparam netlist attached to the class
	self.append( Title(title='s-param curve'))
        self.append( Global(nodes=('0')) )
        self.append( self.library )
        self.append( self.device )
	
	self.append( Port(name='p1', nodes=('plus', '0')) )
	self.append( Vsource(name='v0', nodes=('plus', 'minus'), dc=0) )
	self.append( Vsource(name='v1', nodes=('plus', 'ct'), dc=0) )
	
        self.append( Control() )
	for freqi in self.freq :
	    if isinstance(self.device, Nport):
	        self.append( self.device.alter(freqi) )
  	    self.append( Sp(name='sp1', ports=['p1'], freq=freqi) )
        self.append( Endc() )
        self.append( End() )

    def C11(self):
        x = self.raw['sp1.sp']
        return x['y11'].imag/2.0/pi/x['freq']

    def dBS11(self):
        x = self.raw['sp1.sp']
	return dB(x['s11'])

    def S(self):
        x = self.raw['sp1.sp']
        s11 = x['s11']
        return array([s11])

    def Y(self):
        x = self.raw['sp1.sp']
        y11 = x['y11']
        return array([y11])

    def Z(self):
        x = self.raw['sp1.sp']
        z11 = x['z11']
        return array([z11])

