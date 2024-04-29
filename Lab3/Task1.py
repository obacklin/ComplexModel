from hex_funcs import *
import random
import matplotlib.pyplot as plt
import numpy as np
import time

class Person:
    def __init__(self, status:str):
        self.status = status # S I R?
        self.immunity = 0
        self.k = 3
        self.l = 30
        if self.status == "vaccinated":
            self.to_recovery = self.k
    
    def __str__(self) -> str:
        return self.status
    
    def __repr__(self) -> str:
        return self.status
    
    def update(self, prob, recover_prob):
        if self.immunity == 0 and self.status != "infected":
            sample = random.random()
            if(sample < prob):
                self.status = "infected"
                self.to_recovery = self.k

        if self.status == "recovered":
            self.immunity -= 1
            if self.immunity == 0:
                self.status = "sus"

        if self.status == "vaccinated":
            self.to_recovery -= 1
            if self.to_recovery == 0:
                self.status = "recovered"
                self.immunity = self.l
        
        if self.status == "infected":
            sample = random.random()
            if sample < recover_prob:
                self.status = "recovered"
                self.immunity = self.l
    
    def get_status(self):
        return self.status
    
    def is_infected(self):
        return True if self.status == "infected" else False
       
class Cell:
    def __init__(self, population:int,  num_rest_channels:int):
        self.population = population
        self.num_rest_channel = num_rest_channels
        self.num_vel_channel = 6 # The number of vel chanels
        self.velocity_channel = [None]*self.num_vel_channel # 0,..5 should only be len 6
        self.rest_channel = [None]*self.num_rest_channel # should be len rest_channels
        self.temp_velocity_channel = [None]*self.num_vel_channel
        self.infection_probabilitiy = 0.1 # User defined parameter
        self.recover_probability = 0.05 # User defined parameter

    
    def __str__(self) -> str:
        return f"Cell: {self.population}"
    
    def __repr__(self) -> str:
        return f"Cell({self.population}, {self.num_rest_channel})"
    
    def populate(self, prop_infected, prop_vaccinated):
        """Create initial random population in a cell"""
        self.empty()
        for i in range(self.population):
                sample = random.random()
                if sample < prop_infected:
                    initial_status = "infected"
                elif sample < prop_infected + prop_vaccinated:
                    initial_status = "vaccinated"
                else:
                    initial_status = "sus"

                person = Person(initial_status) # Decide on this!!!
                placed = False
                while not placed:
                    # Place until a position is found
                    x = random.randint(0, 1) # Velocity or Rest
                    if(x == 0):
                        y = random.randint(0, self.num_rest_channel - 1)
                        if( not self.rest_channel[y] ):
                            # Channel is empty insert person
                            self.rest_channel[y] = person
                            placed = True
                    else:
                        y = random.randint(0, self.num_vel_channel - 1)
                        if( not self.velocity_channel[y]):
                            # Channel is empty insert person
                            self.velocity_channel[y] = person
                            placed = True

    def empty(self):
        self.rest_channel = [None]*self.num_rest_channel
        self.velocity_channel = [None]*self.num_vel_channel

    def contact_interaction(self):
        # Count number of infected
        num_infected = 0
        cell_population = self.rest_channel + self.velocity_channel
        for person in cell_population:
            if person and person.is_infected():
                num_infected += 1
        # Compute the probability
        probability = 1 -(1 - self.infection_probabilitiy)**num_infected
        # Update status; infect, recover etc
        for person in cell_population:
            if person:
                person.update(probability, self.recover_probability)
        
    def random_movement(self):
        # Get population
        cell_population = self.rest_channel + self.velocity_channel
        # Shuffle list
        random.shuffle(cell_population)
        self.rest_channel = [None]*self.num_rest_channel
        self.velocity_channel = [None]*self.num_vel_channel
        # Distribute people randomly around the channels
        
        for person in cell_population:
            placed = False
            while not placed:
                # Place until a position is found
                x = random.randint(0, 1) # Velocity or Rest
                if(x == 0):
                    y = random.randint(0, self.num_rest_channel - 1)
                    if( not self.rest_channel[y] ):
                        # Channel is empty insert person
                        self.rest_channel[y] = person
                        placed = True
                else:
                    y = random.randint(0, self.num_vel_channel - 1)
                    if( not self.velocity_channel[y]):
                        # Channel is empty insert person
                        self.velocity_channel[y] = person
                        placed = True
                        
    def receive_new_person(self, person:Person, position):
        self.temp_velocity_channel[position] = person
    
    def switch_velocity_channel(self):

        self.velocity_channel = self.temp_velocity_channel
        self.temp_velocity_channel = [None]*self.num_vel_channel

    def remove_person(self, person):
        for i in range(len(self.rest_channel)):
            if self.rest_channel[i] == person:
                self.rest_channel[i] = None
        for i in range(len(self.velocity_channel)):
            if self.velocity_channel[i] == person:
                self.velocity_channel[i] = None
    
    def calc_population(self):
        population = 0
        for person in self.rest_channel:
            if person:
                population += 1
        for person in self.velocity_channel:
            if person:
                population += 1
        self.population = population

    def demographic(self):
        susceptible = 0
        infected = 0
        vaccinated = 0
        recovered = 0
        for person in self.rest_channel:
            if person:
                if person.status == "sus":
                    susceptible += 1
                elif person.status == "infected":
                    infected += 1
                elif person.status == "vaccinated":
                    vaccinated += 1
                else:
                    recovered += 1

        for person in self.velocity_channel:
            if person:
                if person.status == "sus":
                    susceptible += 1
                elif person.status == "infected":
                    infected += 1
                elif person.status == "vaccinated":
                    vaccinated += 1
                else:
                    recovered += 1

        return susceptible, infected, vaccinated, recovered


