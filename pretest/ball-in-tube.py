
###############  SETUP STATEMENTS  ############
from vpython import *
scene=vpython.canvas()
scene.userzoom = False
###############  BALL IN TUBE EXAMPLE  ############
m = 2.0
f = 100.0
R = 0.5
L = 10.0
t = 0
dt = 0.001
v = vector(5.0,0,0)
tube = cylinder(pos = vector(-L/2,0,0), axis = vector(L,0,0), radius = R, opacity=0.5)
ball = sphere(pos=vector(-3.0,0,0), radius = R, color = color.red)
while (t<10):
    rate(100)
    if ball.pos.x > L/2-R: F1 = f*vector(-1,0,0)
    else: F1=vector(0,0,0)
    if ball.pos.x < -L/2+R: F2 = f*vector(1,0,0)
    else: F2=vector(0,0,0)
    F_net = F1 + F2
    a = F_net/m
    v = v + a*dt
    ball.pos = ball.pos + v*dt
    t = t + dt
