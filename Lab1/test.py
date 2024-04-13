from scipy import optimize
import numpy as np

p_param = 1/4

# Newton iter to find super stable point
df_dx = lambda x, mu, a: mu*(1-2*x+4*a*(x**3)*(1-x)-a*x**4)
f_ = lambda x, mu, a: mu*(x*(1-x)+ a*(x**4)*(1-x))
df_dmu = lambda x, a: x*(1-x)+ a*(x**4)*(1-x) #in [0,1], equal to 0 only if x=0 or x=1
root = optimize.newton(df_dx, 0.05, args=(1,p_param,),maxiter = 200)
print(root)


def newton_iter(iters, mu_zero, n, a, root):
    mu_n = mu_zero
    for i in range(iters):
        mu_n = mu_n - new_q_2n(n, mu_n, a, root)

    # The computed parameter mu at which the orbit is superstable.
    return mu_n

def new_q_2n(n, mu, a, root):
    points = np.zeros(2**n)
    points[0] = root
    
    for i in range((2**n)-1):
        points[i+1] =  f_(points[i], mu, a)

    f_prime = df_dmu(root, a)
    
    #print("fprime", f_prime)
    for i in range(1,2**n):
        f_prime *= df_dmu(points[i], a)
        print(f_prime)
        if(f_prime == 0):
            print(points[i], points[i-1], points[i+1], df_dmu(points[i], a))
            break
            #print("fprime at i = ",i, " fprim = ", f_prime)

    print("Points", points)
    for x in points:
        if(x > 1):
            print("Error!!!! x > 1!")
        elif(x<0):
            print("Also ERROR!!! x < 0!")
        elif(abs(x-1)< 1e-6):
            print("x close to 1", x)
        elif(abs(x)< 1e-6):
            print("x close to zero!", x)
        # elif(abs(x-root) < 1e-6):
        #     print("x close to root!", x)

    return (points[-1] - root) / f_prime

number_of_params = 5
mu_vector = np.zeros(number_of_params)
# Starting guess
mu_vector[0] = 3

new_q_2n(5, 2.8, p_param, root)

# for n in range(1, number_of_params):
#     mu_vector[n] = newton_iter(1, mu_vector[n-1], n, p_param, root)

    








