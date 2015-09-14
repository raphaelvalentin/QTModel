from ngspice import *
from symbolic import Symbol

name = 'myinductor'
self = Netlist()

subckt1 = []
subckt1.append( Parameters( outerdiameter = 200,
                            width = 10.0,
                            spacing = 2.01,
                            thickness_alpa = 1.45, 
                            thickness_mtt2 = 3.4, 
                            thickness_mt1 = 0.9 ) )

PORT1 = 'P1'
PORT2 = 'P2'
SUB = 'SUB'


subckt1.append( Parameters( # process parameters
                            cond_alpa = 30.3, 
                            cond_mtt2 = 59.133, 
                            cond_mt1 = 50.05,
                            rsq_alpa = '1.0/thickness_alpa/cond_alpa',
                            rsq_mtt2 = '1.0/thickness_mtt2/cond_mtt2',
                            rsq_mt1 = '1.0/thickness_mt1/cond_mt1',
                            rsq_alpa_mtt2 = 'rsq_alpa*rsq_mtt2/(rsq_alpa+rsq_mtt2)',
                            # primitive parameters
                            minwidth = 'max(0.5*width, 6.0)',
                            rayon1 = '0.5*outerdiameter - 0.5*width',
                            rayon2 = 'rayon1 - width - spacing',
                            rayon3 = 'rayon2 - width - spacing',
                            #
                            y1 = '0.5*outerdiameter - 0.5*minwidth',
                            y2 = 'y1 - minwidth - spacing',
                            y3 = 'y2 - minwidth - spacing',
                            y4 = 'y3 - minwidth - spacing',
                            y5 = 'y4 - minwidth - spacing',
                            # 
                            segment1 = '2*rayon1',
                            segment2 = 'rayon1+y1',
                            segment3 = '2*rayon1',
                            segment4 = 'rayon1+y2',
                            segment5 = '2*rayon1',
                            segment6 = 'rayon1+y2',
                            segment7 = '2*rayon1',
                            segment8 = 'rayon1+y3',
                            segment9 = '2*rayon2',
                            segment10 = 'rayon2+y3',
                            segment11 = '2*rayon2',
                            segment12 = 'rayon2+y4',
                            segment13 = '2*rayon2',
                            segment14 = 'rayon2+y4',
                            segment15 = '2*rayon2',
                            segment16 = 'rayon2+y5',
                            segment17 = '2*rayon3',
                            segment18 = 'rayon1-rayon3',
                            #                            
                            length1 = 'segment1 + segment2 + segment3 + segment4 + 0.5*segment5',
                            length2 = '0.5*segment5 + segment6 + segment7 + segment8 + 0.5*segment9',
                            length3 = '0.5*segment9 + segment10 + segment11 + segment12 + 0.5*segment13',
                            length4 = '0.5*segment13 + segment14 + segment15 + segment16 + segment17 + segment18',
                            total_length = 'length1 + length2 + length3 + length4',

                            area1 = 'segment1*minwidth + segment2*width + segment3*width + segment4*width + 0.5*segment5*minwidth',
                            area2 = '0.5*segment5*minwidth + segment6*width + segment7*width + segment8*width + 0.5*segment9*minwidth',
                            area3 = '0.5*segment9*minwidth + segment10*width + segment11*width + segment12*width + 0.5*segment13*minwidth',
                            area4 = '0.5*segment13*minwidth + segment14*width + segment15*width + segment16*width + segment17*minwidth + segment18*minwidth',

                            # for CS1
                            area5 = 'segment2*width + segment3*width + segment4*width',
                            area6 = 'segment10*width + segment11*width + segment12*width',

                            length_ref = 1000.0,
                            area_ref = 10000.0,

                            ###########
                            # calcul rdc
                            rc = 0.1,
                            rdc1 = 'rsq_alpa_mtt2 * segment1 / minwidth',
                            rdc2 = 'rsq_mtt2 * (segment2+segment3+segment4) / width',
                            rdc3 = 'rsq_alpa_mtt2 * segment5 / minwidth',
                            rdc4 = 'rsq_alpa * (segment6+segment7+segment8) / width',
                            rdc5 = 'rsq_alpa_mtt2 * segment9/minwidth',
                            rdc6 = 'rsq_mtt2 * (segment10+segment11+segment12) / width',
                            rdc7 = 'rsq_alpa_mtt2 * segment13/minwidth',
                            rdc8 = 'rsq_alpa * (segment14+segment15+segment16) / width',
                            rdc9 = '((rsq_alpa_mtt2*rsq_mt1)/(rsq_alpa_mtt2+rsq_mt1) * segment17 + rsq_mt1 * segment18) / minwidth',

                            # instances for each resistor 
                            rsi1 = '0.5*(rdc1+rdc2+0.5*rdc3+0.25*rc)',
                            rsi2 = '0.5*(0.5*rdc3+rdc4+0.5*rdc5+0.25*rc)',
                            rsi3 = '0.5*(0.5*rdc5+rdc6+0.5*rdc7+0.25*rc)',
                            rsi4 = '0.5*(0.5*rdc7+rdc8+rdc9+0.25*rc)',
                    
                            # instances for each resistor 
                            raci1 = '0.5*rac * sqrt(rsi1/(rsi1+rsi2+rsi3+rsi4)) * sqrt(length1/length_ref)',
                            raci2 = '0.5*rac * sqrt(rsi2/(rsi1+rsi2+rsi3+rsi4)) * sqrt(length2/length_ref)',
                            raci3 = '0.5*rac * sqrt(rsi3/(rsi1+rsi2+rsi3+rsi4)) * sqrt(length3/length_ref)',
                            raci4 = '0.5*rac * sqrt(rsi4/(rsi1+rsi2+rsi3+rsi4)) * sqrt(length4/length_ref)',
                    
                            # instances for each inductor
                            lsi1 = '0.5*ls*length1/length_ref',
                            lsi2 = '0.5*ls*length2/length_ref',
                            lsi3 = '0.5*ls*length3/length_ref',
                            lsi4 = '0.5*ls*length4/length_ref',
                    
                            # instances for each inductor for skin effect
                            ldci1 = '0.5*ldc*length1/length_ref',
                            ldci2 = '0.5*ldc*length2/length_ref',
                            ldci3 = '0.5*ldc*length3/length_ref',
                            ldci4 = '0.5*ldc*length4/length_ref',
                    
                            # instances for each parallel capacitor BOTTOM-to-SUB
                            kdistr_cp = 1./3.,
                            cpi1 = '(cp * area1/area_ref- 0.5*cp2) * (1.0-kdistr_cp)',
                            cpi2 = '(cp * area1/area_ref- 0.5*cp2) * 0.5*kdistr_cp',
                            cpi3 = '(cp * area3/area_ref- 0.5*cp2) * (1.0-kdistr_cp)',
                            cpi4 = '(cp * area3/area_ref- 0.5*cp2) * 0.5*kdistr_cp',
                    
                            # instances for each coupling capacitor BOTTOM-to-TOP
                            kdistr_cs = 1./3.,
                            csi1 = 'cs1 * area5/area_ref * (1.0-kdistr_cs)',
                            csi2 = 'cs1 * area5/area_ref * 0.5*kdistr_cs',
                            csi3 = 'cs1 * area6/area_ref * (1.0-kdistr_cs)',
                            csi4 = 'cs1 * area6/area_ref * 0.5*kdistr_cs',
                    
                            # instances for each coupling capacitor BOTTOM-to-BOTTOM
                            csi5 = 'cs2 * 2*(length1+length3)/length_ref * (1.0-kdistr_cs) * 0.7',
                            csi6 = 'cs2 * 2*(length1+length3)/length_ref * 0.5*kdistr_cs * 0.7',
                    
                            # instances for each coupling capacitor TOP-to-TOP
                            csi7 = 'cs2 * 2*(length2+length4)/length_ref * (1.0-kdistr_cs) * 0.3',
                            csi8 = 'cs2 * 2*(length2+length4)/length_ref * 0.5*kdistr_cs * 0.3',
                    
                            # instances for each coupling capacitor TOP-to-BOTTOM
                            csi9 = 'cs3 * 2*(length1+length3)/length_ref * (1.0-kdistr_cs) * 0.5',
                            csi10 = 'cs3 * 2*(length1+length3)/length_ref * 0.5*kdistr_cs * 0.5',
                            csi11 = 'cs3 * 2*(length2+length4)/length_ref * (1.0-kdistr_cs) * 0.5',
                            csi12 = 'cs3 * 2*(length2+length4)/length_ref * 0.5*kdistr_cs * 0.5',
                    
                            # instances for the pattern resistor
                            rpatti = 'rpattern / ( 0.5*(area1+area3)/area_ref )',
                    
                            # instances for the series gnd resistor
                            rgndi = 'rsub / ( 0.5*(area1+area3)/area_ref)',
                              ) ) 
 
