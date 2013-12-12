from cs import *


class OrderedDictionaryFixedKeyList(odict):
    def __setitem__(self, key, item):
        if key not in self._keys:
            raise KeyError, "The key %s does not exist and OrderedDictionaryFixedKeyList does not allow adding a key with __setitem__." % key
        else:
            UserDict.__setitem__(self, key, item)
        

d = OrderedDictionaryFixedKeyList({'a':None,'b':None,'c':None})

d['a'] = 1
d['b'] = 2
#print d['z']
d['z'] = 1

print d

