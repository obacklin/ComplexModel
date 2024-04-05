from sympy import *
from scipy import optimize

p_param = 1/4
df_dx = lambda x, mu, a: mu*(1-2*x+4*a*(x**3)*(1-x)-a*(x**4))
f_ = lambda x, mu, a: mu*(x*(1-x)+ a*(x**4)*(1-x))
df_dmu = lambda x, a: x*(1-x)+ a*(x**4)*(1-x) #in [0,1], equal to 0 only if x=0 or x=1
root = optimize.newton(df_dx, 0.05, args=(1,p_param,), maxiter = 200) #to obtain the maximum of f
print(root)


x, u = symbols('x u')
f = u*(root*(1-root)+(1/4)*(root)**4*(1-root))
g = u*(x*(1-x) + (1/4)*(x**4)*(1-x))

h = g.subs({'x':f})
print(h)






