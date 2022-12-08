import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm

import random


class Swarm ():
    # max eggholder bounds
    negative_bound = -512
    positive_bound = 512
    
    # eggholder coords and formula
    x = np.outer(np.linspace(negative_bound, positive_bound, 100), np.ones(100))
    y = x.copy().T


    def z(x, y):
        return -(y + 47)*np.sin(np.sqrt(abs(x/2+(y+47))))-x*np.sin(np.sqrt(abs(x-(y + 47))))


    # visualising function
    def eggholder(self, array_of_X, array_of_Y, array_of_Z):
        fig = plt.figure(figsize = (12, 5))

        # original func
        axes_orig = fig.add_subplot(1, 3, 1, projection = "3d")
        axes_orig.plot_surface(self.x, self.y, Swarm.z(self.x, self.y), cmap=cm.ocean, alpha = 0.5)
        axes_orig.set_title("Eggholder")

        # func with dots
        axes = fig.add_subplot(1, 3, 2, projection = "3d")
        axes.plot_surface(self.x, self.y, Swarm.z(self.x, self.y), cmap=cm.coolwarm, alpha = 0.5)
        axes.set_title("Eggholder with dots")
        axes.scatter(array_of_X, array_of_Y, array_of_Z, c = "red", alpha = 0.7)

        # func from above
        axes_above = fig.add_subplot(1, 3, 3, projection = "3d")
        axes_above.axis("off")
        axes_above.plot_surface(self.x, self.y, Swarm.z(self.x, self.y), cmap=cm.coolwarm, alpha = 0.5)
        axes_above.set_title("Eggholder with dots from above")
        axes_above.scatter(array_of_X, array_of_Y, array_of_Z, c = "red", alpha = 0.4)
        axes_above.view_init(90, 0)

        elevation = 20
        rotation_speed = 5

        for angle in range(0, 360, 3):
            axes_orig.view_init(elevation, angle)
            axes.view_init(elevation, angle)
            plt.draw()
            plt.pause(.01)


    def __init__(self, epoch, points):
        global_min    = []
        local_min     = {}
        particle_dict = {}
        velocity      = {} 
        
        for point in range(1, points):
            particle_dict[point] = [random.randint(self.negative_bound, self.positive_bound) for i in range(2)]
            velocity[point] = [random.randint(-11,11) for i in range(2)]
            local_min[point] = particle_dict[point]

        global_min = self.search_global_min(Swarm.z, local_min)

        for key in particle_dict.keys():
            
            x_coordinate = particle_dict[key]
            y_coordinate = local_min[key]
            
            x = Swarm.z(x_coordinate[0], x_coordinate[1])
            y = Swarm.z(y_coordinate[0], y_coordinate[1])
            
            if x < y:
                local_min[key] = x_coordinate
                g = Swarm.z(global_min[0], global_min[1])
                if y < g:
                    global_min[0] = x_coordinate[0]
                    global_min[1] = x_coordinate[1]
        
        for i in range(epoch):

            for key in particle_dict.keys():

                alpha = random.randint(0,1)
                beta  = random.randint(0,1)

                np_par = np.array(particle_dict[key])
                np_loc = np.array(local_min[key])
                np_vel = np.array(velocity[key])
                np_glo = np.array(global_min)

                velocity[key]      = ((np.multiply(alpha,(np_loc-np_par))) + (np.multiply(beta,(np_glo - np_par)))).tolist()
                if  (-512 < (np_par + np_vel)[0] < 512) and (-512 < (np_par + np_vel)[1] < 512): 
                    particle_dict[key] = (np_par + np_vel).tolist()

                x_coordinate = particle_dict[key]
                y_coordinate = local_min[key]

                if ((x_coordinate[0] <= 512) & (x_coordinate[1] <= 512)) & ((x_coordinate[0] >= -512) & (x_coordinate[1] >= 512)):
                    x = Swarm.z(x_coordinate[0], x_coordinate[1])


                y = Swarm.z(y_coordinate[0], y_coordinate[1])

                if x < y:
                    local_min[key] = x_coordinate
                    atm_glob_min = Swarm.z(global_min[0], global_min[1])
                    if y < atm_glob_min:
                        global_min[0] = x_coordinate[0]
                        global_min[1] = x_coordinate[1]

        x_particles = list(map(lambda xy_values: xy_values[0], particle_dict.values()))
        y_particles = list(map(lambda xy_values: xy_values[1], particle_dict.values()))
        z_particles = []

        for i in range(len(x_particles)):
            z_particles.append(Swarm.z(x_particles[i], y_particles[i]))

        self.eggholder(x_particles, y_particles, z_particles)


    def search_global_min(self, z_func, local_min):
        
        global_min = local_min[1]

        for key in local_min.keys():

            coordinate = local_min[key]
            better     = z_func(coordinate[0], coordinate[1])
            worse      = z_func(global_min[0], global_min[1])
            
            if better < worse:
                global_min[0] = coordinate[0]
                global_min[1] = coordinate[1]

        return global_min




Swarm(epoch = 10, points = 100)