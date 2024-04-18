import numpy as np
from Task3 import *

def find_period(grid, N, e):


    # Run sim to go past transient time
    snapshot = run_sim(grid, N, 5000, e)
    iterate = iterate_CA(snapshot,N,e)
    #search for the next time we reach an equal state
    counter = 1
    while not( np.array_equal(snapshot, iterate) ):
        counter += 1
        iterate = iterate_CA(iterate, N, e)
    return counter, snapshot

    

if __name__ == "__main__":    
#SetCA rules
    rows = 11
    cols = 11
   
    num_states = 5
    states = [x for x in range(num_states)]
    e = 2 # {1,2,..e} are the excited states
    excited_states = [x for x in range(1, e+1)]
    # Use uniform dist initial on set {0,..., N-1}
    init_state = np.random.randint(low = 0, high = num_states, size = (rows, cols))
    period = find_period(init_state, num_states, e)[0]
    print(period)




    