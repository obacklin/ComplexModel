from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

sigma = 10
rho = 28
beta = 8/3

dxdt = lambda x, y, z, t: sigma*(y - x)
dydt = lambda x, y, z, t: x*(rho - z) - y
dzdt = lambda x, y, z, t: x*y - beta*z

def runge_kutta(func, coordinates, i, t, h):
    k1 = h * func(coordinates[0], coordinates[1], coordinates[2], t + h)
    k2 = h * func(coordinates[0] + 0.5 * h, coordinates[1] + 0.5 * h, coordinates[2] + 0.5 * h, t + 0.5*k1)
    k3 = h * func(coordinates[0] + 0.5 * h, coordinates[1] + 0.5 * h, coordinates[2] + 0.5 * h, t + 0.5 * k2)
    k4 = h * func(coordinates[0] + h, coordinates[1] + h, coordinates[2] + h, t + k3)

    return coordinates[i] + (1/6)*(k1 + 2*k2 + 2*k3 + k4)

def runge_kutta_3D(x, y, z, t, h):
    coordinates = [x, y, z]
    x_new = runge_kutta(dxdt, coordinates, 0, t, h)
    y_new = runge_kutta(dydt, coordinates, 1, t, h)
    z_new = runge_kutta(dzdt, coordinates, 2, t, h)
    return x_new, y_new, z_new


if __name__ == "__main__":
    h = 0.01
    num_steps = 100000

    fig = plt.figure()
    ax = plt.axes(projection = '3d')

    x = np.empty(num_steps + 1)
    y = np.empty(num_steps + 1)
    z = np.empty(num_steps + 1)
    x[0] = 2
    y[0] = 1
    z[0] = 1
    t = 0

    for i in range(num_steps):
        x[i + 1], y[i + 1], z[i + 1] = runge_kutta_3D(x[i], y[i], z[i], t, h)
        t += h
        

    ax.plot3D(x, y, z, 'blue')
    plt.show()