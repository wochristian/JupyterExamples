
###############  SETUP STATEMENTS  ############

from vpython import *
# from visual.graph import *
from numpy import *
canvas(width=350, height=350)

###############  CONSTANTS  ###################

N = 40                                        # number of paticles
m = 1.0                                       # mass of paticles
L = 4.0                                       # dimensions of the table
R = 0.30                                      # particle radius
A = 50000                                     # force magnitude of ball-ball interaction
v0 = 50                                    # initial velocities
dt = 0.0001                                   # time step
a = 500

###############  SYSTEM CREATION   ############

table = box(size=vector(2 * L, 2 * L, 0), color=color.yellow, opacity=0.2)    # table
monitor = box(pos=vector(0, 0, 0), size=vector(L / 5, 2 * L, 0), color=color.white, opacity=0.5)

#________________  particles List   ______________#

particles = []                                # define "particles" as list variable
i = 0
# creating the list: "particles" with n particles distributed randomely in a box (rho_0*L x rho_0*L x rho_0*L)
while i < N:
    particle = cylinder(pos=vector(random.uniform(-L + 2 * R, -L / 5),
                                   random.uniform(-L + 2 * R, L - 2 * R), 0), radius=R, axis=vector(0, 0, R / 5))
    particles.append(particle)
    i = i + 1

#________________  Velocities List   _________#

v = []                                        # define "v" as list variable
i = 0
# creating the velocities list with n random initial velocity vectors in the range [-vo,v0]
while i < N:
    velocity = vector(random.uniform(-v0, v0), random.uniform(-v0, v0), 0)
    v.append(velocity)
    i = i + 1

#_________________  Graphs   _________________#

canvas(x=350, y=0, width=350, height=350, xtitle='t', ytitle='N')
#avg_N_t = gdots(color=color.blue, shape="square", size=15)
avg_N_t = gdots(color=color.blue, size=15)
N_t = gcurve(color=color.yellow)
#canvas(x=700, y=0, width=350, height=350, xtitle='x', ytitle='N', ymax=N / 10)
#pos_dist = ghistogram(bins=arange(-L, L, L / 10), color=color.green, accumulate=True, average=True)

###############  TIME EVOLUTION  ##############
avg_N = 0
t = 0
while t < 0.5:
    vpython.rate(100000)

    positions = []                            # Reset density_x List #
    counter = 0                               # Reset density_t variable #
    i = 0
    while i < N:                              # i indicates one of the particles

        #_________ particle - particle Collisions ____#

        F_net = vector(0, 0, 0)
        j = 0
        while j < N:

            if i != j:
                # Calculate the distance between particle i and particle j
                r = particles[i].pos - particles[j].pos
                r_hat = r / mag(r)
                if mag(r) < 2 * R:
                    F = A * r_hat    # Assume constant interaction while colliding
                else:
                    F = vector(0, 0, 0)
                # Sum the forces of all the other particle (j) - for the case of collisions between more than two particles.
                F_net = F_net + F
            j = j + 1

        #_________ particle - Wall Collisions _____#

        if abs(particles[i].pos.x) > L - 2 * R:
            v[i].x = -v[i].x
        if abs(particles[i].pos.y) > L - 2 * R:
            v[i].y = -v[i].y

        #_________ Dynamics ___________________#

        # calculate the velocity of each particle
        v[i] = v[i] + (F_net / m) * dt
        # calculate the position of each particle
        particles[i].pos = particles[i].pos + v[i] * dt

        if particles[i].pos.x > -L / 10 and particles[i].pos.x < L / 10:
            counter = counter + 1.0  # Density - time monitor

        positions.append(particles[i].pos.x)

        i = i + 1

    #_________ Graphs _____#

    if t % (a * dt) > dt:
        avg_N = avg_N + counter
    else:
        avg_N_t.plot(pos=(t, avg_N / a))
        avg_N = 0

    N_t.plot(pos=(t, counter))
    # pos_dist.plot(data=positions)

    t = t + dt
