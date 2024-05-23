from painter_play import *
import numpy as np
import random

def paint(croms, room, fitlist):
    nr_of_test = 5
    sum_fitness = 0
    for i, crom in enumerate(croms):
        for _ in range(nr_of_test):
            sum_fitness += painter_play(crom,room)[0]
        fitlist[i] = sum_fitness/nr_of_test

def crossbreed(crom1,crom2):
    r = random.randint(1,54)
    newcrom = np.concatenate(crom1[0:r],crom2[r:])
    return newcrom

def replace(croms, newcroms, fitlist):
    nr_rm_cromes = 10
    sortedlist = np.sort(fitlist)
    a = sortedlist[nr_rm_cromes - 1]
    counter = 0

    for i in range(croms.shape[0]):
        if a >= fitlist[i]:
            croms[i] = newcroms[counter] 
            counter += 1
        if counter == nr_rm_cromes:
            break
    
    return croms

def mutation (croms):
    mut_rate = 0.005
    nr_mut = np.floor(mut_rate*croms.size)
    for i in range(nr_mut):
        x = random.randint(0, croms.shape[0] - 1)
        y = random.randint(0, croms.shape[1] - 1)
        newgene = random.randint(0,3)
        croms[x][y] = newgene
    return croms

def choose_crossbreeds(croms, fitlist):
    sortedlist = np.sort(fitlist)
    a = sortedlist[9]
    x = random.randint(0, croms.shape[0])
    y = random.randint(0, croms.shape[0])
    crom1 = 0
    crom2 = 0
    while crom1 == 0 or crom2 == 0:
        if fitlist[x] >= a:
            crom1 = croms[x]
        if fitlist[y] >= a:
            crom2 = croms[y]
    return(crom1,crom2)

if __name__ == "__main__":
    generations = 200

    croms = np.random.randint(4, size=(100,54) )
    room = np.zeros((30,60))
    fitlist = np.zeros(croms.shape[0])
    
    for i in range(generations):
        paint(croms, room, fitlist)
        






