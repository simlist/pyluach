from collections import OrderedDict

class Cache(OrderedDict):
    
    '''Extends OrderdDict. 
    
    Accepts an extra kwarg maxlength which sets the maximum length of
    the dictionary. If you add more than the maxlength it deletes entries
    oldest first by extending __setitem__.
    '''
    def __init__(self, *args, **kwargs):
        self.maxlen = kwargs.pop('maxlen', None)
        super(Cache, self).__init__(*args, **kwargs)
        
    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if self.maxlen is not None:
            while len(self) >= self.maxlen:
                self.popitem(False)
        return OrderedDict.__setitem__(self, key, value, dict_setitem=dict_setitem)
    
class memoize(object):
    
    """Memoize the result of a function.
    
    This class is used as a decorator to remember the return value of
    a function or method for multiple calls based on the arguments. For class or static
    methods this decorator should come after the classmethod or 
    staticmethod decorator, and it should go without saying that it will not
    work as expected if used on a method that depends on the current
    state of the object. Also all arguments to the function it is used
    on must be hashable.
    """
    
    def __init__(self, maxlen=None):
        self.cache = Cache(maxlen=maxlen)
        
        
    def __call__(self, func):
        def innercall(*args):
            if args in self.cache:
                return self.cache[args]
            result = func(*args)
            self.cache[args] = result
            return result
        return innercall
    
    
##  Debug!!!
#class test(object):
    
    
#    @memoize(maxlength=30)
#    def change(self, var):
#        print 'called change'
#        return var
        
#t = test()

#def testit():
#    for i in xrange(21):
#        print t.change(i)
        
#testit()
#testit()
#testit()
    
    
        
        
        
        
    
        