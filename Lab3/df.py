import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class Particle:
def __init__(self,x,y, x_vel, y_vel) -> None:
self.x_pos = x
self.y_pos = y
self.x_vel = x_vel
self.y_vel = y_vel
self.angle = self.calc_angle()
self.rad1 = 5
self.rad2 = 20
self.rad3 = 30
def calc_angle(self):
np.arccos(self.x_vel/np.sqrt(self.x_vel**2 + self.y_vel**2))
def update(self, delta_t):
rho1 = 0.25
rho2 = 0.25
rho3 = 0.25
rho4 = 0.25
alpha = 0.9
beta = 0.1
self.x_pos += alpha*self.x_vel*delta_t + beta*self.brownian_motion(delta_t)[0]
self.y_pos += self.y_vel*delta_t + beta*self.brownian_motion(delta_t)[1]
self.x_vel = rho1*self.repell_vec()[0] + rho2*self.align_vec(self.align)[0] +
rho3*self.attract_vec(self.attract)[0] + rho4*self.x_vel
self.y_vel = rho1*self.repell_vec()[1] + rho2*self.align_vec(self.align)[1] +
rho3*self.attract_vec(self.attract)[1] + rho4*self.y_vel