# netlist

subckt1.append( Inductor(name='ls1', nodes=(PORT1, '2'), l='lsi1') )
subckt1.append( Device(name='xfp1', model='fracpole1', nodes=('2', '3'), rdc='rsi1', ldc='ldci1', rac='raci1') )
subckt1.append( Device(name='xfp2', model='fracpole1', nodes=('3', '4'), rdc='rsi1', ldc='ldci1', rac='raci1') )
subckt1.append( Inductor(name='ls2', nodes=('4', '5'), l='lsi1') )

subckt1.append( Inductor(name='ls3', nodes=('5', '6'), l='lsi2') )
subckt1.append( Device(name='xfp3', model='fracpole1', nodes=('6', '7'), rdc='rsi2', ldc='ldci2', rac='raci2') )
subckt1.append( Device(name='xfp4', model='fracpole1', nodes=('7', '8'), rdc='rsi2', ldc='ldci2', rac='raci2') )
subckt1.append( Inductor(name='ls4', nodes=('8', '9'), l='lsi2') )

subckt1.append( Inductor(name='ls5', nodes=('9', '10'), l='lsi3') )
subckt1.append( Device(name='xfp5', model='fracpole1', nodes=('10', '11'), rdc='rsi3', ldc='ldci3', rac='raci3') )
subckt1.append( Device(name='xfp6', model='fracpole1', nodes=('11', '12'), rdc='rsi3', ldc='ldci3', rac='raci3') )
subckt1.append( Inductor(name='ls6', nodes=('12', '13'), l='lsi3') )

