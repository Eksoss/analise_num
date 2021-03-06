import numpy as np

class BaseLagrange:
    def __init__(self, x, y):
        self.x = np.array(x)
        self.left, self.right = self.x.min(), self.x.max()
        self.y = np.array(y)
        self.integrity = False
        self.base = []
        self.check_integrity()
        self.create_base()
        
    def check_integrity(self):
        if self.x.shape == self.y.shape:
            self.integrity = True

    def within(self, x):
        return x >= self.left and x <= self.right

    def create_base(self):
        """
        Li = PROD[(x - xj)] per j!=i/ PROD[(xi - xj)] per j!=i
        """
        self.base = lambda x: np.array([np.prod([x - xj for j, xj in enumerate(self.x) if i!=j])/\
                                        np.prod([xi - xj for j, xj in enumerate(self.x) if i!=j])\
                                        for i, xi in enumerate(self.x)])
        
    def __call__(self, x):
        if not self.integrity:
            return np.nan
        if isinstance(x, (list, np.ndarray)):
            return np.array( [np.sum(self.y * self.base(xi)) if self.within(xi) else np.nan for xi in x] )
        return np.sum(self.y * self.base(x))



