import numpy as np

class Integrate:
    def __init__(self, func):
        self.func = func
        self.a = None
        self.b = None
        self.n = None
        self.h = None
        self.X = None
        self.XI0 = None
        self.XI1 = None
        self.XI2 = None
        self.XI = None

    def validate(self):
        if self.a >= self.b:
            raise "a >= b"
        
        if not isinstance(self.n, int):
            print("n is not integer, modifying to int")
            self.n = int(self.n)
            self.validate()
        if self.n%2 != 0:
            self.n += 1
            print("n is not even, using n = %d"%self.n)
        if (self.b - self.a)/self.n > 0.5:
            raise "invalid h, h is too big"
        
    def midpoint(self, a, b, n=10000):
        self.a = a
        self.b = b
        self.n = n + 2
        self.validate()
        self.h = (b - a)/self.n

        self.X = np.linspace(self.a, self.b, self.n)

        self.XI1 = np.nansum(self.func(self.X[1::2]))
        
        self.XI = 2*self.h*self.XI1

        return self.XI
    
    def trapezoidal(self, a, b, n=10000):
        self.a = a
        self.b = b
        self.n = n
        self.validate()
        self.h = (b - a)/self.n

        self.X = np.linspace(self.a, self.b, self.n)[1:-1]
        
        self.XI0 = self.func(a) + self.func(b)
        self.XI1 = np.nansum(self.func(self.X))
        
        self.XI = self.h/2*(self.XI0 + 2*self.XI1)

        return self.XI
            
    def simpson(self, a, b, n=10000):
        self.a = a
        self.b = b
        self.n = n
        self.validate()
        self.h = (b - a)/self.n

        self.X = np.linspace(self.a, self.b, self.n)[1:-1]
        
        self.XI0 = self.func(a) + self.func(b)
        self.XI1 = np.nansum(self.func(self.X[::2])) # index 0 -> i = 1
        self.XI2 = np.nansum(self.func(self.X[1::2])) # index 1 -> i = 2
        
        self.XI = self.h*(self.XI0 + 2*self.XI2 + 4*self.XI1)/3

        return self.XI

    def __call__(self, a, b, n=10000, method='simpson'):
        try:
            return getattr(self, method)(a, b, n)
        except:
            raise 'invalid method %s'%method


    
