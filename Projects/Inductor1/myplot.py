### PLOTS

@Plot(name='l11_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Inductance 11', unit='H')
    plot(sp1.freq, sp1.l11, color=blue)
    scatter(sp2.freq, sp2.l11, color=red)

@Plot(name='r11_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Resistance 11', unit='Ohms')
    plot(sp1.freq, sp1.r11, color=blue)
    scatter(sp2.freq, sp2.r11, color=red)

@Plot(name='q11_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Q-factor 11', unit='1')
    plot(sp1.freq, sp1.q11, color=blue)
    scatter(sp2.freq, sp2.q11, color=red)

@Plot(name='l22_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Inductance 22', unit='H')
    plot(sp1.freq, sp1.l22, color=blue)
    scatter(sp2.freq, sp2.l22, color=red)

@Plot(name='r22_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Resistance 22', unit='Ohms')
    plot(sp1.freq, sp1.r22, color=blue)
    scatter(sp2.freq, sp2.r22, color=red)

@Plot(name='q22_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Q-factor 22', unit='1')
    plot(sp1.freq, sp1.q22, color=blue)
    scatter(sp2.freq, sp2.q22, color=red)

@Plot(name='ldiff_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Inductance Diff', unit='H')
    plot(sp1.freq, sp1.ldiff, color=blue)
    scatter(sp2.freq, sp2.ldiff, color=red)

@Plot(name='rdiff_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Resistance Diff', unit='Ohms')
    plot(sp1.freq, sp1.rdiff, color=blue)
    scatter(sp2.freq, sp2.rdiff, color=red)

@Plot(name='qdiff_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Q-factor Diff', unit='1')
    plot(sp1.freq, sp1.qdiff, color=blue)
    scatter(sp2.freq, sp2.qdiff, color=red)

@Plot(name='c11_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Input Capacitance', unit='F')
    plot(sp1.freq, sp1.c11, color=blue)
    scatter(sp2.freq, sp2.c11, color=red)

@Plot(name='r11b_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Input Resistance', unit='Ohms')
    plot(sp1.freq, sp1.r11b, color=blue)
    scatter(sp2.freq, sp2.r11b, color=red)

@Plot(name='dBS11_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('dB(S11)', unit='dB')
    plot(sp1.freq, sp1.dbs11, color=blue)
    scatter(sp2.freq, sp2.dbs11, color=red)

#@Plot(name='capco_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('Cap CO', unit='F')
    scatter(sp2.freq, sp2.cap11_co, color=red)
    scatter(sp2.freq, sp2.cap22_co, color=blue)
    scatter(sp2.freq, sp2.cap12_co, color=green)

#@Plot(name='rcapco_freq')
def __init__():
    xlabel('Frequency', unit='Hz')
    ylabel('RCap CO', unit='Ohms')
    scatter(sp2.freq, sp2.rcap11_co, color=red)
    scatter(sp2.freq, sp2.rcap22_co, color=blue)
    scatter(sp2.freq, sp2.rcap12_co, color=green)
