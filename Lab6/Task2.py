import matplotlib.pyplot as plt
import numpy as np
import random

def in_triangle(point):
    """Checks if a point is inside a triangle"""
    if point[0] < 1/2 and point[1] <= np.sqrt(3)*point[0]:
        return True
    elif point[0] >= 1/2 and point[1] <= np.sqrt(3) + np.sqrt(3)*point[0]: 
        return True
    else:
        return False

def gen_triangle_point():
    """Generates a random point in a triangle"""
    x_start = random.uniform(0,1)
    y_start = random.uniform(0,1)

    # Repeats until it gets a point in the triangle
    while not in_triangle([x_start,y_start]):
        x_start = random.uniform(0,1)
        y_start = random.uniform(0,1)

    return np.array([x_start, y_start])

if __name__ == "__main__":
    # Parameters
    num_points = 100000
    p1 = 1/3
    p2 = 1/3
    p3 = 1/3

    # Start points (triangle corners)
    c1 = np.array([0, 0])
    c2 = np.array([1, 0])
    c3 = np.array([1/2, np.sqrt(3)/2])

    # Sets up array to store data
    points = np.zeros((2, num_points))
    points[:, 0] = c1
    points[:, 1] = c2
    points[:, 2] = c3

    point = gen_triangle_point() # Generates random points
    # Makes sure the system stabalizes
    for _ in range(100):
        p = random.random()
        if p <= p1:
            point[:] = [(point[0] + c1[0])/2, (point[1] + c1[1])/2]
        elif p <= (p1 + p2):
            point[:] = [(point[0] + c2[0])/2, (point[1] + c2[1])/2]
        else:
            point[:] = [(point[0] + c3[0])/2, (point[1] + c3[1])/2]

    # Generates all points
    for i in range(3, num_points):
        p = random.random()
        if p <= p1:
            point[:] = [(point[0] + c1[0])/2, (point[1] + c1[1])/2]
        elif p <= (p1 + p2):
            point[:] = [(point[0] + c2[0])/2, (point[1] + c2[1])/2]
        else:
            point[:] = [(point[0] + c3[0])/2, (point[1] + c3[1])/2]
        
        points[:, i] = point

    # Plots
    plt.scatter(points[0], points[1], s=0.4)
    plt.show()