from vpython import *
scene = vpython.canvas()
scene.userzoom = False
m1 = 1.0
m2 = 1.0
R = 0.5
L = 10.0
A = 40
t = 0
dt = 0.001
table = box(pos=vector(0,0,0), size=vector(L,L,0))
ball1 = sphere(pos=vector(-2.0,-2,0), radius=R, color=color.red)
ball2 = sphere(pos=vector(2.0,-2,0), radius=R, color=color.blue)
v1 = vector(3.0,3.0,0)
v2 = vector(-3.0,3.0,0)
while(t < 4):
    rate(100)
    r = ball1.pos - ball2.pos
    r_hat = r/mag(r)
    if mag(r) < 2*R: F_net = A*r_hat
    else: F_net=vector(0,0,0)
    a1 = F_net/m1
    v1 = v1 + a1*dt
    ball1.pos = ball1.pos + v1*dt
    a2 = F_net/m2
    v2 = v2 + a2*dt
    ball2.pos = ball2.pos + v2*dt
    t = t + dt
