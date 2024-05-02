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
                self.status = "susceptible"

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
        self.infection_probabilitiy = 0.3 # User defined parameter
        self.recover_probability = 0.2 # User defined parameter

    
    def __str__(self) -> str:
        return f"Cell: {self.population}"
    
    def __repr__(self) -> str:
        return f"Cell({self.population}, {self.num_rest_channel})"
    
    def populate(self, population, status):
        """Create initial random population in a cell"""
        self.population = population
        for i in range(population):
            person = Person(status)
            self.place_person(person)

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
        
    def place_person(self, person):
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
    
    def random_movement(self):
        # Get population
        cell_population = self.rest_channel + self.velocity_channel
        # Shuffle list
        random.shuffle(cell_population)
        self.rest_channel = [None]*self.num_rest_channel
        self.velocity_channel = [None]*self.num_vel_channel
        
        # Distribute people randomly around the channels
        for person in cell_population:
            self.place_person(person)
                        
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
                if person.status == "susceptible":
                    susceptible += 1
                elif person.status == "infected":
                    infected += 1
                elif person.status == "vaccinated":
                    vaccinated += 1
                else:
                    recovered += 1

        for person in self.velocity_channel:
            if person:
                if person.status == "susceptible":
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
        self.num_rest_channels = 2
        for q in range(0, right+1 ):
            q_offset = math.floor(q/2.0)
            for r in range(0-q_offset, bottom - q_offset +1):
                self.grid[Hex(q,r,-q-r)] =  Cell(random.randint(0,8), self.num_rest_channels)

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
    
    def reset(self):
        
        for cell in self.grid.values():
            cell.empty()

    def place_ring(self):
        center = OffsetCoord(round(self.col/2), round(self.row/2))
        center = qoffset_to_cube(ODD, center)
        radius = 20
        
        assert(radius < min((self.col, self.row))) # A bit useless
        
        vaccinated_tiles = []
        ring_width = 3 #width of the ring 

        for i in range(ring_width):
            vaccinated_tiles += hex_ring(center, radius + i) # A list of hexes

        infected_tiles = hex_spiral(center, radius - 1) # A list
        infected_prop_parameter = 0.3
        
        cell_count_except_ring = len(self.grid)- len(vaccinated_tiles) 

        return infected_tiles, vaccinated_tiles, cell_count_except_ring
        
    
    def populate_grid(self, type = ""):
        self.reset()
        num_susceptible = 16_000
        num_vaccinated = 1_000
        num_infected = 10
        if type.lower() == "ring":
            inner_tiles, ring_tiles, cell_count_except_ring = self.place_ring()
            non_ring_tiles = set(self.grid.keys()).difference(set(ring_tiles))
            non_ring_tiles = list(non_ring_tiles)
            non_ring_tiles_dist = self.random_population(num_susceptible, len(non_ring_tiles), np.zeros(num_susceptible))
            print(np.count_nonzero(non_ring_tiles_dist)) 
            ring_dist = self.random_population(num_vaccinated, len(ring_tiles), np.zeros(num_vaccinated))
    
            # Ring
            for i, tile in enumerate(ring_tiles):
                self.grid[tile].populate(int(ring_dist[i]), "vaccinated")
            # The rest
            for i, tile in enumerate(non_ring_tiles):
                self.grid[tile].populate(int(non_ring_tiles_dist[i]), "susceptible")
            
            for i in range(num_infected):
                tile = random.choice(inner_tiles)
                while self.grid[tile].population == 8:
                    tile = random.choice(inner_tiles)

                person = Person("infected")
                self.grid[tile].place_person(person)
                self.grid[tile].population += 1

        else:
            # Boilerplate, but eeeh

            inner_tiles = self.place_ring()[0]
            susceptible_dist = self.random_population(num_susceptible, len(self.grid), np.zeros(num_susceptible)) 
            vaccinated_dist = self.random_population(num_vaccinated, len(self.grid), susceptible_dist)
            # Place susceptible, Place vaccinated
            for i, tile in enumerate(self.grid.keys()):
                self.grid[tile].populate(int(susceptible_dist[i]), "susceptible")
                self.grid[tile].populate(int(vaccinated_dist[i]), "vaccinated")
                self.grid[tile].population = susceptible_dist[i] + vaccinated_dist[i]

            for i in range(num_infected):
                tile = random.choice(inner_tiles)
                while self.grid[tile].population == 8:
                    tile = random.choice(inner_tiles)

                person = Person("infected")
                self.grid[tile].place_person(person)
                self.grid[tile].population += 1

    def random_population(self, population, map_size, initial_distribution):
        resulting_distribution = np.copy(initial_distribution)
        for i in range(population):
            index = random.randint(0, map_size - 1)
            while resulting_distribution[index] == 8:
                index = random.randint(0, map_size)
            
            resulting_distribution[index] += 1
        
        resulting_distribution = resulting_distribution - initial_distribution
        return resulting_distribution
            

if __name__ == "__main__":

    time_start = time.perf_counter()
    steps = 80
    grid = Hex_grid(100,100)
    grid.populate_grid()
    print("Initial population:", grid.calc_population())
    num_sims = 100
    susceptible = np.empty((num_sims,steps))
    infected = np.empty((num_sims,steps))
    vaccinated = np.empty((num_sims,steps))
    recovered = np.empty((num_sims,steps))

    susceptible_no_barr = np.empty((num_sims,steps))
    infected_no_barr = np.empty((num_sims,steps))
    vaccinated_no_barr = np.empty((num_sims,steps))
    recovered_no_barr = np.empty((num_sims,steps))
    
    for j in range(num_sims):
        grid.populate_grid()
        susceptible[j,0], infected[j,0], vaccinated[j,0], recovered[j,0] = grid.hex_grid_demographic()

        for i in range(1, steps):
            grid.propagate_step()
            susceptible[j,i], infected[j,i], vaccinated[j,i], recovered[j,i] = grid.hex_grid_demographic()
    
    # Reset the grid
    for j in range(num_sims):
        grid.populate_grid()
        susceptible_no_barr[j,0], infected_no_barr[j,0], vaccinated_no_barr[j,0], recovered_no_barr[j,0] = grid.hex_grid_demographic()

        for i in range(1, steps):
            grid.propagate_step()
            susceptible_no_barr[j,i], infected_no_barr[j,i], vaccinated_no_barr[j,i], recovered_no_barr[j,i] = grid.hex_grid_demographic()


    print("Time taken:", time.perf_counter() - time_start)

    susceptible = np.average(susceptible, axis=0)
    infected = np.average(infected, axis=0)
    vaccinated = np.average(vaccinated, axis=0)
    recovered = np.average(recovered, axis=0)

    susceptible_no_barr = np.average(susceptible_no_barr, axis=0)
    infected_no_barr = np.average(infected_no_barr, axis=0)
    vaccinated_no_barr = np.average(vaccinated_no_barr, axis=0)
    recovered_no_barr = np.average(recovered_no_barr, axis=0)

    x = np.linspace(0, steps, steps)
    #plt.plot(x, susceptible)
    plt.plot(x, infected)
    plt.plot(x, infected_no_barr)
    plt.title("Average infected over 100 simulations")
    plt.xlabel("Number of steps")
    plt.ylabel("Number of infected")
    plt.legend(["Barrier", "No barrier"])
    plt.savefig("Average_infected.eps", format = "eps", bbox_inches = 'tight')
