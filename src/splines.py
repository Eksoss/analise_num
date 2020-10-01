import numpy as np

class ClampedCubicSpline:
    def __init__(self, x, y, **kwargs):
        self.x = np.array(x)
        self.y = np.array(y)
        self.n = self.x.size # [0, n]
        self.n1 = self.n - 1 # [0, n-1]
        self.coefs = np.zeros((self.n, 4), dtype=np.float64)
        self.coefs[:, 0] = self.y
        self.FPO = kwargs.get('FPO', 0)
        self.FPN = kwargs.get('FPN', 0)
        self.h = np.zeros(self.n1)
        self.mu = np.zeros(self.n1)
        self.l = np.zeros(self.n)
        self.z = np.zeros(self.n)
        self.alpha = np.zeros(self.n)

    def run(self):
        self.define_hi()
        self.define_a0_an()
        self.define_a()
        self.define_lmz0()
        self.define_lmz()
        self.define_lzcn()
        self.define_cbd()

    # step 1
    def define_hi(self):
        self.h = self.x[1:] - self.x[:-1]

    # step 2
    def define_a0_an(self):
        self.alpha[0] = 3 * (self.coefs[1, 0] - self.coefs[0, 0])/self.h[0] - 3 * self.FPO
        self.alpha[-1] = 3 * self.FPN - 3*(self.coefs[-1, 0] - self.coefs[-2, 0])/self.h[-1]

    # step 3 
    def define_a(self):
        self.alpha[1:-1] = 3/self.h[1:] * (self.coefs[2:, 0] - self.coefs[1:-1, 0])\
                           - 3/self.h[:-1] * (self.coefs[1:-1, 0] - self.coefs[:-2, 0])

    # step 4
    def define_lmz0(self):
        self.l[0] = 2 * self.h[0]
        self.mu[0] = 0.5
        self.z[0] = self.alpha[0]/self.l[0]

    # step 5
    def define_lmz(self):
        for i in range(1, self.n1):
            self.l[i] = 2 * (self.x[i + 1] - self.x[i - 1]) - self.h[i - 1] * self.mu[i - 1]
            self.mu[i] = self.h[i]/self.l[i]
            self.z[i] = (self.alpha[i] - self.h[i - 1]*self.z[i - 1])/self.l[i]

    # step 6
    def define_lzcn(self):
        self.l[-1] = self.h[-1] * (2 - self.mu[-1])
        self.z[-1] = (self.alpha[-1] - self.h[-1]*self.z[-2])/self.l[-1]
        self.coefs[-1, 2] = self.z[-1]

    # step 7
    def define_cbd(self):
        for i in np.arange(self.n1)[::-1]:
            self.coefs[i, 2] = self.z[i] - self.mu[i] * self.coefs[i + 1, 2]
            self.coefs[i, 1] = (self.coefs[i + 1, 0] - self.coefs[i, 0])/self.h[i]\
                               - self.h[i] * (self.coefs[i + 1, 2] + 2 * self.coefs[i, 2])/3
            self.coefs[i, 3] = (self.coefs[i + 1, 2] - self.coefs[i, 2])/(3 * self.h[i])

    # step 8
    def output(self):
        return self.coefs[:-1, :]

    def gen_function(self):
        coefs = self.output()
        intervals = lambda x: (self.n1 - np.argmax((self.x - x)[::-1] <= 0)).clip(0, self.n1 - 1) if x >= self.x.min() and x <= self.x.max() else None
        S = []
        for coef, x0 in zip(coefs, self.x[:-1]):
            S.append([coef, x0])
        def _(x):
            idx = intervals(x)
            if idx is None:
                return np.nan
            # print(idx)
            _vars = S[idx]
            powers = np.power(np.full(4, x) - np.full(4, _vars[1]), [0, 1, 2, 3])
            res = _vars[0].dot(powers)
            return res
        _ = np.vectorize(_)
        return _

class NaturalCubicSpline:
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
        self.n = self.x.size  # [0, n]
        self.n1 = self.n - 1  # [0, n-1]
        self.coefs = np.zeros((self.n, 4), dtype=np.float64)
        self.h = None
        self.alpha = np.zeros(self.n1)
        
        self.coefs[:, 0] = self.y
        self.u = np.zeros(self.n)
        self.l = np.zeros(self.n)
        self.z = np.zeros(self.n)
        
    def run(self):
        self.define_h()
        self.define_alpha()
        self.define_luz0()
        self.define_luzi()
        self.define_luzn()
        self.define_cbd()
        
    def define_h(self):
        self.h = self.x[1:] - self.x[:-1]

    def define_alpha(self):
        self.alpha = 3/self.h[1:] * (self.coefs[2:, 0] - self.coefs[1:-1, 0]) - 3/self.h[:-1] * (self.coefs[1:-1, 0] - self.coefs[:-2, 0])

    def define_luz0(self):
        self.l[0] = 1
        self.u[0] = 0
        self.z[0] = 0

    def define_luzi(self):
        for i in range(1, self.n1):
            self.l[i] = 2*(self.x[i + 1] - self.x[i - 1]) - self.h[i - 1]*self.u[i - 1]
            self.u[i] = self.h[i]/self.l[i]
            self.z[i] = (self.alpha[i - 1] - self.h[i - 1]*self.z[i - 1])/self.l[i]

    def define_luzn(self):
        self.l[-1] = 1
        self.z[-1] = 0
        self.coefs[-1, 2] = 0

    def define_cbd(self):
        for i in np.arange(self.n1)[::-1]:
            self.coefs[i, 2] = self.z[i] - self.u[i]*self.coefs[i + 1, 2]
            self.coefs[i, 1] = (self.coefs[i + 1, 0] - self.coefs[i , 0])/self.h[i] - self.h[i]*(self.coefs[i + 1, 2] + 2*self.coefs[i, 2])/3
            self.coefs[i, 3] = (self.coefs[i + 1, 2] - self.coefs[i, 2])/(3 * self.h[i])
    
    def output(self):
        return self.coefs[:-1, :]

    def gen_function(self):
        coefs = self.output()
        intervals = lambda x: (self.n1 - np.argmax((self.x - x)[::-1] <= 0)).clip(0, self.n1 - 1) if x >= self.x.min() and x <= self.x.max() else None
        S = []
        for coef, x0 in zip(coefs, self.x[:-1]):
            S.append([coef, x0])
        def _(x):
            idx = intervals(x)
            if idx is None:
                return np.nan
            _vars = S[idx]
            powers = np.power(np.full(4, x) - np.full(4, _vars[1]), [0, 1, 2, 3])
            res = _vars[0].dot(powers)
            return res
        _ = np.vectorize(_)
        return _

