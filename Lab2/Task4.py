import time
import numpy as np
from Task3 import *

def find_period(grid, N, e):


    # Run sim to go past transient time
    snapshot = run_sim(grid, N, 10000, e)
    iterate = iterate_CA(snapshot,N,e)
    #search for the next time we reach an equal state
    counter = 1
    while not( np.array_equal(snapshot, iterate) ):
        counter += 1
        iterate = iterate_CA(iterate, N, e)
        if counter > 30000:
            return "Could not find period in 30 000 steps"
    return counter

    

if __name__ == "__main__":    
#SetCA rules
    start_time = time.perf_counter()
    rows = 50
    cols = 50
    num_states = 5
    states = [x for x in range(num_states)]
    e = 1 # {1,2,..e} are the excited states
    excited_states = [x for x in range(1, e+1)]
    # Use uniform dist initial on set {0,..., N-1}
    init_state = np.random.randint(low = 0, high = num_states, size = (rows, cols))
    period = find_period(init_state, num_states, e)

    end_time = time.perf_counter()
    print("Period: " + str(period) + "\nTime taken: " + str(round(end_time - start_time,2)) + " seconds")




    