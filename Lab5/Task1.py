import numpy as np

class particle:
    def __init__(self,x,y, x_vel, y_vel) -> None:
        self.x_pos = x
        self.y_pos = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.angle = self.calc_angle()
        self.rad1 = 10
        self.rad2 = 20 
        self.rad3 = 30
        
    def calc_angle(self):
        np.arccos(self.x_vel/np.sqrt(self.x_vel**2 + self.y_vel**2))

    def update(self, delta_t):
        rho1 = 0.2
        rho2 = 0.2
        rho3 = 0.2
        rho4 = 0.2
        self.x_pos += self.x_vel*delta_t
        self.y_pos += self.y_vel*delta_t
        #self.x_vel = rho1*bla + rho2*bla2 + rho3* + rho4*self.x_vel
        #self.y_vel = rho1*bla + rho2*bla2 + rho3* + rho4*self.y_vel
        
        
    def influence(self, particles):
        self.repell = [] # Zone 1
        self.align  = [] # Zone 2
        self.attract  = [] # Zone 3

        for p in particles:
            if p != self:
                distance = np.sqrt((self.x_pos - p.x_pos)**2 + (self.y_pos- p.y_pos)**2)
                if distance < self.rad1:
                    self.repell += [p]
                elif distance < self.rad2:
                    self.align += [p]
                elif distance < self.rad3:
                    self.attract += [p]

    def center_of_mass_in_zone(parts):
        x_center = 0
        y_center = 0
        n_count = 0

        for p in parts:
            x_center += p.x_pos
            y_center += p.y_pos
            n_count += 1
        # Should return the angle instead?
        return (x_center/n_count, y_center/n_count) 
    
    def vec_away_from_mass(self, particles):
        #compute the normalized vector from the center of mass to the particle
        self.influence(particles)
        center = self.center_of_mass_in_zone(self.repell)
        e_1 = (self.x_pos -center[0], self.y_pos-center[1])
        e_1 = e_1/np.sqrt(e_1[0]**2+e_1[1]**2)
    
    def polarization(self, parts):
        # For zone 
        angles = []
        for p in parts:
            # Compute angle for particle
            angles.append(np.arctan(p.y/p.x))
        
        p_sin = 0
        p_cos = 0

        for theta in angles:
            p_sin += np.sin(theta)
            p_cos += np.cos(theta)
        
        p_measure = np.sqrt(p_sin**2 + p_cos**2)/len(angles)

class simulation:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    pass