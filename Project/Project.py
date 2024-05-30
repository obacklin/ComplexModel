import numpy as np
import random

def prisoners_dillema(choices):
    if choices[0] == 0 and choices[1] == 0:
        return [1, 1]
    elif choices[0] == 1 and choices[1] == 0:
        return [0, 5]
    elif choices[0] == 0 and choices[1] == 1:
        return [5, 0]
    else:
        return [3, 3]
    

def fitness_scaling(fitlist):
    minimum = np.min(fitlist)
    average = np.average(fitlist)

    a = average*average/(average-minimum)
    b = minimum*(average)/(average-minimum)

    for i, fitness in enumerate(fitlist):
        fitlist[i] = a*fitness - b

def crossbreed(crom1, crom2):
    """Crossbreads two croms by taking a random cutoff point"""
    r = random.randint(1, crom1.size - 1)
    child1 = np.concatenate((crom1[0:r],crom2[r:]))
    child2 = np.concatenate((crom2[0:r],crom1[r:]))
    return [child1, child2]

def mutation (croms):
    """Randomly mutates the croms"""
    mut_rate = 0.005
    nr_mut = int(mut_rate*croms.size)
    for i in range(nr_mut):
        x = random.randint(0, croms.shape[0] - 1)
        y = random.randint(0, croms.shape[1] - 1)
        newgene = random.randint(0,1)
        croms[x][y] = newgene

def choose_crom(croms, probability_list):
    """Randomly picks a crom based on the probability list"""
    sample = random.random()
    counter = 0
    for p in probability_list:
        if sample <= p:
            break
        counter += 1

    return croms[counter]

def create_crossbreeds(croms, fitlist, newcroms):
    """Creates various crossbreads"""
    probability_list = fitlist/fitlist.size
    p = 0
    for i in range(probability_list.size - 1):
        probability_list[i] = p
        p += probability_list[i + 1]

    probability_list[-1] = 1

    for i in range(0, newcroms.shape[0], 2):
        crom1 = choose_crom(croms, probability_list)
        crom2 = choose_crom(croms, probability_list)
        while crom1 == crom2:
            crom1 = choose_crom(croms, probability_list)
            crom2 = choose_crom(croms, probability_list)

        newcroms[i:i+2] = crossbreed(crom1, crom2)

if __name__ == "__main__":
    generations = 200
    crom_size = 70
    nr_of_croms = 100
    croms = croms = np.random.randint(2, size=(nr_of_croms, crom_size))
    newcroms = np.empty((nr_of_croms, crom_size))

    for i in range(generations):
