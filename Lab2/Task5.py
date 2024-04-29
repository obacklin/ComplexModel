import numpy as np
import random
from Task3 import *
from Task4 import *

def modify_grid(grid,N,e,nr_modifies):
    nr_rows , nr_cols =grid.shape
    modified_cells = []
    new_grid = grid.copy()
<<<<<<< HEAD
    for cells in range(5):
=======
    for cells in range(nr_modifies):
>>>>>>> ba921876ae19741fc5274328b4c10ef9ec209e57
        row = random.randint(0,nr_rows-1)
        col = random.randint(0,nr_cols-1)
        while (row,col) in modified_cells:
            row = random.randint(0,nr_rows-1)
            col = random.randint(0,nr_cols-1)
        modified_cells.append((row,col))

        state = random.randint(0,N-1)
        while grid[row,col] == state:
            state = random.randint(0,N-1)
        new_grid[row,col] = state
    return modified_cells, new_grid
           
if __name__ == "__main__":
    
    #SetCA rules¨

    nr_rows = 20
    nr_cols = 20
    nr_states = 5
    states = [x for x in range(nr_states)]
    e = 1 # {1,2,..e} are the excited states
    excited_states = [x for x in range(1, e+1)]
    # Use uniform dist initial on set {0,..., N-1}
    grid = np.random.randint(low = 0, high = nr_states, size = (nr_rows, nr_cols))
    #period, periodic_grid = find_period(grid, nr_states, e)
    periodic_grid = run_sim(grid,nr_states,100,e)
<<<<<<< HEAD
    modified_states, modified_grid = modify_grid(periodic_grid, nr_states, e)
=======
    modified_states, modified_grid = modify_grid(periodic_grid, nr_states, e, 5)
>>>>>>> ba921876ae19741fc5274328b4c10ef9ec209e57
    simulated_modified_grid = run_sim(modified_grid, nr_states , 500, e)
    simulated_periodic_grid = run_sim(periodic_grid, nr_states , 500, e)
    print(modified_states)
    


    cmap = colors.ListedColormap([ (0,0,0), (187/255,230/255,179/255), (104/255,227/255,79/255), (47/255,158/255,25/255) , (15/255,67/255,122/255)])
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
<<<<<<< HEAD

    ax.imshow(simulated_periodic_grid, cmap=cmap)
    #ax2.imshow(modified_grid, cmap = cmap)
    ax3.imshow(simulated_modified_grid, cmap = cmap)

=======
    fig4, ax4 = plt.subplots()

    ax.imshow(simulated_periodic_grid, cmap=cmap)
    ax2.imshow(modified_grid, cmap = cmap)
    ax3.imshow(simulated_modified_grid, cmap = cmap)
    ax4.imshow(periodic_grid, cmap=cmap)
>>>>>>> ba921876ae19741fc5274328b4c10ef9ec209e57
    ax.set_xticks(np.arange(0, nr_rows, 1))
    ax.set_yticks(np.arange(0, nr_cols, 1))
    ax2.set_xticks(np.arange(0, nr_rows, 1))
    ax2.set_yticks(np.arange(0, nr_cols, 1))
    ax3.set_xticks(np.arange(0, nr_rows, 1))
    ax3.set_yticks(np.arange(0, nr_cols, 1))
<<<<<<< HEAD
    ax.set_title("Simulated periodic grid")
    ax2.set_title("Slightly modified grid")
    ax3.set_title("Simulated modified grid")
=======
    ax4.set_xticks(np.arange(0, nr_rows, 1))
    ax4.set_yticks(np.arange(0, nr_cols, 1))
    ax.set_title("Simulated periodic grid")
    ax2.set_title("Slightly modified grid")
    ax3.set_title("Simulated modified grid")
    ax4.set_title("Periodic grid")
>>>>>>> ba921876ae19741fc5274328b4c10ef9ec209e57
    plt.show()