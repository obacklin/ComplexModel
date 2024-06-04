import numpy as np
import random
import matplotlib.pyplot as plt
def prisoners_dilemma(choices):
    if choices[0] == 0 and choices[1] == 0:
        return np.array([1, 1])
    elif choices[0] == 1 and choices[1] == 0:
        return np.array([0, 5])
    elif choices[0] == 0 and choices[1] == 1:
        return np.array([5, 0])
    else:
        return np.array([3, 3])
    

def fitness_scaling(fitlist):
    minimum = np.min(fitlist)
    average = np.average(fitlist)

    a = average/(average-minimum)
    b = minimum*(average)/(average-minimum)

    for i, fitness in enumerate(fitlist):
        fitlist[i] = a*fitness - b

def crossbreed(crom1, crom2):
    """Crossbreads two croms by taking a random cutoff point"""
    r = random.randint(1, crom1.size - 1)
    child1 = np.concatenate((crom1[0:r],crom2[r:]))
    child2 = np.concatenate((crom2[0:r],crom1[r:]))
    return [child1, child2]

def mutation(croms):
    """Randomly mutates the croms"""
    mut_rate = 0.001
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
 #       while crom1.all() == crom2.all():
 #           crom1 = choose_crom(croms, probability_list)
 #           crom2 = choose_crom(croms, probability_list)

        newcroms[i:i+2] = crossbreed(crom1, crom2)

def hist_to_num(hist):
    bin_str = ''.join(f'{a}{b}' for a , b, in hist)
    bin_num = int(bin_str,2)
    num = int(bin_num)
    return(num)

def pd_play(rounds, crom1 ,crom2):
    memory_1 = []
    memory_2 = []
    pointcount = np.array([0,0])
    hist= [crom1[0],crom2[0]]
    res = prisoners_dilemma(hist)
    pointcount += res
    memory_1.append(hist)
    hist.reverse()
    memory_2.append(hist)
    
    add = 1
    for i in range(1,5):
        hist=[crom1[hist_to_num(memory_1)+ add],crom2[hist_to_num(memory_2)+ add]]
        pointcount += prisoners_dilemma(hist)
        memory_1.append(hist)
        hist.reverse()
        memory_2.append(hist)
        add += 2**(2*i)

    for i in range(rounds-5): 
        hist=[crom1[hist_to_num(memory_1)+ add],crom2[hist_to_num(memory_2)+add]]
        pointcount += prisoners_dilemma(hist)
        memory_1.pop(0)
        memory_2.pop(0)
        memory_1.append(hist)
        hist.reverse()
        memory_2.append(hist)
    return pointcount


            
            
if __name__ == "__main__":
    generations = 100
    add = 1 + 4 +  16 + 64 + 256
    crom_size = 1024+add
    nr_of_croms = 100
    croms_culled = 10
    avg_fitness = np.empty(generations)
    top_fitness = np.empty(generations)
    std_dev = np.empty(generations)
    median = np.empty(generations)
    newcroms = np.zeros((croms_culled, crom_size))
    
    croms = np.random.randint(2, size=(nr_of_croms, crom_size))
    start_croms = np.copy(croms)
    for g in range(generations):
        print(f"Generation: {g}")
        fitlist= np.zeros([croms.shape[0]])
        for i in range(nr_of_croms):
            for j in range(i, nr_of_croms):
                points = pd_play(20,croms[i],croms[j])
                fitlist[i] += points[0]
                fitlist[j] += points[1]

        fitness_scaling(fitlist)

        top_crom_id = np.argmax(fitlist)
        points = 0
        for i in range(nr_of_croms):
            points += pd_play(20, croms[top_crom_id], start_croms[i])[0]

        avg_fitness[g] = np.average(fitlist)
        top_fitness[g] = points
        std_dev[g] = np.std(fitlist)
        median[g] = np.median(fitlist)
        if g == generations - 1:
            print(fitlist)
        #fitness_scaling(fitlist)
        create_crossbreeds(croms, fitlist, newcroms)
        replace(croms, newcroms, fitlist)
        mutation(croms)


    

    x = np.linspace(0, generations, generations)
    fig, ax1 = plt.subplots()
    fig, ax2 = plt.subplots()
    fig, ax3 = plt.subplots()
    fig, ax4 = plt.subplots()
    ax1.plot(x, avg_fitness)
    ax2.plot(x, top_fitness)
    ax3.plot(x, std_dev)
    ax4.plot(x, median)

    ax1.set_title(f"Average result over {generations} generations")
    ax1.set_xlabel("Generations")
    ax1.set_ylabel("Average result")

    ax2.set_title(f"Highest result over {generations} generations")
    ax2.set_xlabel("Generations")
    ax2.set_ylabel("Highest result")
    
    ax3.set_title(f"Average standard deviation over {generations} generations")
    ax3.set_xlabel("Generations")
    ax3.set_ylabel("Standard Deviation")

    ax4.set_title(f"Average median over {generations} generations")
    ax4.set_xlabel("Generations")
    ax4.set_ylabel("Median")
    plt.show()
                
                

