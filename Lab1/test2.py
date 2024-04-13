import numpy as np
from scipy import optimize

pert = 0.01 # Adjust size of pertubations
f = lambda a, x: a*x*(1-x) + pert*x**4*(1-x) # The pertubed function
df = lambda a, x: x*(1 - x) # f's derivative with respect to a
df_dx = lambda x, a: a - 2*a*x + 4*pert*x**3*(1-x) - pert*x**4 # f's derivative with respect to x
dfa = lambda mu, p_prev_prim, p_prev: (p_prev + mu*p_prev_prim - p_prev**2 - 2*mu*p_prev_prim*p_prev
+ 4*pert*p_prev_prim*p_prev**3 - 5*pert*p_prev_prim*p_prev**4) # Derivative of the composite function

def q2(a, root, pow):
    """Returns the value and derivative at a of the function where the composition is taken pow times"""
    # Gets first values
    fnew = f(a, root)
    fprime = df(a, root)
    
    # Takes the value of the lower composition and uses it to calculate the next composition
    for i in range(1, pow):
        fprime = dfa(a, fprime, fnew)
        fnew = f(a, fnew)

    return fnew, fprime


def newton(a_guess, root, pow, maxIter):
    """Newton's method for the composite function"""
    tolerance = 1e-10
    aNew = a_guess
    for i in range(maxIter):
        aOld = aNew
        fnew, fprime = q2(aNew, root, pow) # Get the values for funcition and it's derivative
        aNew -= (fnew - root) / fprime # Newton iteration
        if abs(aNew - aOld) < tolerance:
            break

    return aNew

# Set Inital iteration values
# These are the solution to the logistic map
# The idea is the the roots for the perturbed map lies very close to these since the pertubation is small
a_i = [2, 1 + np.sqrt(5)]
delta = 3.2 # Starting value for delta
max_iter = 10000 # Max
num_iter = 10 # Number of values to calc for the approx
root = []

for i in range(2, num_iter):
    # Compute next guess for parameter
    a = a_i[i - 1] + (a_i[i - 1] - a_i[i - 2])/delta
    # Compute super stable point for this parameter value
    root += [optimize.newton(df_dx, 0.5, args=(a,), maxiter=2000)]
    # Do newton iter
    a_i += [newton(a, root[-1], 2**i, max_iter)]
    # Update delta according to ratio
    delta = (a_i[i - 1] - a_i[i - 2]) / (a_i[i] - a_i[i - 1])
print("The Fiegenbaum delta is ", delta)

delta = 4.669201609 # Assume we've calculated delta to a high precision
a_i = [2, 1 + np.sqrt(5)]
alpha_iter = 15
bprim  = []
for i in range(2, alpha_iter):
    a = a_i[i - 1] + (a_i[i - 1] - a_i[i - 2])/delta
    root += [optimize.newton(df_dx, 0.5, args=(a,), maxiter=2000)]
    a_i += [newton(a, root[-1], 2**i, max_iter)]
    # Compute the derivativs
    bprim += [ q2(a_i[-1], root[-1], 2**i)[1] ]

alpha = (-1)*(bprim[-2]/bprim[-1] * delta) # -1 because Wikipedia told us to
print("The Feigenbaum alpha is ", alpha)