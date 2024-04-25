from hex_funcs import *
import random

hex_gird  = []

left = 0
right = 6
top = 0
bottom = 4
for q in range(left, right+1 ):
    q_offset = math.floor(q/2.0)
    for r in range(top-q_offset, bottom - q_offset +1):
        hex_gird.append(Hex(q,r,-q-r))

print(hex_gird)

class hex_gird:
    def __init__(self) -> None:
        grid = []
        pass
    
    def propagate_step(self):
        # For each cell take get the neighbours and move
        pass

class Person:
    # 1: S
    # 2: I
    # 3: R
    # 4: V
    def __init__(self, status, vaccine):
        self.status = status # S I R?
        self.immunity = 0
        if self.status == "vaccinated":
            self.to_recovery = k
    
    def update(self, prob):
        if self.immunity == 0 and self.status == "sus":
            sample = random.random()
            if(sample < prob):
                self.status = "infected"
                self.to_recovery = k

        if self.status == "recovered":
            self.immunity -= 1
            if self.immunity == 0:
                self.status = "sus"

        if self.status == "vaccinated":
            self.to_recovery -= 1
            if self.to_recovery == 0:
                self.status = "recovered"
                self.immunity = l
    
    def get_status(self):
        return self.status
    
    def is_infected(self):
        return True if self.status == "infected" else False
       
class Cell:
    def __init__(self, hex, population, num_rest_channels, model_states):
        self.hex = hex
        self.population = population
        self.num_rest_channel = num_rest_channels
        self.num_vel_channel = 6 # The number of vel chanels
        self.velocity_channel = [None]*self.num_vel_channel # 0,..5 should only be len 6
        self.rest_channel = [None]*self.num_rest_channel # should be len rest_channels
        self.infection_probabilitiy = 0.1 # User defined parameter
        self.recover_probability = 0.05 # User defined parameter
        # Create inital randomish population in cell
        for i in range(population):
                person = Person() # Decide on this!!!
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
    
    def contact_interaction(self):
        # Count number of infected
        num_infected = 0
        cell_population = self.rest_channel + self.velocity_channel
        for person in cell_population:
            if person.is_infected() == True:
                num_infected += 1
        # Compute the probability
        probability = 1 -(1 - self.infection_probabilitiy)**num_infected
        # Update status; infect, recover etc
        for person in cell_population:
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





    



