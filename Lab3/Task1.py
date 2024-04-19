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

class Cell:
    def __init__(self, hex, population, num_rest_channels, model_states):
        self.hex = hex
        self.population = population
        self.num_rest_channel = num_rest_channels
        self.velocity_channels = [0 for i in range(6)] # 0,..5 should only be len 6
        self.rest_channel = [0 for i in range(num_rest_channels)] # should be len rest_channels
        self.infection_probabilitiy = 0.1
        # Create inital randomish population in cell
        for i in range(population):
            # Sample
            x = random.randint(0,1)
            if(x == 0):
                # Add to vel channel
                index = random.randint(0,5)
                self.velocity_channels[index] = random.randint(1,4)
                # 1: S
                # 2: I
                # 3: R
                # 4: V
            else:
                # Add to rest
                index = random.randint(0, num_rest_channels-1)
                self.rest_channels[index] = random.randint(1,4)
    
    def contact_interaction(self):
        # Count number of infected
        num_infected = 0
        for i in range(len(self.velocity_channels)):
            if self.velocity_channels[i] == 2: # Infected
                num_infected += 1
        for i in range(len(self.rest_channel)):
            if self.rest_channel[i] == 2: # Infected
                num_infected += 1
        
    def random_movement():
        pass
    









    



