import numpy as np
from Task1 import *

sigma = 10
rho = 28
beta = 8/3

dxdt = lambda x, y, z, t: sigma*(y - x)
dydt = lambda x, y, z, t: x*(rho - z) - y
dzdt = lambda x, y, z, t: x*y - beta*z

if __name__ == "__main__":
    pert = 0.0001
    h = 0.001
    num_steps = 1000000


    x = np.empty(num_steps + 1)
    y = np.empty(num_steps + 1)
    z = np.empty(num_steps + 1)
    x[0] = 2
    y[0] = 1
    z[0] = 1
    x_pert = np.empty(num_steps + 1)
    y_pert = np.empty(num_steps + 1)
    z_pert = np.empty(num_steps + 1)
    x_pert[0] = 2 + pert
    y_pert[0] = 1 + pert
    z_pert[0] = 1 + pert
    t = 0

    for i in range(num_steps):
        x[i + 1], y[i + 1], z[i + 1] = runge_kutta_3D(x[i], y[i], z[i], t, h)

        x_pert[i + 1], y_pert[i + 1], z_pert[i + 1] = runge_kutta_3D(x_pert[i], y_pert[i], z_pert[i], t, h)

        t += h

    unpertubed_start_coord = np.array([x[0], y[0], z[0]])
    unpertubed_end_coord = np.array([x[-1], y[-1], z[-1]])
    pertubed_start_coord = np.array([x_pert[0], y_pert[0], z_pert[0]])
    pertubed_end_coord = np.array([x_pert[-1], y_pert[-1], z_pert[-1]])

    Z0 = np.linalg.norm(unpertubed_start_coord - pertubed_start_coord)
    Zt = np.linalg.norm(unpertubed_end_coord - pertubed_end_coord)

    Lyapunov = (1/t)*np.log(Zt/Z0)

    print(Lyapunov)