class Hex_grid:
    
    def __init__(self, right:int, bottom:int) -> None:    
        self.grid = {}
        for q in range(0, right+1 ):
            q_offset = math.floor(q/2.0)
            for r in range(0-q_offset, bottom - q_offset +1):
                self.grid[Hex(q,r,-q-r)] =  Cell(random.randint(0,8), 2)

        # Find max column, row in offset cords
        self.col = 0
        self.row = 0
        for key in self.grid:
            cord = qoffset_from_cube(ODD, key)
            if cord.col > self.col:
                self.col = cord.col
            if cord.row > self.row:
                self.row = cord.row
        # Adjust for length
        self.col += 1
        self.row += 1

    def propagate_step(self):
        for hex_key, cell_value in self.grid.items():
            cell_value.contact_interaction() # Infect, recover, etc
            cell_value.random_movement() # random_movement
            for i, person in enumerate(cell_value.velocity_channel):
                if person:
                    self.transfer_person(hex_key, person, i)
        # Switch vel_channels
        for hex_key, cell_value in self.grid.items():
            cell_value.switch_velocity_channel()

    def transfer_person(self, curr_hex, person:Person, direction:int):
        # Find corresponding cell
        neighbour_hex = hex_neighbor(curr_hex, direction)
        neighbour_offset_cord = qoffset_from_cube(ODD, neighbour_hex)
        neighbour_hex = qoffset_wraparound_to_hex(neighbour_offset_cord, self.col, self.row)

        neighbour_cell = self.grid[neighbour_hex]
        neighbour_cell.receive_new_person(person, direction)

    def hex_grid_demographic(self):
        susceptible = 0
        infected = 0
        vaccinated = 0
        recovered = 0
        for hex_key, cell_value in self.grid.items():
            sus_in_cell, inf_in_cell, vac_in_cell, rec_in_cell = cell_value.demographic()
            susceptible += sus_in_cell
            infected += inf_in_cell
            vaccinated += vac_in_cell
            recovered += rec_in_cell

        return susceptible, infected, vaccinated, recovered
    
    def calc_population(self):
        population = 0
        for hex_key, cell_value in self.grid.items():
            cell_value.calc_population()
            population += cell_value.population
        
        return population

    def place_ring(self):
        center = OffsetCoord(round(self.col/2), round(self.row/2))
        center = qoffset_to_cube(ODD, center)
        radius = round(min(self.col,self.row)/3)
        assert(radius > 1)
        vaccinated_tiles = hex_ring(center, radius) # A list of hexes
        infected_tiles = hex_spiral(center, radius - 1) # A list
        infected_prop_parameter = 0.3
        # Populate
        for tile in self.grid.values():
            tile.populate(0,0)

        for tile in vaccinated_tiles:
            self.grid[tile].populate(0,1)

        for tile in infected_tiles:
            self.grid[tile].populate(infected_prop_parameter, 0)
        
    
    def populate_grid(self, type = "", prop_infected=0.1, prop_vaccinated=0.2):
        
        if type.lower() == "ring":
            self.place_ring()
        else:
            for cell in self.grid.values():
                x = random
                cell.populate(prop_infected, prop_vaccinated)


def plot_grid():
    pass



if __name__ == "__main__":
    start_time = time.perf_counter()
    steps = 1
    grid = Hex_grid(50,50)
    grid.populate_grid("ring")
    # print("Initial population:", grid.calc_population())
    grid.propagate_step()
    time_taken = time.perf_counter() - start_time
    print("Done!, time: ", time_taken)
    # susceptible = np.empty(steps)
    # infected = np.empty(steps)
    # vaccinated = np.empty(steps)
    # recovered = np.empty(steps)

    # susceptible[0], infected[0], vaccinated[0], recovered[0] = grid.hex_grid_demographic()
    # for i in range(steps):
    #     grid.propagate_step()
    #     susceptible[i], infected[i], vaccinated[i], recovered[i] = grid.hex_grid_demographic()
    #     #print(grid.calc_population())

    # x = np.linspace(0, steps, steps)
    # plt.plot(x, susceptible)
    # plt.plot(x, infected)
    # plt.plot(x, vaccinated)
    # plt.plot(x, recovered)
    # plt.legend(["sus","inf","vaxx", "rec"])
    # plt.show()