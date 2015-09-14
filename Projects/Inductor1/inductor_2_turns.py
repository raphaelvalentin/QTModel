### first tentative model

@Model(name='myinductor')
class myinductor(Netlist):
    def __init__(self, name='myinductor', ls=1e-9, rs=1.0, cp=100e-15, cs1=20e-15, cs2=5e-15, cs3=5e-15, ldc=1e-9, rac=2, k1=0.1, k2=0.1, k3=0.1, rpattern=5, rsub=10, cp2=1e-15, rsubp2=65, outerdiameter=200, width=9.99, spacing=2.01, **kwargs):

        # FIT GLOBAL
        logwidth = log10(width)
        logspacing = log10(spacing)
        k1 = 7.990E-001*(10**(1.516E-002*logwidth-3.610E-002*logspacing))/(1+2.071E+001/outerdiameter)
        k2 = 5.735E-001*(10**(1.673E-001*logwidth-7.396E-002*logspacing))/(1+6.164E+001/outerdiameter)
        k3 = 5.710E-001*(10**(1.361E-001*logwidth-8.678E-002*logspacing))/(1+7.964E+001/outerdiameter)

        #ls = 1.082e-9 * 10**(- 5.007e-3*logspacing - 1.724e-1*logwidth)
        #rac = 6.560e0 * 10**(-1.454e-1*logspacing - 1.957e-1*logwidth)
        #ldc = 1.545e-10*(1 - 3.745e-2*spacing + 4.112e-2*width)
        #cp = 4.911e-13 * 10**(1.674e-1*logspacing - 5.020e-1*logwidth)

        #cs1 = 4.927e-12 * 10**(1.441e-1*logspacing - 1.695e-0*logwidth + 5.592e-1*logwidth*logwidth)
        #rsub = 2.292e0 * (1 - 1.032e-2*spacing + 2.096e-1*width)
        #rpattern = 7.743e-1 * (-1 - 1.112e0*spacing + 1.201e0*width)
        #cs2 = 5e-15
        #cs3 = 1.704e-14 * (1 - 2.121e-1*spacing + 1.043e-1*width)
        #cp2 = 3.020e-14 * (1 + 5.778e-2*spacing - 1.409e-2*width)
        #rsubp2 = 15.0
   
        PORT1 = 'P1'
        PORT2 = 'P2'
        SUB = 'SUB'

        # ls is inductance-value for 1mm
        # cx are capacitance-values for 1mm-length, 10um-width piece line
        # cs1 ~ 500fF for 1mm-length, 10um-width piece line


        # process parameters
        thickness_alpa = 1.45
        thickness_mtt2 = 3.4
        thickness_mt1 = 0.9
        cond_alpa = 30.3
        cond_mtt2 = 59.133
        cond_mt1 = 50.05
        minwidth = max(0.5*width, 6.0)
        rsq_alpa = 1.0/thickness_alpa/cond_alpa
        rsq_mtt2 = 1.0/thickness_mtt2/cond_mtt2
        rsq_mt1 = 1.0/thickness_mt1/cond_mt1
        rsq_alpa_mtt2 = rsq_alpa*rsq_mtt2/(rsq_alpa+rsq_mtt2)

        # nturn = 2
        minwidth = max(0.5*width, 6.0)
        rayon1 = 0.5*outerdiameter - 0.5*width 
        rayon2 = rayon1 - width - spacing
        rayon3 = rayon2 - width - spacing
        y1 = 0.5*outerdiameter - 0.5*minwidth
        y2 = y1 - minwidth - spacing
        y3 = y2 - minwidth - spacing
        y4 = y3 - minwidth - spacing
        y5 = y4 - minwidth - spacing

        # BOTTOM1
        segment1 = 2*rayon1
        segment2 = rayon1+y1
        segment3 = 2*rayon1
        segment4 = rayon1+y2
        # TOP1
        segment5 = 2*rayon1
        segment6 = rayon1+y2
        segment7 = 2*rayon1
        segment8 = rayon1+y3
        # BOTTOM2
        segment9 = rayon1+rayon2
        segment10 = rayon2+y3
        segment11 = 2*rayon2
        segment12 = rayon2+y4
        # TOP2
        segment13 = 2*rayon2
        segment14 = rayon2+y4
        segment15 = 2*rayon2
        segment16 = rayon2+y5

        segment17 = rayon2+rayon3+0.5*width
        segment18 = rayon1-(rayon3+0.5*width)


        length1 = segment1 + segment2 + segment3 + segment4 + 0.5*segment5
        length2 = 0.5*segment5 + segment6 + segment7 + segment8 + 0.5*segment9
        length3 = 0.5*segment9 + segment10 + segment11 + segment12 + 0.5*segment13
        length4 = 0.5*segment13 + segment14 + segment15 + segment16 + segment17 + segment18
        total_length = length1 + length2 + length3 + length4


        area1 = segment1*minwidth + segment2*width + segment3*width + segment4*width + 0.5*segment5*minwidth
        area2 = 0.5*segment5*minwidth + segment6*width + segment7*width + segment8*width + 0.5*segment9*minwidth
        area3 = 0.5*segment9*minwidth + segment10*width + segment11*width + segment12*width + 0.5*segment13*minwidth
        area4 = 0.5*segment13*minwidth + segment14*width + segment15*width + segment16*width + segment17*minwidth + segment18*minwidth


        # for CS1
        area5 = segment2*width + segment3*width + segment4*width
        area6 = segment10*width + segment11*width + segment12*width

        length_ref = 1000.0
        width_ref = 10.0
        area_ref = length_ref * width_ref
        spacing_ref = 2.0

        
        ###########
        # calcul rdc
        rc = 0.1
        rdc1 = rsq_alpa_mtt2 * segment1 / minwidth
        rdc2 = rsq_mtt2 * (segment2+segment3+segment4) / width
        rdc3 = rsq_alpa_mtt2 * segment5 / minwidth
        rdc4 = rsq_alpa * (segment6+segment7+segment8) / width
        rdc5 = rsq_alpa_mtt2 * segment9/minwidth
        rdc6 = rsq_mtt2 * (segment10+segment11+segment12) / width
        rdc7 = rsq_alpa_mtt2 * segment13/minwidth
        rdc8 = rsq_alpa * (segment14+segment15+segment16) / width
        rdc9 = ((rsq_alpa_mtt2*rsq_mt1)/(rsq_alpa_mtt2+rsq_mt1) * segment17 + rsq_mt1 * segment18) / minwidth

        # instances for each resistor 
        rsi1 = 0.5*(rdc1+rdc2+0.5*rdc3+0.25*rc)
        rsi2 = 0.5*(0.5*rdc3+rdc4+0.5*rdc5+0.25*rc)
        rsi3 = 0.5*(0.5*rdc5+rdc6+0.5*rdc7+0.25*rc)
        rsi4 = 0.5*(0.5*rdc7+rdc8+rdc9+0.25*rc)

        # instances for each resistor 
        rsref = 0.5*rsq_mtt2*length_ref/width_ref +  0.5*rsq_alpa*length_ref/width_ref
        raci1 = 0.5*rac * sqrt(rsi1/rsref) * sqrt(length1/length_ref)
        raci2 = 0.5*rac * sqrt(rsi2/rsref) * sqrt(length2/length_ref)
        raci3 = 0.5*rac * sqrt(rsi3/rsref) * sqrt(length3/length_ref)
        raci4 = 0.5*rac * sqrt(rsi4/rsref) * sqrt(length4/length_ref)

        # instances for each inductor
        lsi1 = 0.5*ls*length1/length_ref
        lsi2 = 0.5*ls*length2/length_ref
        lsi3 = 0.5*ls*length3/length_ref
        lsi4 = 0.5*ls*length4/length_ref

        kd = 30.0 # CST FIT
        k1 = k1
        k2 = k2 / (1.0+((width+spacing)/kd)**2)
        k3 = k3 / (1.0+((width+spacing)/kd)**2)


        # instances for each inductor for skin effect
        ldci1 = 0.5*ldc*length1/length_ref
        ldci2 = 0.5*ldc*length2/length_ref
        ldci3 = 0.5*ldc*length3/length_ref
        ldci4 = 0.5*ldc*length4/length_ref

        # instances for each parallel capacitor BOTTOM-to-SUB
        kdistr_cp = 1./3.
        cpi1 = cp * area1/area_ref * (1.0-kdistr_cp)
        cpi2 = cp * area1/area_ref * 0.5*kdistr_cp
        cpi3 = cp * area3/area_ref * (1.0-kdistr_cp)
        cpi4 = cp * area3/area_ref * 0.5*kdistr_cp

        cp2 = cp2 * (segment17*minwidth + segment18*minwidth)/area_ref

        # HELPER FOR THE EXTRACTION
        cpi1 = cpi1 - 0.5*cp2 * (1.0-kdistr_cp)
        cpi2 = cpi2 - 0.5*cp2 * 0.5*kdistr_cp
        cpi3 = cpi3 - 0.5*cp2 * (1.0-kdistr_cp)
        cpi4 = cpi4 - 0.5*cp2 * 0.5*kdistr_cp

        # instances for each coupling capacitor BOTTOM-to-TOP
        kdistr_cs = 1./3.
        csi1 = cs1 * area5/area_ref * (1.0-kdistr_cs)
        csi2 = cs1 * area5/area_ref * 0.5*kdistr_cs
        csi3 = cs1 * area6/area_ref * (1.0-kdistr_cs)
        csi4 = cs1 * area6/area_ref * 0.5*kdistr_cs

        # instances for each coupling capacitor BOTTOM-to-BOTTOM
        csi5 = cs2 * 2*(length1+length3)/length_ref * (1.0-kdistr_cs) * 0.7
        csi6 = cs2 * 2*(length1+length3)/length_ref * 0.5*kdistr_cs * 0.7

        # instances for each coupling capacitor TOP-to-TOP
        csi7 = cs2 * 2*(length2+length4)/length_ref * (1.0-kdistr_cs) * 0.3
        csi8 = cs2 * 2*(length2+length4)/length_ref * 0.5*kdistr_cs * 0.3

        # instances for each coupling capacitor TOP-to-BOTTOM
        csi9 = cs3 * 2*(length1+length3)/length_ref * (1.0-kdistr_cs) * 0.5
        csi10 = cs3 * 2*(length1+length3)/length_ref * 0.5*kdistr_cs * 0.5
        csi11 = cs3 * 2*(length2+length4)/length_ref * (1.0-kdistr_cs) * 0.5
        csi12 = cs3 * 2*(length2+length4)/length_ref * 0.5*kdistr_cs * 0.5

        # instances for the pattern resistor
        rpatti = rpattern / ( 0.5*(area1+area3)/area_ref )
        rpatterni1 = rpattern / ( area1/area_ref * (1.0-kdistr_cp) )
        rpatterni2 = rpattern / ( area1/area_ref * 0.5*kdistr_cp )
        rpatterni3 = rpattern / ( area3/area_ref * (1.0-kdistr_cp) )
        rpatterni4 = rpattern / ( area3/area_ref * 0.5*kdistr_cp )

        # instances for the series gnd resistor
        rgndi = rsub / ( 0.5*(area1+area3)/area_ref)

        rsubp2 = rsubp2 / ( (segment17*minwidth + segment18*minwidth)/area_ref ) # DISSIMETRY SUB RES


        # netlist
        subckt1 = []

        # BOTTOM 1
        subckt1.append( Inductor(name='ls1', nodes=(PORT1, '2'), l=lsi1) )
        subckt1.append( Device(name='xfp1', model='fracpole1', nodes=('2', '3'), rdc=rsi1, ldc=ldci1, rac=raci1) )
        subckt1.append( Device(name='xfp2', model='fracpole1', nodes=('3', '4'), rdc=rsi1, ldc=ldci1, rac=raci1) )
        subckt1.append( Inductor(name='ls2', nodes=('4', '5'), l=lsi1) )
        # TOP 1
        subckt1.append( Inductor(name='ls3', nodes=('5', '6'), l=lsi2) )
        subckt1.append( Device(name='xfp3', model='fracpole1', nodes=('6', '7'), rdc=rsi2, ldc=ldci2, rac=raci2) )
        subckt1.append( Device(name='xfp4', model='fracpole1', nodes=('7', '8'), rdc=rsi2, ldc=ldci2, rac=raci2) )
        subckt1.append( Inductor(name='ls4', nodes=('8', '9'), l=lsi2) )
        # BOTTOM 2
        subckt1.append( Inductor(name='ls5', nodes=('9', '10'), l=lsi3) )
        subckt1.append( Device(name='xfp5', model='fracpole1', nodes=('10', '11'), rdc=rsi3, ldc=ldci3, rac=raci3) )
        subckt1.append( Device(name='xfp6', model='fracpole1', nodes=('11', '12'), rdc=rsi3, ldc=ldci3, rac=raci3) )
        subckt1.append( Inductor(name='ls6', nodes=('12', '13'), l=lsi3) )
        # TOP 2
        subckt1.append( Inductor(name='ls7', nodes=('13', '14'), l=lsi4) )
        subckt1.append( Device(name='xfp7', model='fracpole1', nodes=('14', '15'), rdc=rsi4, ldc=ldci4, rac=raci4) )
        subckt1.append( Device(name='xfp8', model='fracpole1', nodes=('15', '16'), rdc=rsi4, ldc=ldci4, rac=raci4) )
        subckt1.append( Inductor(name='ls8', nodes=('16', PORT2), l=lsi4) )


        subckt1.append( MutualInductor(name='ml13', coupling=k1, ind1='ls1', ind2='ls3') )
        subckt1.append( MutualInductor(name='ml24', coupling=k1, ind1='ls2', ind2='ls4') )
        subckt1.append( MutualInductor(name='ml57', coupling=k1, ind1='ls5', ind2='ls7') )
        subckt1.append( MutualInductor(name='ml68', coupling=k1, ind1='ls6', ind2='ls8') )



        subckt1.append( MutualInductor(name='ml15', coupling=k2, ind1='ls1', ind2='ls5') )
        subckt1.append( MutualInductor(name='ml26', coupling=k2, ind1='ls2', ind2='ls6') )

        subckt1.append( MutualInductor(name='ml17', coupling=k3, ind1='ls1', ind2='ls7') )
        subckt1.append( MutualInductor(name='ml28', coupling=k3, ind1='ls2', ind2='ls8') )

        subckt1.append( MutualInductor(name='ml35', coupling=k3, ind1='ls3', ind2='ls5') )
        subckt1.append( MutualInductor(name='ml46', coupling=k3, ind1='ls4', ind2='ls6') )

        subckt1.append( MutualInductor(name='ml37', coupling=k2, ind1='ls3', ind2='ls7') )
        subckt1.append( MutualInductor(name='ml48', coupling=k2, ind1='ls4', ind2='ls8') )

        # BOTTOM1 to TOP1
        subckt1.append( Capacitor(name='cs1', nodes=(PORT1, '5'), c=csi2) )
        subckt1.append( Capacitor(name='cs2', nodes=('3', '7'), c=csi1) )
        subckt1.append( Capacitor(name='cs3', nodes=('5', '9'), c=csi2) )
        # BOTTOM2 to TOP2
        subckt1.append( Capacitor(name='cs4', nodes=('9', '13'), c=csi4) )
        subckt1.append( Capacitor(name='cs5', nodes=('11', '15'), c=csi3) )
        subckt1.append( Capacitor(name='cs6', nodes=('13', PORT2), c=csi4) )

        # BOTTOM1 to BOTTOM2
        subckt1.append( Capacitor(name='cs7', nodes=(PORT1, '9'), c=csi6) )
        subckt1.append( Capacitor(name='cs8', nodes=('3', '11'), c=csi5) )
        subckt1.append( Capacitor(name='cs9', nodes=('5', '13'), c=csi6) )
        # TOP1 to TOP2
        subckt1.append( Capacitor(name='cs10', nodes=('5', '13'), c=csi8) )
        subckt1.append( Capacitor(name='cs11', nodes=('7', '15'), c=csi7) )
        subckt1.append( Capacitor(name='cs12', nodes=('9', PORT2), c=csi8) )

        # BOTTOM1 to TOP2
        subckt1.append( Capacitor(name='cs13', nodes=(PORT1, '13'), c=csi10) )
        subckt1.append( Capacitor(name='cs14', nodes=('3', '15'), c=csi9) )
        subckt1.append( Capacitor(name='cs15', nodes=('5', PORT2), c=csi10) )
        # TOP1 to BOTTOM2
        subckt1.append( Capacitor(name='cs16', nodes=('5', '9'), c=csi12) )
        subckt1.append( Capacitor(name='cs17', nodes=('7', '11'), c=csi11) )
        subckt1.append( Capacitor(name='cs18', nodes=('9', '13'), c=csi12) )

        # Parallel CAP
        subckt1.append( Capacitor(name='cp1', nodes=(PORT1, '18'), c=cpi2) )
        subckt1.append( Capacitor(name='cp2', nodes=('3', '19'), c=cpi1) )
        subckt1.append( Capacitor(name='cp3', nodes=('5', '20'), c=cpi2) )

        subckt1.append( Capacitor(name='cp4', nodes=('9', '21'), c=cpi4) )
        subckt1.append( Capacitor(name='cp5', nodes=('11', '22'), c=cpi3) )
        subckt1.append( Capacitor(name='cp6', nodes=('13', '23'), c=cpi4) )

        # Pattern Resistance
        subckt1.append( Resistor(name='rpatt1', nodes=('18', '26'), r=rpatterni2) )
        subckt1.append( Resistor(name='rpatt2', nodes=('19', '26'), r=rpatterni1) )
        subckt1.append( Resistor(name='rpatt3', nodes=('20', '26'), r=rpatterni2) )
        subckt1.append( Resistor(name='rpatt4', nodes=('21', '26'), r=rpatterni4) )
        subckt1.append( Resistor(name='rpatt5', nodes=('22', '26'), r=rpatterni3) )
        subckt1.append( Resistor(name='rpatt6', nodes=('23', '26'), r=rpatterni4) )

        # non ideal gnd
        subckt1.append( Resistor(name='rgnd1', nodes=('26', '27'), r=rgndi) )
        subckt1.append( Inductor(name='lgnd1', nodes=('27', SUB), l=0.05e-9) )

        # Fit Dissimetry of Port
        subckt1.append( Capacitor(name='cp7', nodes=(PORT2, '25'), c=cp2) )
        subckt1.append( Resistor(name='rsub10', nodes=('25', '26'), r=rsubp2) )

        self.append( Fracpole(name='fracpole1', order=4, symmetry=False, fac=4e9) )

        self.append( Subckt(name=name, nodes=(PORT1, PORT2, SUB), childs=subckt1) )

