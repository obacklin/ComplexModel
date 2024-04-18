from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# The constants for the Lorenz system
sigma = 10
rho = 28
beta = 8/3

# The ODEs for the Lorenz system. t is added for consistency
dxdt = lambda x, y, z, t: sigma*(y - x)
dydt = lambda x, y, z, t: x*(rho - z) - y
dzdt = lambda x, y, z, t: x*y - beta*z

def runge_kutta(func, coordinates, i, t, h):
    """Applies Runge-Kutta to one coordinate for a function with 3 coordinates"""
    k1 = h * func(coordinates[0], coordinates[1], coordinates[2], t + h)
    k2 = h * func(coordinates[0] + 0.5 * h, coordinates[1] + 0.5 * h, coordinates[2] + 0.5 * h, t + 0.5*k1)
    k3 = h * func(coordinates[0] + 0.5 * h, coordinates[1] + 0.5 * h, coordinates[2] + 0.5 * h, t + 0.5 * k2)
    k4 = h * func(coordinates[0] + h, coordinates[1] + h, coordinates[2] + h, t + k3)

    return coordinates[i] + (1/6)*(k1 + 2*k2 + 2*k3 + k4)

def runge_kutta_3D(coordinates, t, h):
    """Applies Runge-Kutta to all 3 coordinates"""
    x_new = runge_kutta(dxdt, coordinates, 0, t, h)
    y_new = runge_kutta(dydt, coordinates, 1, t, h)
    z_new = runge_kutta(dzdt, coordinates, 2, t, h)
    return [x_new, y_new, z_new]


if __name__ == "__main__":
    # Increments for Runge-Kutta
    h = 0.01
    # Number of steps to be taken
    num_steps = 10000

    # For ploting
    fig = plt.figure()
    ax = plt.axes(projection = '3d')

    # Creates an array for the values
    coor = np.empty((num_steps + 1, 3))
    # Sets (x_0, y_0, z_0)
    coor[0] = [2, 1, 1]
    t = 0

    for i in range(num_steps):
        # Applies Runge_Kutta for num_steps steps
        coor[i + 1] = runge_kutta_3D(coor[i], t, h)
        t += h
        

    ax.plot3D(coor[:, 0], coor[:, 1], coor[:, 2], 'blue')
    plt.title("Lorenz attractor plotted to t = {} using Runge-Kutta starting at (2, 1, 1)".format(int(t)))
    plt.show()
    plt.savefig("Lorentzattract.eps", format = "eps")
