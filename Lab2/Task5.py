import numpy as np
import random
from Task3 import *

def modify_grid(grid,N,e):
    nr_rows , nr_cols =grid.shape
    modified_cells = []
    for cells in range(5):
        row = random.randint(0,nr_rows)
        col = random.randint(0,nr_cols)
        while (row,col) in modified_cells:
            row = random.randint(0,nr_rows)
            col = random.randint(0,nr_cols)
        modified_cells.append((row,col))

        state = random.randint(0,N-1)
        while grid[row,col] == state:
            state = random.randint(0,N-1)
        grid[row,col] == state
    return grid, modified_cells
           

