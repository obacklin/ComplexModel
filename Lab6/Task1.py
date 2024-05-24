from painter_play import *
import numpy as np
import random
import matplotlib.pyplot as plt

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
    generations = 200
    nr_of_croms = 100
    crom_size = 54
    croms_culled = 10

    # Creates the various matrixes and arrays needed
    croms = np.random.randint(4, size=(nr_of_croms, crom_size))
    newcroms = np.zeros((croms_culled, crom_size))
    room = np.zeros((30,60))
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
    # Do something with this










