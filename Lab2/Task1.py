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

def runge_kutta_3D(coordinates, t, h):
    return [runge_kutta(dxdt, coordinates, 0, t, h), runge_kutta(dydt, coordinates, 1, t, h), runge_kutta(dzdt, coordinates, 2, t, h)], t + h


if __name__ == "__main__":
    h = 0.01
    num_steps = 10000

    fig = plt.figure()
    ax = plt.axes(projection = '3d')

    x = np.array([2])
    y = np.array([1])
    z = np.array([1])
    t = 0

    for i in range(num_steps):
        new_coor, t = runge_kutta_3D([x[i], y[i], z[i]], t, h)
        x = np.append(x, [new_coor[0]])
        y = np.append(y, [new_coor[1]])
        z = np.append(z, [new_coor[2]])

    ax.plot3D(x, y, z, 'blue')
    plt.show()