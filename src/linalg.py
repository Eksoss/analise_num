import numpy as np

class TridiagonalLinear:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.n = self.b.size
        self.l = np.eye(self.n, dtype=np.float64)
        self.u = np.eye(self.n, dtype=np.float64)
        self.z = np.zeros(b.shape, dtype=np.float64)
        self.x = np.zeros(b.shape, dtype=np.float64)

    def run(self):
        self.define_luz()
        self.define_lluz()
        self.define_llz()
        self.define_x()

    def define_luz(self):
        self.l[0, 0] = self.A[0, 0]
        self.u[0, 1] = self.A[0, 1]/self.l[0, 0]
        self.z[0] = self.b[0]/self.l[0, 0]

    def define_lluz(self):
        for i in range(1, self.n - 1):
            self.l[i, i - 1] = self.A[i, i - 1]
            self.l[i, i] = self.A[i, i] - self.l[i, i - 1]*self.u[i - 1, i]
            self.u[i, i + 1] = self.A[i, i + 1]/self.l[i, i]
            self.z[i] = (self.b[i] - self.l[i, i - 1]*self.z[i - 1])/self.l[i, i]

    def define_llz(self):
        self.l[-1, -2] = self.A[-1, -2]
        self.l[-1, -1] = self.A[-1, -1] - self.l[-1, -2]*self.u[-2, -1]
        self.z[-1] = (self.b[-1] - self.l[-1, -2]*self.z[-2])/self.l[-1, -1]

    def define_x(self):
        self.x[-1] = self.z[-1]
        for i in np.arange(self.n - 1)[::-1]:
            self.x[i] = self.z[i] - self.u[i, i + 1]*self.x[i + 1]

    def output(self):
        return self.x
  
    def easy_way(self):
        return np.linalg.solve(self.A, self.b)