subckt1.append( Inductor(name='ls7', nodes=('13', '14'), l='lsi4') )
subckt1.append( Device(name='xfp7', model='fracpole1', nodes=('14', '15'), rdc='rsi4', ldc='ldci4', rac='raci4') )
subckt1.append( Device(name='xfp8', model='fracpole1', nodes=('15', '16'), rdc='rsi4', ldc='ldci4', rac='raci4') )
subckt1.append( Inductor(name='ls8', nodes=('16', PORT2), l='lsi4') )


subckt1.append( MutualInductor(name='ml13', coupling='k1', ind1='ls1', ind2='ls3') )
subckt1.append( MutualInductor(name='ml24', coupling='k1', ind1='ls2', ind2='ls4') )
subckt1.append( MutualInductor(name='ml57', coupling='k1', ind1='ls5', ind2='ls7') )
subckt1.append( MutualInductor(name='ml68', coupling='k1', ind1='ls6', ind2='ls8') )



subckt1.append( MutualInductor(name='ml15', coupling='k2', ind1='ls1', ind2='ls5') )
subckt1.append( MutualInductor(name='ml26', coupling='k2', ind1='ls2', ind2='ls6') )

subckt1.append( MutualInductor(name='ml17', coupling='k3', ind1='ls1', ind2='ls7') )
subckt1.append( MutualInductor(name='ml28', coupling='k3', ind1='ls2', ind2='ls8') )

