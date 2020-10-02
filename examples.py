import numpy as np

from src.integration import Simpson

f = lambda x: 3 + 3*x + 4*x**2
F = Simpson(f)

a, b = 0, 4
res = F(a, b)

print(res)
