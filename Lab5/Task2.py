import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Particle:
    def __init__(self,x,y, x_vel, y_vel,beta) -> None:
        self.x_pos = x
        self.y_pos = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.angle = self.calc_angle()
        self.rad1 = 10
        self.rad2 = 20
        self.rad3 = 100
        self.beta = beta
        
    def calc_angle(self):
        np.arccos(self.x_vel/np.sqrt(self.x_vel**2 + self.y_vel**2))

    def update(self, delta_t):
        rho1 = 0
        rho2 = 1
        rho3 = 0
        rho4 = 0
        self.x_pos += self.x_vel*delta_t
        self.y_pos += self.y_vel*delta_t 
        self.x_vel = (1-self.beta)*(rho1*self.repell_vec()[0] + rho2*self.align_vec(self.align)[0] + rho3*self.attract_vec(self.attract)[0]  + rho4*self.x_vel) +self.beta*self.brownian_motion(delta_t)[0]
        self.y_vel = (1-self.beta)*(rho1*self.repell_vec()[1] + rho2*self.align_vec(self.align)[1] + rho3*self.attract_vec(self.attract)[1] + rho4*self.y_vel) + self.beta*self.brownian_motion(delta_t)[1]
    
    def brownian_motion(self,delta_t):
        c = 0.5
        r_max = 10
        a = 1/(1-np.e**(-r_max**2/(2*c**4*delta_t**2)))
        u = random.uniform(0,1)
        R = np.sqrt(-2*c**4*delta_t**2*np.log((a-u)/a))
        theta = random.uniform(0,2*np.pi)
        return(R*np.cos(theta),R*np.sin(theta))
    def influence(self, particles):

        self.repell = [] # Zone 1
        self.align  = [] # Zone 2
        self.attract  = [] # Zone 3
        for p in particles:
            distance = np.sqrt((self.x_pos - p.x_pos)**2 + (self.y_pos- p.y_pos)**2)
            if distance < self.rad1:
                self.repell += [p]
            elif distance < self.rad2:
                self.align += [p]
            elif distance < self.rad3:
                self.attract += [p]

    def center_of_mass(self,parts):
        x_center = 0
        y_center = 0
        n_count = 0
        for p in parts:
            x_center += p.x_pos
            y_center += p.y_pos
            n_count += 1
        # Should return the angle instead?
        if n_count == 0:
            return(0,0)
        return (x_center/n_count, y_center/n_count) 

    def repell_vec(self):
        #compute the normalized vector from the center of mass to the particle    
        center = self.center_of_mass(self.repell)
        e_1 = (self.x_pos -center[0], self.y_pos-center[1])
        if e_1 == (0,0):
            return (self.x_vel,self.y_vel)
        vec = ( e_1[0]/np.sqrt(e_1[0]**2+e_1[1]**2) , e_1[1]/np.sqrt(e_1[0]**2+e_1[1]**2) )
        return vec
    
    def align_vec(self, parts):
        # For zone 
        angles = []
        for p in parts:
            # Compute angle for particle
            
            angles.append(np.arctan(p.y_pos/p.x_pos))
        angles.append(np.arctan(self.y_pos/self.x_pos))
        
        p_sin = 0
        p_cos = 0

        for theta in angles:
            p_sin += np.sin(theta)
            p_cos += np.cos(theta)
        
        p_measure = np.sqrt(p_sin**2 + p_cos**2)/len(angles)

        newangle = np.arctan(np.sum([np.sin(angle) for angle in angles]/np.sum([np.cos(angle) for angle in angles]))) + random.uniform(-np.pi/6,np.pi/6)
        return (np.cos(newangle),np.sin(newangle))

    def attract_vec(self, parts):
        center=self.center_of_mass(parts)

        e_1 = (self.x_pos -center[0], self.y_pos-center[1])
        if e_1 == (0,0):
            return (self.x_vel,self.y_vel)
        else:
            vec = (-e_1[0]/np.sqrt(e_1[0]**2+e_1[1]**2),-e_1[1]/np.sqrt(e_1[0]**2+e_1[1]**2))
        return vec
    
        
class Simulation:
    def __init__(self,particles):

        self.particles = particles

    
    def update(self,frame):
        for p in self.particles:
            p.influence(self.particles)
            p.update(1)

def beta_plot():
    scatter =[]
    betas = []
    for r in range(30):
        beta = r/30
        nr_particles = 100
        x=[random.uniform(-1,1) for _ in range(nr_particles)]
        particles = [Particle(np.random.uniform(-2.5,2.5), np.random.uniform(-2.5,2.5), x[i], (random.randint(0,1)-1/2)*2*np.sqrt(1-x[i]**2),beta) for i in range(nr_particles)]
        tstop = 20
        simulation = Simulation(particles)
        V_lst = []
        for t in range(tstop):
            vsum = (0,0)
            for p in particles:
                vsum = (vsum[0]+p.x_vel, vsum[1]+p.y_vel)
            V_t = np.sqrt(vsum[0]**2 +vsum[1]**2)/nr_particles
            V_lst.append(V_t)
            simulation.update(0)
        scatter.append(np.mean(V_lst))
        betas.append(beta)
    fig, ax = plt.subplots()
    ax.set_ylim(0,1)
    ax.scatter(betas,scatter)
    plt.show()

def density_plot():
    scatter =[]
    densities = []
    for r in range(1,30):
        beta = 1
        nr_particles = 8*r
        density = nr_particles/25
        x=[random.uniform(-1,1) for _ in range(nr_particles)]
        particles = [Particle(np.random.uniform(-2.5,2.5), np.random.uniform(-2.5,2.5), x[i], (random.randint(0,1)-1/2)*2*np.sqrt(1-x[i]**2),beta) for i in range(nr_particles)]
        tstop = 10
        simulation = Simulation(particles)
        V_lst = []
        for t in range(tstop):
            vsum = (0,0)
            for p in particles:
                vsum = (vsum[0]+p.x_vel, vsum[1]+p.y_vel)
                  
            V_t = np.sqrt(vsum[0]**2 +vsum[1]**2)/nr_particles
            V_lst.append(V_t)
            simulation.update(0)
        scatter.append(np.mean(V_lst))
        densities.append(density)
    fig, ax = plt.subplots()
    ax.set_ylim(0,1)
    ax.scatter(densities,scatter)
    plt.show()

if __name__ == "__main__":
<<<<<<< HEAD
    beta_plot()
    #density_plot()
=======
    density_plot()
>>>>>>> 85e0c25fb98f0a10637fa29ff9f2d22af9e1a8c5
