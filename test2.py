import numpy as np
from scipy import optimize
pert = 0.01
f = lambda a, x: a*x*(1-x) + pert*x**4*(1-x)
df = lambda a, x: x*(1 - x)
df_dx = lambda x, a: a - 2*a*x + 4*pert*x**3*(1-x) - pert*x**4
dfa = lambda mu, p_prev_prim, p_prev: (p_prev + mu*p_prev_prim - p_prev**2 - 2*mu*p_prev_prim*p_prev
+ 4*pert*p_prev_prim*p_prev**3 - 5*pert*p_prev_prim*p_prev**4)

# Verkar rimligt

# dfa = lambda a, func, func_prime: a*func_prime - 2*a*func*func_prime


def q2(a, root, pow):
    fnew = f(a, root)
    fprime = df(a, root)

    for i in range(1, pow):
        fprime = dfa(a, fprime, fnew)
        fnew = f(a, fnew)

    return fnew, fprime


def newton(a_guess, root, pow, maxIter):
    tolerance = 1e-10

    aNew = a_guess
    for i in range(maxIter):
        aOld = aNew
        fnew, fprime = q2(aNew, root, pow)
        aNew -= (fnew - root) / fprime
        if abs(aNew - aOld) < tolerance:
            break

    return aNew

def computeAlpha(a, delta, roots):

    fprime_prev = q2(a[-2], roots[-2], len(a)-1)[1]
    fprime_next = q2(a[-1], roots[-1], len(a))[1]
    alpha = (fprime_prev/fprime_next) * delta
    return alpha


a_i = [2, 1 + np.sqrt(5)]
delta = 3.2
max_iter = 10000
num_iter = 10
root = []

bprim = [q2(a_i[0],1/2, 1)[1], q2(a_i[1], 1/2,2)[1]]

for i in range(2, num_iter):
    a = a_i[i - 1] + (a_i[i - 1] - a_i[i - 2])/delta
    root += [optimize.newton(df_dx, 0.5, args=(a,), maxiter=2000)]
    a_i += [newton(a, root[-1], 2**i, max_iter)]
    bprim += [ q2(a_i[-1], root[-1], 2**i)[1] ]
    delta = (a_i[i - 1] - a_i[i - 2]) / (a_i[i] - a_i[i - 1])
    #print((bprim[-2]/bprim[-1])*delta)
print("Bprim:", bprim)
print(a_i)
print(delta)



