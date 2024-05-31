from painter_play import *
import numpy as np
import random
import matplotlib.pyplot as plt
import tkinter as tk

def paint(croms, room, fitlist):
    """Paints all croms desired nr of times and takes average fitness"""
    nr_of_test = 5
    for i, crom in enumerate(croms):
        sum_fitness = 0
        for _ in range(nr_of_test):
            sum_fitness += painter_play(crom,room)[0]
        fitlist[i] = sum_fitness/nr_of_test

def crossbreed(crom1, crom2):
    """Crossbreads two croms by taking a random cutoff point"""
    r = random.randint(1, crom1.size - 1)
    newcrom = np.concatenate((crom1[0:r],crom2[r:]))
    return newcrom

def replace(croms, newcroms, fitlist):
    """Replaces all croms that are undesired with the new crossbreads"""
    sortedlist = np.sort(fitlist)
    a = sortedlist[newcroms.shape[0] - 1]
    counter = 0

    for i in range(croms.shape[0]):
        if a >= fitlist[i]:
            croms[i] = newcroms[counter] 
            counter += 1
        if counter == newcroms.shape[0]:
            break

def mutation (croms):
    """Randomly mutates the croms"""
    mut_rate = 0.005
    nr_mut = int(mut_rate*croms.size)
    for i in range(nr_mut):
        x = random.randint(0, croms.shape[0] - 1)
        y = random.randint(0, croms.shape[1] - 1)
        newgene = random.randint(0,3)
        croms[x][y] = newgene

def create_crossbreeds(croms, fitlist, newcroms):
    """Creates various crossbreads"""
    sortedlist = np.sort(fitlist)
    a = sortedlist[newcroms.shape[0] - 1]
    for i in range(newcroms.shape[0]):
        found_crom1 = False
        found_crom2 = False
        while (not found_crom1) or (not found_crom2):
            x = random.randint(0, croms.shape[0] - 1)
            y = random.randint(0, croms.shape[0] - 1)
            if fitlist[x] >= a:
                crom1 = croms[x]
                found_crom1 = True
            if fitlist[y] >= a:
                crom2 = croms[y]
                found_crom2 = True
        newcroms[i] = crossbreed(crom1, crom2)

if __name__ == "__main__":
    # Select parameters
    generations = 5
    nr_of_croms = 100
    crom_size = 54
    croms_culled = 10

    # Creates the various matrixes and arrays needed
    croms = np.random.randint(4, size=(nr_of_croms, crom_size))
    newcroms = np.zeros((croms_culled, crom_size))
    room = np.zeros((60,30))
    fitlist = np.zeros(croms.shape[0])
    avg_fitness = np.empty(generations + 1)
    
    # Goes through a nr of generations
    for i in range(generations):
        print("Gen: " + str(i)) # To keep track of how far the simulation has gotten as it can take a while
        paint(croms, room, fitlist)
        avg_fitness[i] = np.average(fitlist) # Keeps track of how the average fitness changes
        create_crossbreeds(croms, fitlist, newcroms)
        replace(croms, newcroms, fitlist)
        mutation(croms)

    print("Final generation: {}".format(generations))
    paint(croms, room, fitlist) # A final paint to check the fitness of the end result
    avg_fitness[generations] = np.average(fitlist)

    # Plot fitness
    x = np.linspace(0, generations, generations + 1)
    plt.plot(x, avg_fitness)
    plt.title("Average fitness over {} generations".format(generations))
    plt.xlabel("Generations")
    plt.ylabel("Average fitness")
    plt.show()
    
    # Find best crom and paint using it
    top_crom = croms[np.argmax(fitlist)]
    fitness, xpos, ypos = painter_play(top_crom, room)
    
    # Initializes tk for drawing
    top = tk.Tk()
    # Setup of sizes
    square_size = 20
    can_heigth = 600
    can_width = 1200
    # Setup canvas. Background is black to get black lines between squares
    Canvas = tk.Canvas(top, bg="black", height=can_heigth, width=can_width)

    # Gets which squares are painted and path
    painted_squares = np.array([xpos, ypos])
    painted_squares = np.transpose(painted_squares)
    painted_squares += np.full((painted_squares.shape[0], painted_squares.shape[1]), -1) # Adjusts since painter_play matrix starts at (1, 1), not (0, 0)
    
    # Creates all unpainted squares
    for xcoor in range(2, can_width, square_size):
        for ycoor in range(2, can_heigth, square_size):
            Canvas.create_rectangle(xcoor, ycoor, xcoor + square_size - 1, ycoor + square_size - 1, fill="white")

    # Paints all painted squares. Must be done separately from the path or it will overwrite them
    for square in painted_squares:
        x, y = square[0]*square_size + 2, square[1]*square_size + 2
        Canvas.create_rectangle(x, y, x + square_size - 1, y + square_size - 1, fill="grey") # For clarity we paint a fairly boring grey

    # Start
    x_old, y_old = painted_squares[0][0]*square_size + square_size/2 + 2, painted_squares[0][1]*square_size+ square_size/2 + 2

    # Traces the path
    for square in painted_squares[1:]:
        x, y = square[0]*square_size + square_size/2 + 2, square[1]*square_size + square_size/2 + 2
        Canvas.create_line(x_old, y_old, x, y, fill="orange", width=2, arrow=tk.LAST)
        x_old = x
        y_old = y

    # Creates circles at start and finish
    x, y = painted_squares[0]
    x, y = x*square_size + square_size/2 + 2, y*square_size+ square_size/2 + 2
    r = 5
    Canvas.create_oval(x-r, y-r, x + r, y + r, fill="green")
    Canvas.create_oval(x_old-r, y_old-r, x_old + r, y_old + r, fill="red")

    Canvas.pack()
    top.mainloop()







def in_triangle(point):
    if point[0] < 1/2 and point[1] <= np.sqrt(3)*point[0]:
        return True
    elif point[0] >= 1/2 and point[1] <= np.sqrt(3) - np.sqrt(3)*point[0]: 
        return True
    else:
        return False
x_start = random.uniform(0,1)
y_start = random.uniform(0,1)

while not in_triangle([x_start,y_start]):
    x_start = random.uniform(0,1)
    y_start = random.uniform(0,1)

    