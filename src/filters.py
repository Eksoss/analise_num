import numpy as np

class KZAFilter:
    def __init__(self, X):
        self.X = X.copy()
        self.shape = self.X.shape
        self.window = self.X.shape[0]
        self.Z = X.copy()
        self.D = None
        self.dD = None
        self.fD = None
    
    def calculate_D(self, q):
        expanded = np.concatenate((np.full((q, ) + self.shape[1:], np.nan), self.Z, np.full((q, ) + self.shape[1:], np.nan)))
        self.D = abs(expanded[2*q:] - expanded[:-2*q])
        self.dD = np.concatenate((self.D[1:] - self.D[:-1], np.full((1, ) + self.shape[1:], np.nan)))
        self.fD = 1 - self.D/np.nanmax(self.D, axis=0)
        
    def moving_average(self, q):
        expanded = np.concatenate((np.full((q, ) + self.shape[1:], np.nan), self.Z, np.full((q,) + self.shape[1:], np.nan)))
        mean = np.zeros(self.shape, dtype=np.float32)
        base = np.zeros(self.shape, dtype=np.float32)
        for i in range(2*q + 1):
            mean = np.nansum([mean, expanded[i: self.window + i, :, :]], axis=0)
            base = np.nansum([base, expanded[i: self.window + i, :, :]*0 + 1], axis=0)
        self.Z[:] = mean / base
    
    def moving_average_extreme(self, q):
        expanded_x = np.concatenate((np.full((q, ) + self.shape[1:], np.nan), self.X, np.full((q,) + self.shape[1:], np.nan)))
        expanded = np.concatenate((np.full((q, ) + self.shape[1:], np.nan), self.Z, np.full((q,) + self.shape[1:], np.nan)))
        for i in range(self.window):
            mask = np.full((2*q + 1, ) + self.shape[1:], False)
            mask[q] = True
            
            # tail
            mask[:q, self.dD[i] > 0] = True
            mask_range = np.zeros(self.fD[i].shape)
            mask_range[self.dD[i] <= 0] = (self.fD[i][self.dD[i] <= 0]*q).astype(int)
            for j in range(q)[::-1]:
                mask[j][np.where(mask_range > 0)] = True
                mask_range -= 1
                
            # head
            mask[q+1:, self.dD[i] < 0] = True
            mask_range = np.zeros(self.fD[i].shape)
            mask_range[self.dD[i] >= 0] = (self.fD[i][self.dD[i] >= 0]*q).astype(int)
            for j in range(q+1, 2*q+1):
                mask[j][np.where(mask_range > 0)] = True
                mask_range -= 1
            
            self.Z[i] = np.nansum(expanded[i: i+2*q + 1] * mask.astype(int), axis=0)/np.nansum(mask.astype(int), axis=0)
​
    def KZ(self, q, k):
        self.Z = self.X.copy()
        for i in range(k):
            self.moving_average(q)
            
    def KZA(self, q, k):
        self.KZ(q, k)
        for i in range(k):
            self.calculate_D(q)
            self.moving_average_extreme(q)
