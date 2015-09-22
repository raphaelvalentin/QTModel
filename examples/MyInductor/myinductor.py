### first tentative model

@setenv(type='model', name='myinductor')
class myinductor(Netlist):
    def __init__(self, name='myinductor', ls=1e-9, rs=1.0, cp=100e-15, cs=20e-15, ldc=1e-9, rac=2, k1=0.1, rsub=5):

        PORT1 = 'P1'
        PORT2 = 'P2'
        SUB = 'SUB'

        # netlist
        subckt1 = []
        subckt1.append( Inductor(name='ls1', nodes=(PORT1, '2'), l=ls) )
        subckt1.append( Device(name='xfp1', model='fracpole1', nodes=('2', '3'), rdc=rs, ldc=ldc, rac=rac) )
        subckt1.append( Device(name='xfp2', model='fracpole1', nodes=('3', '4'), rdc=rs, ldc=ldc, rac=rac) )
        subckt1.append( Inductor(name='ls2', nodes=('4', PORT2), l=ls) )

        # Coupling
        subckt1.append( MutualInductor(name='ml1', coupling=k1, ind1='ls1', ind2='ls2') )
        subckt1.append( Capacitor(name='cs1', nodes=(PORT1, '3'), c=cs) )
        subckt1.append( Capacitor(name='cs2', nodes=('3', PORT2), c=cs) )

        # Parallel CAP
        subckt1.append( Capacitor(name='cp1', nodes=(PORT1, '18'), c=cp) )
        subckt1.append( Resistor(name='rsub1', nodes=('18', 'SUB'), r=rsub) )
        subckt1.append( Capacitor(name='cp2', nodes=('3', '19'), c=cp) )
        subckt1.append( Resistor(name='rsub2', nodes=('19', 'SUB'), r=rsub) )
        subckt1.append( Capacitor(name='cp3', nodes=(PORT2, '20'), c=cp) )
        subckt1.append( Resistor(name='rsub3', nodes=('20', 'SUB'), r=rsub ) )

        self.append( Fracpole(name='fracpole1', order=4, symmetry=False, fac=4e9) )
        self.append( Subckt(name=name, nodes=(PORT1, PORT2, SUB), childs=subckt1) )

