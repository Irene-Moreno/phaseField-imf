
from scipy.optimize import fsolve

def equations(vars):
    x1, x2 = vars
    eq1 = 10*x2 - 9.9746 -5.4748*x1**3 + 8.205*x1**2 - 10.3244*x1 + 4.776  # f'(x1) = g'(x2)
    eq2 = (x1 -x2)*(5.4748*x1**3 -8.205*x1**2 +10.3244*x1 -4.776) -((1.3687*x1**4 -2.735*x1**3 +5.1622*x1**2 -4.776*x1 -1.6704)-(5*x2**2 -9.9746*x2 +1.59744))
    return [eq1, eq2]

def f(x):
    return 1.3687*x**4 -2.735*x**3 +5.1622*x**2 -4.776*x -1.6704

def g(x):
    return 5*x**2 -9.9746*x +1.59744


x, infodict, ier, mesg = fsolve(equations, (0.54, 0.92), full_output = True)

print(infodict)

y1 = f(x[0])
y2 = g(x[1])

print((x[0], y1))
print((x[1], y2))
