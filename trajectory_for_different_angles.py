import numpy as npy
import matplotlib.pyplot as mplt
from scipy.integrate import solve_ivp

# initial conditions and constants
m=0.16
D=1E-3
g=9.81
x0=0
z0=1.8
v0=120*(5/18)
angle=[0,15,30,45,60,75,90]
phi=npy.radians(angle)
t0,tf =0,100

def fn(t,u):
    x,dx,z,dz=u
    v=npy.hypot(dx,dz) # hypoteneus
    d2x=-D/m*v*dx
    d2z=-D/m*v*dz -g
    return dx,d2x,dz,d2z

def hit_gnd(t,u): # ground hit if z=0
    return u[2]

hit_gnd.terminal=True # stop when ground hit
hit_gnd.direction=-1 # stop if moving down
# for more info, check scipy documentation

for i in range(7):
    u0=x0,v0*npy.cos(phi[i]),z0,v0*npy.sin(phi[i]) # x0,v0_x,z0,v0_z
    s=solve_ivp(fn,(t0, tf),u0, dense_output=True,events=hit_gnd)
    #print(soln)

    t=npy.linspace(0,s.t_events[0][0],tf) # time data

    # output and range plot
    sol=s.sol(t)
    x,z=sol[0],sol[2]
    mplt.plot(x,z,lw=3,label=angle[i])

mplt.grid(True)
mplt.axis([0,80,0,45])
mplt.legend()
mplt.title('Projectile Trajectory for different projection angle')
mplt.xlabel('x (m)')
mplt.ylabel('z (m)')
mplt.show() 
 
