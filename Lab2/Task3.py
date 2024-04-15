import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

def read_from_file(file_path):
    """
        Reads in values from a .txt file and returns a numpy array
            Input:
                file_path (string) - corresponding to the path of the file
            Output:

        The format of the file needs to be the following;
            1. All characthers should be integers
            2. The first digit specifies the number of rows in the gird
            3. The second digits specifies the number of columns in the grid
            4. The number of following digits must be at least rows*columns.
            5. The values should be in row-major ordering.
    """
    fp = open(file_path, "r")
    rows = int(fp.read(1))
    cols = int(fp.read(1))
    matrix = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            matrix[i,j] = int(fp.read(1))
    fp.close()
    return matrix

def save_to_file(output_name, array):
    rows, cols = array.shape
    fp = open(output_name, "w")
    fp.write(str(int(rows)))
    fp.write(str(int(cols)))
    for i in range(rows):
        for j in range(cols):
            fp.write(str(int(array[i,j])))
    fp.close()
    pass

def run_sim(grid, num_states, num_steps, e):
    # Iterates the GH a number of times
    for i in range(num_steps):
        sim = iterate_CA(grid, num_states, e)
    return sim

def nbh_check(grid, i, j, e):
    # Check if a node has an excited neighbour
    nr_rows,nr_cols = grid.shape 
    for k in range(-1,2):
        for l in range(-1,2):
            element = grid[(i+k)% nr_rows, (j+l) % nr_cols]
            if( element > 0 and element <= e ):
                return 1
    return 0


def iterate_CA(grid, N, e):
    # Do one iteration of the Greenberg-Hasting on a torus
    # with N total states and e excited states
    nr_rows, nr_cols = grid.shape 
    next_grid = np.zeros((nr_rows, nr_cols))
    for i in range(nr_rows):
        for j in range(nr_cols):
            if grid[i,j] != 0:
                next_grid[i,j] = (grid[i,j]+1) % N
            else:
                next_grid[i,j] = nbh_check(grid ,i ,j ,e)

    return next_grid


if __name__ == "__main__":

    # Define grid as n x m matrix
    nr_rows = 50
    nr_cols = 50

    mat = read_from_file("Lab2/test.txt")
    print(mat)
    save_to_file("Lab2/out.txt", mat)

    #SetCA rules
    nr_states = 5
    states = [x for x in range(nr_states)]
    e = 1 # {1,2,..e} are the excited states
    excited_states = [x for x in range(1, e+1)]
    # Use uniform dist initial on set {0,..., N-1}
    init_state = np.random.randint(low = 0, high = nr_states, size = (nr_rows, nr_cols))
    nr_steps = 1

    final_state = run_sim(init_state, nr_states, nr_steps, e)

    cmap = colors.ListedColormap([ (0,0,0), (187/255,230/255,179/255), (104/255,227/255,79/255),
                                   (47/255,158/255,25/255) , (15/255,67/255,122/255)])
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    ax.imshow(final_state, cmap=cmap)
    ax2.imshow(init_state, cmap = cmap)
    ax.set_xticks(np.arange(0, nr_rows, 1))
    ax.set_yticks(np.arange(0, nr_cols, 1))
    ax2.set_xticks(np.arange(0, nr_rows, 1))
    ax2.set_yticks(np.arange(0, nr_cols, 1))
    ax.set_title("Final")
    ax2.set_title("Inital")
    plt.show()