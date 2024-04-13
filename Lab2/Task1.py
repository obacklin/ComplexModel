dxdt = lambda x: 


def runge_kutta(func, coordinates, t, h):
    k1 = h * func(coordinates[0], y)
    k2 = h * func(x + 0.5 * h, y + 0.5 * k1)
    k3 = h * func(x + 0.5 * h, y + 0.5 * k2)
    k4 = h * func(x + h, y + k3)

    y += (1/6)*(k1 + 2*k2 + 2*k3 + k4)
    x += h

    return x, y

