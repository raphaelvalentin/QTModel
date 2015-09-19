__all__ = ['__globals__', 'setenv']

# ordered dictionnary
from collections import OrderedDict


# GLOBAL
__globals__ = { 'model' : OrderedDict(), 
                'bench' : OrderedDict(),
                'plot'  : OrderedDict(),
                'param' : OrderedDict(),
              }



def setenv(type=None, name=None):
    assert isinstance(type, str), 'type is not a string'
    assert isinstance(name, str), 'name is not a string'
    if type.lower() == 'model':
        __type__ = 'model'
    elif type.lower() == 'plot':
        __type__ = 'plot'
    elif type.lower() == 'bench':
        __type__ = 'bench'
    else:
        raise Exception('type is not a plot or a bench or a model')        
    def call(item):
        def wrap(*args, **kwargs):
            return item(*args, **kwargs)
        __globals__[__type__][name] = wrap
        return wrap
    return call


"""
__globals__ = OrderedDict()

def setenv(type=None, name=None):
    assert isinstance(type, str), 'type is not a string'
    assert isinstance(name, str), 'name is not a string'
    if type.lower() == 'model':
        __type__ = 'model'
    elif type.lower() == 'plot':
        __type__ = 'plot'
    elif type.lower() == 'bench':
        __type__ = 'bench'
    else:
        raise Exception('type is not a plot or a bench or a model')        
    def call(item):
        def wrap(*args, **kwargs):
            return item(*args, **kwargs)
        __globals__[name] = (__type__, wrap)
    return call

"""







