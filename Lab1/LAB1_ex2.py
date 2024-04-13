from scipy import optimize
import numpy as np

p_param = 1/4

# mu_calc = 2.03123535004797
# mu_calc 3.19483850876

# Newton iter to find super stable point
df_dx = lambda x, mu, a: mu*(1-2*x+4*a*(x**3)*(1-x)-a*(x**4))
f_ = lambda x, mu, a: mu*(x*(1-x)+ a*(x**4)*(1-x))
df_dmu = lambda x, a: x*(1-x)+ a*(x**4)*(1-x) #in [0,1], equal to 0 only if x=0 or x=1
root = optimize.newton(df_dx, 0.05, args=(1,p_param,), maxiter = 200) #to obtain the maximum of f
print(root)


#Definition of the iterates and the derivative of f^(2^n)[mu,root]-root
def new_q_2n(n, mu, a, root):
    points = np.zeros(2**n+1) #because we want to keep here 2^n iterations of the function + our root
    points[0] = root
    for i in range((2**n)):
        points[i+1] =  f_(points[i], mu, a) #vector that contains all the interations until the 2^n
    f_prime = df_dmu(root, a) 
    for i in range(1,2**n):
        f_prime *= df_dmu(points[i], a)
        print(f_prime)

    return ((points[-1] - root), f_prime)

#Newton method
def newton_iter(iters, mu_zero, n, a, root, tolerance, epsilon):
    mu_0 = mu_zero #initial value
    for i in range(iters):
        if abs(new_q_2n(n, mu_0, a, root)[1]) < epsilon: #in fact the derivative doesn't depend on the value of mu, so if this breaks it will be in the first iteration
            break
        mu_1= mu_0-((new_q_2n(n, mu_0, a, root)[0])/(new_q_2n(n, mu_0, a, root)[1]))
        if abs(mu_1-mu_0) <=tolerance:
            return mu_1
        
        mu_0=mu_1
    # The computed parameter mu at which the orbit is superstable.
    return mu_0

tolerance = 1e-5
epsilon = 1e-7
number_newton = 10 #number of iterations in the newton method
number_params = 3 #number of values of u_(2^n) that we are going to find 
mu_vector = np.zeros(number_params + 1) #because the first coordinate is going to be our first guess
# Starting guess

mu_vector[0] = 2.03123535004797
mu_vector[1]= 3.19483850876
delta = 3.2

for n in range (2, number_params+1):
   mu_vector[n] = mu_vector[n-1] + (mu_vector[n-1] - mu_vector[n-2])/delta
   mu_vector[n] = newton_iter(number_newton, mu_vector[n], n, p_param, root, tolerance, epsilon)
   delta = (mu_vector[n]-mu_vector[n-1])/(mu_vector[n-1]-mu_vector[n-2])

#Feigenbaum   constants.
print("The Feigembuam constant is ", delta)