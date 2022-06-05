import numpy as npy
import matplotlib.pyplot as mplt
from scipy.integrate import solve_ivp

# initial conditions and constants
m=0.16
D=1E-3
g=9.81
v0=120*(5/18)
x0=0
z0=1.8

eps=1E-6
tolerance=1E-6
delta=1E-4

def solve(phi):
    u0=x0,v0*npy.cos(phi),z0,v0*npy.sin(phi) # x0,v0_x,z0,v0_z
    t0,tf =0,100

    def fn(t,u):
        x,xdot,z,zdot=u
        speed=npy.hypot(xdot,zdot) # hypoteneus
        xdotdot=-D/m*speed*xdot
        zdotdot=-D/m*speed*zdot -g
        return xdot,xdotdot,zdot,zdotdot

    def hit_gnd(t,u): # ground hit if z=0
        return u[2]

    hit_gnd.terminal=True # stop when ground hit
    hit_gnd.direction=-1 # stop if moving down 
    # check scipy documentation for these
    s=solve_ivp(fn,(t0, tf),u0, dense_output=True,events=hit_gnd)
    t=npy.linspace(0,s.t_events[0][0],tf) # time data
    sol=s.sol(t)
    x=sol[0]
    return x[-1]

ang=[]
ran=[]
for angle in range(0,91):
    phi=npy.radians(angle)
    ang.append(angle)
    ran.append(solve(phi))
 
dat=[ang,ran]
mplt.grid(True)
mplt.axis([0,90,0,80])
mplt.title('Range as a function of throwing angle')
mplt.xlabel('angle (deg)')
mplt.ylabel('x (m)')
mplt.plot(dat[0],dat[1],'b')
mplt.show() 

def derivative(p):
    return round((solve(p+eps)-solve(p))/(eps),2)

def bisection(p0,p1): #Bisection Method Algorithom

    for i in range(500):
        mid=(p0+p1)/2
        a,b,c=derivative(p0),derivative(p1),derivative(mid)

        if abs(c)<=tolerance:
            N=i+1
            print('Maximum range:', solve(mid),'m')
            print('Corresponding throwing angle', npy.degrees(mid),'deg')
            break
        
        elif abs(min((mid-p0),(mid-p1)))<delta:
            N=i+1
            print('Maximum range:', solve(mid),'m')
            print('Corresponding throwing angle', npy.degrees(mid),'deg')
            break
        
        elif a*c>0:
            p0=mid
            
        elif a*c<0:
            p1=mid
    else:
        print('Sorry. Bisection failed.')

    return 0

bisection(npy.radians(0.0),npy.radians(90.0))
