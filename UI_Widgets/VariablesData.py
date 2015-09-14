__all__ = ['__globals__', 'Model', 'Bench', 'Plot', 'Param']

# ordered dictionnary
class Dict(object):
    def __init__(self):
        self._keys = []
        self.values = []
    def __getitem__(self, key):
        try:
            indx = self._keys.index(key)
            return self.values[indx]
        except ValueError:
            raise KeyError(key)
    def __setitem__(self, key, value):
        try:
            indx = self._keys.index(key)
            self._keys[indx] = key
            self.values[indx] = value
        except ValueError:
            self._keys.append(key)
            self.values.append(value)
    def iteritems(self):
        for name, function in zip(self._keys, self.values):
            yield name, function
    def keys(self):
        return self._keys
    def __delitem__(self, key):
         try:
            indx = self._keys.index(key)
            del self._keys[indx]
            del self.values[indx]
         except ValueError:
            raise KeyError(key)
    def __str__(self):
        s = []
        for name, function in zip(self._keys, self.values):
            s.append( "%r:%r, "%(name, function))
        return "".join(s)

# ordered dictionnary
class Dict(object):
    def __init__(self):
        self._keys = []
        self._values = []
    def __len__(self):
        return len(self._keys)
    def __getitem__(self, key):
        try:
            indx = self._keys.index(key)
            return self._values[indx]
        except ValueError:
            raise KeyError(key)
    def __setitem__(self, key, value):
        try:
            indx = self._keys.index(key)
            self._keys[indx] = key
            self._values[indx] = value
        except ValueError:
            self._keys.append(key)
            self._values.append(value)
    def iteritems(self):
        for name, value in zip(self._keys, self._values):
            yield name, value
    def items(self):
        return self._keys, self._values
    def keys(self):
        return self._keys
    def values(self):
        return self._values
    def __delitem__(self, key):
         try:
            indx = self._keys.index(key)
            del self._keys[indx]
            del self._values[indx]
         except ValueError:
            raise KeyError(key)
    def __str__(self):
        s = []
        for name, value in zip(self._keys, self._values):
            s.append( "%r:%r, "%(name, value))
        return "".join(s)
        

# GLOBAL
__globals__ = { 'model' : Dict(), 
                'bench' : Dict(),
                'plot'  : Dict(),
                'param' : Dict(),
              }

class Bench(object):
    def __init__(self, name):
        self.name = name
    def __call__(self, item):
        __globals__['bench'][self.name] = item

class Plot(object):
    def __init__(self, name):
        self.name = name
    def __call__(self, item):
        __globals__['plot'][self.name] = item

def Model(name):
    def call(item):
        def wrap(*args, **kwargs):
            return item(*args, **kwargs)
        __globals__['model'][name] = wrap
        return wrap
    return call

def Bench(name):
    def call(item):
        def wrap(*args, **kwargs):
            return item(*args, **kwargs)
        __globals__['bench'][name] = wrap
        return wrap
    return call

def Plot(name):
    def call(item):
        def wrap(*args, **kwargs):
            return item(*args, **kwargs)
        __globals__['plot'][name] = wrap
    return call

