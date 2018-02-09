
###############  SETUP STATEMENTS  ############

from vpython import *
from numpy import *
# from visual.display  import *
#display(width=350, height=350)
canvas(width=350, height=350)

###############  CONSTANTS  ###################

N = 50                                        # number of paticles
m = 1.0                                       # mass of paticles
L = 5.0                                       # dimensions of the table
R = 0.20                                      # particles radius
A = 50000                                     # force magnitude of particle-particle interaction
v0 = 100.00                                   # initial velocities range
dt = 0.0001                                   # time step


###############  SYSTEM CREATION   ############
# table = box(color=color.yellow, opacity=0.2)
table = box(size=vector(2 * L, 2 * L, 0), color=color.yellow, opacity=0.2)    # create table

#________________  particles List   __________#

particles = []                                # define "particles" as list variable
i = 0
while i < N:                                  # create the list: "particles" with n particles distributed randomely in a box
    #disk = cylinder(pos=(random.uniform(-L + R, L - R), random.uniform(-L + R, L - R), 0), radius=R, axis=(0, 0, R / 5))
    disk = cylinder(pos=vector(random.uniform(-L + R, L - R),
                               random.uniform(-L + R, L - R), 0), radius=R, axis=vector(0, 0, R / 5))
    particles.append(disk)
    i = i + 1

#________________  Velocities List   _________#

v = []                                        # define "v" as list variable
i = 0
# create velocities list with n random initial velocity vectors in the range [-vo,v0]
while i < N:
    velocity = vector(random.uniform(-v0, v0), random.uniform(-v0, v0), 0)
    v.append(velocity)
    i = i + 1

###############  TIME EVOLUTION  ##############

t = 0
while t < 5:
    vpython.rate(1000)
    i = 0
    while i < N:                                            # i indicates one of the particles

        #_________ particle - particle Collisions ____#

        F_net = vector(0, 0, 0)
        j = 0
        while j < N:

            if i != j:
                # Calculate the distance between particle i and particle j
                r = particles[i].pos - particles[j].pos
                r_hat = r / mag(r)
                if mag(r) < 2 * R:
                    F = A * r_hat                # Assume constant interaction
                    F_net = F_net + F
                # else:
                    #F = vector(0, 0, 0)
                # F_net = F_net + F                           # Sum the forces of all the other particle j
            j = j + 1

        #_________ particle - Wall Collisions _____#

        if abs(particles[i].pos.x) > L - R:
            v[i].x = -v[i].x
        if abs(particles[i].pos.y) > L - R:
            v[i].y = -v[i].y

        #_________ Dynamics ___________________#

        # calculate the velocity of each particle
        v[i] = v[i] + (F_net / m) * dt
        # calculate the position of each particle
        particles[i].pos = particles[i].pos + v[i] * dt

        i = i + 1

    t = t + dt
