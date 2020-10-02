import numpy as np

class Simpson:
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
        if self.a >= self.b;
            raise "a >= b"
        
        if not isinstance(self, int):
            print("n is not integer, modifying to int")
            self.n = int(self.n)
            self.validate()
        elif self.n <= 3:
            raise "invalid n, n is too small"
        elif self.n%2 != 0:
            self.n -= 1
            print("n is not even, using n = %d"%self.n)
            
    def __call__(self, a, b, n=10000):
        self.a = a
        self.b = b
        self.n = n
        self.h = (b - a)/self.n
        self.validate()

        self.X = np.linspace(self.a, self.b, self.n)[1:-1]
        
        self.XI0 = self.func(a) + self.func(b)
        self.XI1 = np.nansum(self.func(self.X[::2])) # index 0 -> i = 1
        self.XI2 = np.nansum(self.func(self.X[1::2])) # index 1 -> i = 2
        
        self.XI = self.h*(self.XI0 + 2*self.XI2 + 4*self.XI1)/3

        return self.XI
