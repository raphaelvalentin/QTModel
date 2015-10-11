########

sp2()
def residual(parameters):
    sp1(**parameters)
    return (sp1.l11-sp2.l11)/sp2.l11, 
           (sp1.r11-sp2.r11)/sp2.r11
minimize(residual, method="cma-es")


class goal1(Goal):
    def __init__(self, **parameters):
        self.method( )
        sp2()

    @minimize(method="cma-es")
    def f(self, **parameters):
        sp1(**parameters)
        return (sp1.l11-sp2.l11)/sp2.l11, 
               (sp1.r11-sp2.r11)/sp2.r11
        
    
@Optim(name='strategy1')
def optim():
    sp2()

    @fmin(method="cma-es", variables=('cp', 'cs'))
    def f(**parameters):

        @fmin(method='levmar', variables=('ls', 'rs'), verbose=False)
        def g(**parameters):
            sp1(**parameters)
            _, ldc1 = box(sp1.freq, sp1.l11, lambda freq, l11: freq<5e9)
            _, rdc1 = box(sp1.freq, sp1.r11, lambda freq, r11: freq<5e9)
            _, ldc2 = box(sp2.freq, sp2.l11, lambda freq, l11: freq<5e9)
            _, rdc2 = box(sp2.freq, sp2.r11, lambda freq, r11: freq<5e9)
            return (ldc1-ldc2)/ldc2,
                   (rdc1-rdc2)/rdc2
                    
        sp1(**parameters)
        return (sp1.l11-sp2.l11)/sp2.l11, 
               (sp1.r11-sp2.r11)/sp2.r11
        
