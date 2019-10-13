#coding=utf-8

from __future__ import division
from visual import *
from visual.graph import *
from math import *
import wx

win_height = 900
win_width = 1600

w = window(width = win_width + 2 * window.dwidth,
            height = win_height + window.dheight,
            title = 'Physics demonstration',
            style = wx.CAPTION | wx.CLOSE_BOX)

offset = 20
disp = display(window = w, x = offset, y = offset, forward = vector(0,-0.3,-1),
            range=1.5,
            width = w.width / 3 - 2 * offset, height = w.height - 2 * offset)


Natoms = 60 # change this to have more or fewer atoms
mass = 4E-3 / 6E23 # helium mass
Ratom = 0.06 # wildly exaggerated size of helium atom
k = 1.4E-23 # Boltzmann constant
R = 8.3
T = 300 # around room temperature
dt = 1E-5


time = 0  # время, чтобы считать скорость поршня
def speed(time):
    if ((time % 100) < 50):
        return sqrt(3 * mass * k * T) / (5 * mass)
    else:
        return - sqrt(3 * mass * k * T) / (5 * mass)


L = 1 # container is a cube L on a side
gray = color.gray(0.7) # color of edges of container
d = L / 2 + Ratom # half of cylinder's height
topborder = d

cylindertop = cylinder(pos = (0, d, 0), axis = (0, -d / 50, 0), radius = d)
ringtop = ring(pos = (0, d, 0), axis = (0, -d, 0), radius = d,
            thickness = 0.005)
ringbottom = ring(pos = (0, -d, 0), axis = (0, -d, 0), radius = d,
            thickness = 0.005)
body = cylinder(pos = (0, -d, 0), axis = (0, 2*d, 0), radius = d,
            opacity = 0.2)


Atoms = []  # spheres
p = []      # momentums (vectors)
apos = []   # positions (vectors)
pavg = sqrt(3 * mass * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

# uniform particle distribution
for i in range(Natoms):
    qq = 2 * pi * random.random()

    x = sqrt(random.random()) * L * cos(qq) / 2
    y = L * random.random() - L / 2
    z = sqrt(random.random()) * L * sin(qq) / 2

    if i == 0:
        # particle with a trace
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom,
            color=color.cyan, make_trail=True, retain=100,
            trail_radius=0.3 * Ratom))
    else:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=gray))

    apos.append(vector(x, y, z))
    

    theta = pi * random.random()
    phi = 2 * pi * random.random()

    px = pavg * sin(theta) * cos(phi)
    py = pavg * sin(theta) * sin(phi)
    pz = pavg * cos(theta)

    p.append(vector(px, py, pz))


#temperature graph
g1 = gdisplay(window = w, x = w.width / 3, y = offset,
            width = w.width / 3, height = w.height / 2)

graph_temp = gcurve(gdisplay = g1, color=color.cyan)


deltav = 100 # histogram bar width

g2 = gdisplay(window = w, x = w.width / 3, y = 2 * offset + w.height / 2,
            width = w.width / 3, height = w.height / 2, 
            xmax = 3000, ymax = Natoms * deltav / 1000)


# theoretical prediction
theory_speed = gcurve(gdisplay=g2, color=color.cyan)

dv = 10
for v in range(0, 3001 + dv, dv):  
    theory_speed.plot(pos=(v, (deltav / dv) * Natoms *
                4 * pi * ((mass / (2 * pi * k * T)) ** 1.5) *
                exp(-0.5 * mass * (v ** 2) / (k * T)) * (v ** 2) * dv))

# histogram
hist_speed = ghistogram(gdisplay = g2, bins = arange(0, 3000, 100),
            color = color.red, accumulate = True, average = True)


speed_data = [] # histogram data
for i in range(Natoms):
    speed_data.append(mag(p[i]) / mass)


def checkCollisions():
    hitlist = []
    r2 = 2 * Ratom
    for i in range(Natoms):
        for j in range(i):
            dr = apos[i] - apos[j]
            if dr.mag < r2:
                hitlist.append([i, j])
    return hitlist

while True:
    rate(60)
    
    sp = speed(time)
    cylindertop.pos.y -= sp * dt
    time += 1
    

    for i in range(Natoms):
        Atoms[i].pos = apos[i] = apos[i] + (p[i] / mass) * dt
        speed_data[i] = mag(p[i]) / mass

    hist_speed.plot(data = speed_data)

    total_momentum = 0
    for i in range(Natoms):
        total_momentum += mag2(p[i])
    
    graph_temp.plot(pos = (time, total_momentum / (3 * k * mass) / Natoms))


    hitlist = checkCollisions()

    for ij in hitlist:
        
        i = ij[0]
        j = ij[1]
        ptot = p[i] + p[j]
        posi = apos[i]
        posj = apos[j]
        vi = p[i] / mass
        vj = p[j] / mass
        vrel = vj - vi
        a = vrel.mag2
        if a == 0: # exactly same velocities
            continue
        rrel = posi - posj
        if rrel.mag > Ratom: # one atom went all the way through another
            continue

        # theta is the angle between vrel and rrel:
        dx = dot(rrel, norm(vrel))  # rrel.mag*cos(theta)
        dy = cross(rrel, norm(vrel)).mag  # rrel.mag*sin(theta)
        # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atome j hits atom i:
        alpha = asin(dy / (2 * Ratom))
        d = (2 * Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
        deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

        posi = posi - vi * deltat  # back up to contact configuration
        posj = posj - vj * deltat
        mtot = 2 * mass
        pcmi = p[i] - ptot * mass / mtot  # transform momenta to cm frame
        pcmj = p[j] - ptot * mass / mtot
        rrel = norm(rrel)
        pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel  # bounce in cm frame
        pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
        p[i] = pcmi + ptot * mass / mtot  # transform momenta back to lab frame
        p[j] = pcmj + ptot * mass / mtot
        apos[i] = posi + (p[i] / mass) * deltat  # move forward deltat in time
        apos[j] = posj + (p[j] / mass) * deltat

    # collisions with walls
    for i in range(Natoms):
        # проекция радиус-вектора на плоскость
        loc = vector(apos[i])
        loc.y = 0

        # вылет за боковую стенку (цилиндр радиуса L / 2 + Ratom)
        if (mag(loc) > L / 2):

            # проекция импульса на плоскость
            proj_p = vector(p[i])
            proj_p.y = 0

            loc = norm(loc)
            # скалярное произведение нормированного радиус-вектора на импульс (все в проекции на плоскость)
            dotlp = dot(loc, proj_p) 

            if dotlp > 0:
                p[i] -= 2 * dotlp * loc
            # dotlp < 0 - атом улетает от стенки
            # dotlp = 0 - атом летит вдоль стенки
        
        loc = apos[i]
        # вылет за торцы
        if loc.y < - L / 2:
            p[i].y = abs(p[i].y)

        if loc.y > cylindertop.pos.y - Ratom:
            v_otn = p[i].y / mass + sp
            if v_otn > 0:
                p[i].y = (- v_otn - sp) * mass
