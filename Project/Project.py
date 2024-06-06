import numpy as np
import random
import matplotlib.pyplot as plt
def prisoners_dilemma(choices):
    """Takes choices for prisoners dilemma and gives results"""
    if choices[0] == 0 and choices[1] == 0:
        return np.array([1, 1])
    elif choices[0] == 1 and choices[1] == 0:
        return np.array([0, 5])
    elif choices[0] == 0 and choices[1] == 1:
        return np.array([5, 0])
    else:
        return np.array([3, 3])
    

def fitness_scaling(fitlist):
    """Scales the fitness as per the article"""
    maximum = np.max(fitlist)
    average = np.average(fitlist)

    a = average/(maximum - average)
    b = average*(average - 2*average)/(maximum-average)

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
    """Converts history to a choice"""
    bin_str = ''.join(f'{a}{b}' for a , b, in hist)
    bin_num = int(bin_str,2)
    num = int(bin_num)
    return(num)

def pd_play(rounds, crom1 ,crom2):
    """Plays a number of rounds between two croms"""
    # Too keep track of memory
    memory_1 = []
    memory_2 = []
    pointcount = np.array([0,0]) # Keeps track of points
    hist= [crom1[0],crom2[0]] # Initial decisions
    pointcount += prisoners_dilemma(hist) # Intial points
    memory_1.append(hist) # First move remembered
    hist.reverse()
    memory_2.append(hist)
    
    add = 1
    # Initial 5 rounds
    for i in range(1,5):
        hist=[crom1[hist_to_num(memory_1)+ add],crom2[hist_to_num(memory_2)+ add]]
        pointcount += prisoners_dilemma(hist)
        memory_1.append(hist)
        hist.reverse()
        memory_2.append(hist)
        add += 2**(2*i)

    # Plays out the remaining rounds
    for i in range(rounds-5): 
        hist=[crom1[hist_to_num(memory_1)+ add],crom2[hist_to_num(memory_2)+add]]
        pointcount += prisoners_dilemma(hist)
        memory_1.pop(0)
        memory_2.pop(0)
        memory_1.append(hist)
        hist.reverse()
        memory_2.append(hist)
    return pointcount

def play_against_group(croms, fitlist, nr_opponents, rounds):
    """Croms play against each other"""
    for i in range(croms.shape[0]):
            for j in range(i, nr_opponents):
                points = pd_play(rounds,croms[i],croms[j])
                fitlist[i] += points[0]
                fitlist[j] += points[1]

def play_against_random(croms, fitlist, nr_opponents, rounds):
    """Croms play against random opponents"""
    opponents = np.random.randint(2, size=(nr_opponents, crom_size))
    for i in range(croms.shape[0]):
            for j in range(nr_opponents):
                points = pd_play(rounds,croms[i],opponents[j])
                fitlist[i] += points[0]
            
if __name__ == "__main__":
    # Setup
    generations = 200
    add = 1 + 4 +  16 + 64 + 256
    crom_size = 1024+add # Total size of memory
    nr_of_croms = 100
    croms_culled = 10
    rounds = 100
    # Keeps track of things
    avg_fitness = np.empty(generations)
    std_dev = np.empty(generations)
    median = np.empty(generations)
    newcroms = np.zeros((croms_culled, crom_size))
    
    croms = np.random.randint(2, size=(nr_of_croms, crom_size))
    prob_c_after_d = np.empty(generations)

    against = "group" # Select who you want croms to play against
    if against == "group":
        play = play_against_group
        nr_of_opponents = croms.shape[0]
        for_graph = "against each other"
    else:
        play = play_against_random
        nr_of_opponents = 100
        for_graph = "against random opponents"

    for g in range(generations):
        print(f"Generation: {g}") # To keep track of how far along it's gotten
        fitlist= np.zeros([croms.shape[0]])

        play(croms, fitlist, nr_of_opponents, rounds)

        fitlist /= nr_of_opponents*rounds # Scales to average result
        avg_fitness[g] = np.average(fitlist)
        # Keeps track of probability to cooperate if opponent defects 5 previous times
        count = 0
        count2 = 0
        for crom in croms:
            for i in range(len(crom)):
                if i > add and (i-add) % 2 < 1 and (i -add) % 8 < 4 and (i-add) % 32 < 16 and (i-add) % 128<64 and (i-add) % 512 < 256:
                    count +=1
                    count2 += crom[i]
        prob_c_after_d[g]= count2/count
        std_dev[g] = np.std(fitlist)
        median[g] = np.median(fitlist)
        if g == generations - 1:
            print(fitlist)

        fitness_scaling(fitlist) # Rescales fitness
        create_crossbreeds(croms, fitlist, newcroms) # Crossbreads
        replace(croms, newcroms, fitlist) # Replaces with crossbreads
        mutation(croms) # Mutates


    # Plotting
    x = np.linspace(0, generations, generations)
    fig, ax1 = plt.subplots() # Average result
    fig, ax2 = plt.subplots() # Probability of cooperating when opponent has defected 5 times
    fig, ax3 = plt.subplots() # Standard deviation
    fig, ax4 = plt.subplots() # Median result
    ax1.plot(x, avg_fitness)
    ax2.plot(x, prob_c_after_d)
    ax3.plot(x, std_dev)
    ax4.plot(x, median)

    ax1.set_title(f"Average result over {generations} generations\nplaying against random opponents")
    ax1.set_xlabel("Generations")
    ax1.set_ylabel("Average result")

    ax2.set_title(f"Probability of cooperating while enemy defected last 5 times\nover {generations} generations playing against " + for_graph)
    ax2.set_xlabel("Generations")
    ax2.set_ylabel("Probability")
    
    ax3.set_title(f"Average standard deviation over {generations} generations\nplaying against " + for_graph)
    ax3.set_xlabel("Generations")
    ax3.set_ylabel("Standard Deviation")

    ax4.set_title(f"Average median over {generations} generations\nplaying against " + for_graph)
    ax4.set_xlabel("Generations")
    ax4.set_ylabel("Median")
    plt.show()
                
                

