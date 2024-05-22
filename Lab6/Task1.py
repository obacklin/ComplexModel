from painter_play import *
import numpy as np
import random

croms = np.random.randint(4, size=(100,54) )
print(croms)
room = np.zeros((30,60))
def paint(croms):
    cromsfit = []
    for crom in croms:
        cromsfit.append(painter_play(crom,room)[0])

def crossbreed(crom1,crom2):
    r = random.randint(1,54)
    newcrom = np.concatenate(crom1[0:r],crom2[r:])
    return newcrom

def replace(croms, newcroms, fitlist):
    
    sortedlist = np.sort(fitlist)
    a = sortedlist[9]
    counter = 0

    for i in range(croms.shape[0]):
        if a >= fitlist[i]:
            croms[i] = newcroms[counter] 
            counter += 1
        if counter == 10:
            break
    
    return croms

def mutation (croms):
    mut_rate = 0.005
    nr_mut = np.floor(mut_rate*croms.size)
    for i in range(nr_mut):
        x = random.randint(0,99)
        y = random.randint(0,53)
        newgene = random.randint(0,3)
        croms[x][y] = newgene
    return croms

def choose_crossbreeds(croms, fitlist):
    sortedlist = np.sort(fitlist)
    a = sortedlist[9]
    x = random.randint(0,99)
    y = random.randint(0,99)
    crom1 = 0
    crom2 = 0
    while crom1 == 0 or crom2 == 0:
        if fitlist[x] >= a:
            crom1 = croms[x]
        if fitlist[y] >= a:
            crom2 = croms[y]
    return(crom1,crom2)





