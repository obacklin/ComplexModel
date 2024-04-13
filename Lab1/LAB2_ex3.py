from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

df_dx = lambda x, mu, a: mu*(1-2*x+4*a*(x**3)*(1-x)-a*(x**4))
f_ = lambda x, mu, a: mu*(x*(1-x)+ a*(x**4)*(1-x))

#FUNCTION DEFINIG THE ITERATIONS

def new_q_n(n, mu, a, root):
    points = np.zeros(n+1) #because we want to keep here n iterations of the function + our initial value
    points[0] = root
    for i in range((n)):
        points[i+1] =  f_(points[i], mu, a)
    return points


interval = (0, 4)  # start, end (maybe it needs to be adjusted later)
accuracy = 0.001
x_0=0.7 #initial value for the iterations
iters=600 #number of iterations for caculatin the Lyapunov exponent
p_param = 1/4
numtoplot = 200
lims = np.zeros(iters)
fig,(biax,biax2) = plt.subplots(2)
fig.set_size_inches(16, 9)
lims[0] = np.random.rand()

mu_values=np.arange(interval[0], interval[1], accuracy)
l=len(mu_values)
lyap=np.zeros(l) #vector that will keep the Lyapunov exponents
j=0
lambda_n=0
for mu in mu_values:
    points=new_q_n(iters,mu,p_param,x_0)
    for i in range (iters):
      lambda_n += np.log(abs(df_dx(points[i],mu,p_param)))
    lyap[j]=(lambda_n)/iters #Lyapunov exponent
 #print(mu,lyap[j])<
    j+=1
    lambda_n=0
    for i in range(iters - 1):
        lims[i + 1] = mu * (lims[i] * (1 - lims[i]) + p_param*(lims[i]**4) *(1-lims[i])) #sine_param*np.sin(np.pi*lims[i]) # logistic map ux(1-x) + pertb (blue)
    biax.plot([mu] * numtoplot, lims[iters - numtoplot :], "b.", markersize=0.02)

biax2.plot(mu_values,lyap)
biax.set(xlabel="u", ylabel="x", title="Bifuraction Diagram")
biax2.set(xlabel="u", ylabel="Lyapunov exponent", title="Lyapunov Exponents")
plt.axhline(0,color="black")
plt.show()
