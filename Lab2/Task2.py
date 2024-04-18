import numpy as np
from scipy.stats import linregress
from Task1 import *

# The constants for the Lorenz system
sigma = 10
rho = 28
beta = 8/3

# The ODEs for the Lorenz system. t is added for consistency
dxdt = lambda x, y, z, t: sigma*(y - x)
dydt = lambda x, y, z, t: x*(rho - z) - y
dzdt = lambda x, y, z, t: x*y - beta*z

def find_lyapunov(normal, pertubed, h, num_steps, pert):
    """Finds the Lyapunov exponent of for a direction"""
    step_size = int(1/h)
    lambda_values = np.ones(int(num_steps/step_size))
    t_values = np.arange(1, h*num_steps + 1, 1)

    index = 0
    for i in range(step_size, num_steps + 1, step_size):
        lambda_values[index] = (1/t_values[index])*np.log(np.linalg.norm(normal[i] - pertubed[i])/pert)
        index += 1

    lambda_val = linregress(t_values, lambda_values)[0]
    return lambda_val

if __name__ == "__main__":
    pert = 0.00001 # The pertubation to applied
    h = 0.001 # The step size
    num_steps = 1000000 # The number of steps
    

    # Initializes array and sets start values for the normal and pertubed cases
    normal = np.empty((num_steps + 1, 3))
    normal[0] = [2, 1, 1]
    x_pert = np.empty((num_steps + 1, 3))
    x_pert[0] = [2 + pert, 1, 1]
    y_pert = np.empty((num_steps + 1, 3))
    y_pert[0] = [2, 1 + pert, 1]
    z_pert = np.empty((num_steps + 1, 3))
    z_pert[0] = [2, 1, 1 + pert]
    t = 0

    # Applies Runge-Kutta to the various pertubations
    for i in range(num_steps):
        normal[i + 1] = runge_kutta_3D(normal[i], t, h)
        x_pert[i + 1] = runge_kutta_3D(x_pert[i], t, h)
        y_pert[i + 1] = runge_kutta_3D(y_pert[i], t, h)
        z_pert[i + 1] = runge_kutta_3D(z_pert[i], t, h)
        t += h

    # Calculates the various lyapunov exponents
    lambda_x = find_lyapunov(normal, x_pert, h, num_steps, pert)
    lambda_y = find_lyapunov(normal, y_pert, h, num_steps, pert)
    lambda_z = find_lyapunov(normal, z_pert, h, num_steps, pert)

    # Gets the max
    lambda_max = max([lambda_x, lambda_y, lambda_z])
    print("The largest Lyapunov exponent along this orbit is:", lambda_max)
