# Adapted from Weizmann Institute code by Wolfgang Christian
from vpython import *
from numpy import *

# Hard-sphere gas with simple evolution

win = 250

# Typical values
N = 50                                        # number of paticles
mass = 1.0                                  # mass of paticles
k = 1                                           # Boltzmann's constant
L = 5.0                                       # dimensions of the box containing the particles
R = 0.20                                     # particle radius
A = 50000                                  # force magnitude of particle-particle interaction
v0 = 100.00                                # initial velocities range
T = 0.5 * mass * v0 * v0 / k       # TemperatureI
dt = 0.0005                                 # time step
t = 0                                            # time
deltav = 20                                 # bin size for v histogram
nbins = 25                                  # number of bins
histo = []                                   # histogram bins
nhisto = 0                                   # number of histogram snapshots that are being averaged
r = []                                           # position vector list
v = []                                           # velocity vector list
a = []                                           # acceleration vector list
particles = []                                # particle list ; each particle is a vpython cylinder
accum = []                                   # stores for histogram averages
running = True                            # stops animation when false


def run(b):
    global running
    running = not running
    if running:
        b.text = "Pause"
    else:
        b.text = "Run"
    evolve(running)


def clearHistogram(b):
    global accum
    for i in range(len(accum)):
        accum[i][1] = 0
    global nhisto
    nhisto = 0


def speedHistogram(v, bins):
    nbin = len(bins)
    for i in range(nbin):
        bins[i] = 0
    nv = len(v)
    for i in range(nv):
        speed = math.sqrt(v[i].x * v[i].x + v[i].y * v[i].y)
        index = int(min(speed / deltav, nbin - 1))
        bins[index] += 1.0
    return bins


# Advance the position and velocity vectors using the Euler algorithm
def eulerAlgorithm(n, r, v, a):
    for i in range(n):
        v[i] = v[i] + a[i] * dt  # compute the new velocity of each particle
        r[i] = r[i] + v[i] * dt   # compute the new position of each particle


# Reflect  particles at boundary located at +/- d
def wallBounce(n, r, v, d):
    for i in range(n):
        if (v[i].x > 0 and r[i].x) > d:
            v[i].x = -abs(v[i].x)
        if (v[i].x < 0 and r[i].x) < - d:
            v[i].x = abs(v[i].x)
        if (v[i].y > 0 and r[i].y) > d:
            v[i].y = -abs(v[i].y)
        if (v[i].y < 0 and r[i].y) < - d:
            v[i].y = abs(v[i].y)


# Initialize the drawing
def initializeGraphs():
    global histgraph, vdist
    ## canvas(width=win, height=win, align='left')
    button(text="Stop", pos=scene.title_anchor, bind=run)
    button(text="Clear Histogram", pos=scene.title_anchor, bind=clearHistogram)

    box(size=vector(2 * L, 2 * L, 0))    # container for hard disks

    #________________  Create lists for N particles and their postion and velocity  ______________#
    # Particles are distributed randomely in a box (rho_0*L x rho_0*L x rho_0*L)
    # Particles have random initial velocity vectors in the range [-vo,v0]
    for i in range(N):
        particle = cylinder(pos=vector(random.uniform(-L + 2 * R, L - 2 * R),
                                       random.uniform(-L + 2 * R, L - 2 * R), 0), radius=R, axis=vector(0, 0, R / 5))
        particles.append(particle)
        r.append(particle.pos)          # particle position vector
        velocity = vector(random.uniform(-v0, v0), random.uniform(-v0, v0), 0)
        v.append(velocity)              # particle velocity vector
        a.append(vector(0, 0, 0))      # partcle acceleration vector

    # create and initialize histogram bins
    for i in range(nbins):
        histo.append(0.0)

    # create histogram graph
    histgraph = graph(width=2 * win, height=win, xmax=deltav * nbins,
                      ymax=N * deltav / 100, align='right')
    theory = gcurve(color=color.cyan)

    for vel in range(0, deltav * nbins + 10, 10):  # theoretical prediction
        # theory.plot(vel, (deltav / dv) * N * 4 * pi * ((mass / (2 * pi * k * T))**1.5)*exp(-0.5 * mass * (vel**2) / (k * T)) * (vel**2) * dv)
        b2 = 2 * k * T / mass
        theory.plot(vel, deltav * N * (2 * vel / b2) * exp(-vel * vel / b2))

    for i in range(nbins):
        accum.append([deltav * (i + .5), 0])
    vdist = gvbars(color=color.red, delta=deltav)


# Starts time evolution.  This function is called at end of file.
def evolve(running):
    global histo, nhisto, t
    while running:
        vpython.rate(100)
        histo = speedHistogram(v, histo)
        # Accumulate and average histogram snapshots
        for i in range(nbins):
            accum[i][1] = (nhisto * accum[i][1] + histo[i]) / (nhisto + 1)
        if nhisto % 10 == 0:
            vdist.data = accum
        nhisto += 1

        for i in range(N):  # zero acceleration vector before starting the sum
            a[i].x = 0
            a[i].y = 0

        #_________ particle - particle Collisions ____#
        for i in range(N):                           # i indicates one of the particles
            for j in range(i + 1, N, 1):
                dr = r[i] - r[j]      # distance between particle i and particle j
                r_hat = dr / mag(dr)
                if mag(dr) < 2 * R:
                    F = A * r_hat    # assume constant interaction in radial direction while colliding
                else:
                    F = vector(0, 0, 0)
                # Use Newton's 2nd and 3rd laws
                a[i] = a[i] + F / mass
                a[j] = a[j] - F / mass
        eulerAlgorithm(N, r, v, a)              # compute the  new position and velocity
        wallBounce(N, r, v, L - 2 * R)       # check to make sure partilces are within walls
        t += dt                                            # advance time
        for i in range(N):                           # move the screen objects to their new positions
            particles[i].pos = r[i]


# Simulation starts here.
initializeGraphs()
evolve(True)