subckt1.append( MutualInductor(name='ml35', coupling='k3', ind1='ls3', ind2='ls5') )
subckt1.append( MutualInductor(name='ml46', coupling='k3', ind1='ls4', ind2='ls6') )

subckt1.append( MutualInductor(name='ml37', coupling='k2', ind1='ls3', ind2='ls7') )
subckt1.append( MutualInductor(name='ml48', coupling='k2', ind1='ls4', ind2='ls8') )



# BOTTOM1 to TOP1
subckt1.append( Capacitor(name='cs1', nodes=(PORT1, '5'), c='csi2') )
subckt1.append( Capacitor(name='cs2', nodes=('3', '7'), c='csi1') )
subckt1.append( Capacitor(name='cs3', nodes=('5', '9'), c='csi2') )
# BOTTOM2 to TOP2
subckt1.append( Capacitor(name='cs4', nodes=('9', '13'), c='csi4') )
subckt1.append( Capacitor(name='cs5', nodes=('11', '15'), c='csi3') )
subckt1.append( Capacitor(name='cs6', nodes=('13', PORT2), c='csi4') )

# BOTTOM1 to BOTTOM2
subckt1.append( Capacitor(name='cs7', nodes=(PORT1, '9'), c='csi6') )
subckt1.append( Capacitor(name='cs8', nodes=('3', '11'), c='csi5') )
subckt1.append( Capacitor(name='cs9', nodes=('5', '13'), c='csi6') )
# TOP1 to TOP2
subckt1.append( Capacitor(name='cs10', nodes=('5', '13'), c='csi8') )
subckt1.append( Capacitor(name='cs11', nodes=('7', '15'), c='csi7') )
subckt1.append( Capacitor(name='cs12', nodes=('9', PORT2), c='csi8') )

# BOTTOM1 to TOP2
subckt1.append( Capacitor(name='cs13', nodes=(PORT1, '13'), c='csi10') )
subckt1.append( Capacitor(name='cs14', nodes=('3', '15'), c='csi9') )
subckt1.append( Capacitor(name='cs15', nodes=('5', PORT2), c='csi10') )
# TOP1 to BOTTOM2
subckt1.append( Capacitor(name='cs16', nodes=('5', '9'), c='csi12') )
subckt1.append( Capacitor(name='cs17', nodes=('7', '11'), c='csi11') )
subckt1.append( Capacitor(name='cs18', nodes=('9', '13'), c='csi12') )

# Parallel CAP
subckt1.append( Capacitor(name='cp1', nodes=(PORT1, '18'), c='cpi2') )
subckt1.append( Capacitor(name='cp2', nodes=('3', '18'), c='cpi1') )
subckt1.append( Capacitor(name='cp3', nodes=('5', '18'), c='cpi2') )

subckt1.append( Capacitor(name='cp4', nodes=('9', '19'), c='cpi4') )
subckt1.append( Capacitor(name='cp5', nodes=('11', '19'), c='cpi3') )
subckt1.append( Capacitor(name='cp6', nodes=('13', '19'), c='cpi4') )

# Pattern Resistance
subckt1.append( Resistor(name='rpatt1', nodes=('18', '19'), r='rpatti') )

# Dissimetry of Port (FIT)
subckt1.append( Capacitor(name='cp7', nodes=(PORT2, '20'), c='cp2') )
subckt1.append( Resistor(name='rsub10', nodes=('20', '19'), r='rsubp2') )

# non ideal gnd
subckt1.append( Resistor(name='rgnd1', nodes=('18', '21'), r='rgndi') )
subckt1.append( Inductor(name='lgnd1', nodes=('21', SUB), l=0.05e-9) )

subckt1.append( Resistor(name='rgnd2', nodes=('19', '22'), r='rgndi') )
subckt1.append( Inductor(name='lgnd2', nodes=('22', SUB), l=0.05e-9) )

      
self.append( Fracpole(name='fracpole1', order=4, symmetry=False, fac=4e9) )

self.append( Subckt(name=name, nodes=(PORT1, PORT2, SUB), childs=subckt1) )

                            
                           
print self

