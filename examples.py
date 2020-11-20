import numpy as np

from src.integration import Integrate

f = lambda x: 3 + 3*x + 4*x**2
F = Integrate(f)

a, b = 0, 4

print('\n### Simpson integration')
print(F(a, b, method='simpson'))

print('\n### Midpoint integration')
print(F(a, b, method='midpoint'))

print('\n### Trapezoidal integration')
print(F(a, b, method='trapezoidal'))

print('\n### Gauss Quadrature integration')
print(F(a, b, method='gauss_quad'))


from src.splines import ClampedCubicSpline, NaturalCubicSpline

x = np.linspace(1, 5, 10)
y = f(x)

c_spl = ClampedCubicSpline(x, y)
func_c_spl = c_spl.gen_function()

print('\n### ClampedCubicSpline')
print(func_c_spl(np.linspace(0, 6, 30)))

n_spl = NaturalCubicSpline(x, y)
func_n_spl = n_spl.gen_function()

print('\n### NaturalCubicSpline')
print(func_n_spl(np.linspace(0, 6, 30)))

from src.interpolation import BaseLagrange

base = BaseLagrange(x, y)

print('\n### BaseLagrange')
print(base(np.linspace(0, 6, 30)))



