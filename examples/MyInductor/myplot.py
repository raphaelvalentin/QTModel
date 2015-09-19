# -*- type: plot -*-

@setenv(type='plot', name='plot1')
def plot1():
    xlabel('Frequency', unit='Hz')
    ylabel('Inductance', unit='H')
    plot(sp1.freq, sp1.l11, color=blue)
    scatter(sp2.freq, sp2.l11, color=red)

@setenv(type='plot', name='plot2')
def plot2():
    xlabel('Frequency', unit='Hz')
    ylabel('Resistance', unit='Ohms')
    plot(sp1.freq, sp1.r11, color=blue)
    scatter(sp2.freq, sp2.r11, color=red)

@setenv(type='plot', name='plot3')
def plot3():
    xlabel('Frequency', unit='Hz')
    ylabel('Q-factor', unit=None)
    plot(sp1.freq, sp1.q11, color=blue)
    scatter(sp2.freq, sp2.q11, color=red)
    