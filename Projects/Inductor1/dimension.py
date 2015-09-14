

from sympy import Symbol, simplify, expand


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(%s; %s)"%(str(self.x), str(self.y))

###############
###############

outerdiameter = Symbol('outerdiameter')
spacing = Symbol('spacing')
width = Symbol('width')
minwidth = Symbol('max(0.5*width, 6.0)')




rayon1 = 0.5*outerdiameter - 0.5*width 
rayon2 = rayon1 - width - spacing
rayon3 = rayon2 - width - spacing
y1 = 0.5*outerdiameter - 0.5*minwidth
y2 = y1 - minwidth - spacing
y3 = y2 - minwidth - spacing
y4 = y3 - minwidth - spacing
y5 = y4 - minwidth - spacing
thickness_alpa = 1.45
thickness_mtt2 = 3.4
spacing_imd2 = 7.872532-7.123994
sigma_alpa = 30.3
sigma_mtt2 = 59.133

def parallel(a,b):
    return (a*b)/(a+b)

segment1 = 2*rayon1
segment2 = rayon1+y1
segment3 = 2*rayon1
segment4 = rayon1+y2
segment5 = 2*rayon1
segment6 = rayon1+y2
segment7 = 2*rayon1
segment8 = rayon1+y3
segment9 = 2*rayon2
segment10 = rayon2+y3
segment11 = 2*rayon2
segment12 = rayon2+y4
segment13 = 2*rayon2
segment14 = rayon2+y4
segment15 = 2*rayon2
segment16 = rayon2+y5
segment17 = 2*rayon3



length1 = segment1 + segment2 + segment3 + segment4
length2 = segment5 + segment6 + segment7 + segment8
length3 = segment9 + segment10 + segment11 + segment12
length4 = segment13 + segment14 + segment15 + segment16

rsq_alpa = 1./sigma_alpa/thickness_alpa
rsq_mtt2 = 1./sigma_mtt2/thickness_mtt2

resistance1 = parallel(segment1*rsq_alpa/minwidth, segment1*rsq_mtt2/minwidth)
resistance2 = (segment2+segment3+segment4)*rsq_mtt2/width
resistance3 = parallel(segment5*rsq_alpa/minwidth, segment5*rsq_mtt2/minwidth)
resistance4 = (segment6+segment7+segment8)*rsq_alpa/width
resistance5 = parallel(segment9*rsq_alpa/minwidth, segment9*rsq_mtt2/minwidth)
resistance6 = (segment10+segment11+segment12)*rsq_mtt2/width
resistance7 = parallel(segment13*rsq_alpa/minwidth, segment13*rsq_mtt2/minwidth)
resistance8 = (segment14+segment15+segment16)*rsq_alpa/width
resistance9 = parallel(segment17*rsq_alpa/minwidth, segment17*rsq_mtt2/minwidth)


length =  length1+length2+length3+length4+segment16


outerdiameter = 300
spacing = 2.01
width = 20.0
minwidth = max(0.5*width, 6.0)



resistance = resistance1 + resistance2+resistance3+resistance4+resistance5+resistance6+resistance7+resistance8+resistance9

s =  simplify(resistance)
#print s
s  = str(s)
print eval(s)


s =  simplify(length)
print s
s  = str(s)
print eval(s)


