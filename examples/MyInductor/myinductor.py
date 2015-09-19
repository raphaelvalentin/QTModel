# -*- type: model -*-

@setenv(type='model', name='myinductor')
class myinductor(Netlist):
    def __init__(self, name='myinductor', ls=1e-9, rs=1.0, cp=100e-15, cs=20e-15, rsub=100):
        subckt1 = []
        subckt1.append( Inductor(name='ls1', nodes=('1', '2'), l=0.5*ls) )
        subckt1.append( Resistor(name='rs1', nodes=('2', '3'), r=0.5*rs) )
        subckt1.append( Capacitor(name='cs1', nodes=('1', '3'), c=2*cs) )

        subckt1.append( Resistor(name='rs2', nodes=('3', '4'), r=0.5*rs) )
        subckt1.append( Inductor(name='ls2', nodes=('4', '5'), l=0.5*ls) )
        subckt1.append( Capacitor(name='cs2', nodes=('3', '5'), c=2*cs) )

        subckt1.append( Capacitor(name='cp1', nodes=('1', '6'), c=0.25*cp) )
        subckt1.append( Resistor(name='rsub1', nodes=('6', '0'), r=4*rsub) )
        subckt1.append( Capacitor(name='cp2', nodes=('3', '7'), c=0.5*cp) )
        subckt1.append( Resistor(name='rsub2', nodes=('7', '0'), r=2*rsub) )
        subckt1.append( Capacitor(name='cp3', nodes=('5', '8'), c=0.25*cp) )
        subckt1.append( Resistor(name='rsub3', nodes=('8', '0'), r=4*rsub) )

        self.append( Subckt(name=name, nodes=('1', '5'), childs=subckt1) )

@setenv(type='model', name='myinductor2')
class myinductor2(Netlist):
    def __init__(self, name='myinductor', ls=1e-9, rs=1.0, cp=100e-15, cs=20e-15, rsub=100):
        subckt1 = []
        subckt1.append( Inductor(name='ls1', nodes=('1', '2'), l=ls) )
        subckt1.append( Resistor(name='rs1', nodes=('2', '3'), r=rs) )
        subckt1.append( Capacitor(name='cs1', nodes=('1', '3'), c=cs) )

        subckt1.append( Capacitor(name='cp1', nodes=('1', '4'), c=0.5*cp) )
        subckt1.append( Resistor(name='rsub1', nodes=('4', '0'), r=2*rsub) )
        subckt1.append( Capacitor(name='cp2', nodes=('3', '5'), c=0.5*cp) )
        subckt1.append( Resistor(name='rsub2', nodes=('5', '0'), r=2*rsub) )

        self.append( Subckt(name=name, nodes=('1', '3'), childs=subckt1) )