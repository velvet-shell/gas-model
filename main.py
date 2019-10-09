# Hard-sphere gas.

# Bruce Sherwood

from vpython import *
from math import *

win = 500 # размер картинки

Natoms = 20  # change this to have more or fewer atoms

# какие-то константы
L = 1  # container is a cube L on a side
gray = color.gray(0.7)  # color of edges of container
mass = 4E-3 / 6E23  # helium mass
Ratom = 0.06  # wildly exaggerated size of helium atom
k = 1.4E-23  # Boltzmann constant
T = 300  # around room temperature
dt = 1E-5

animation = canvas(width=win, height=win, align='left')
animation.range = L
animation.title = 'A "hard-sphere" gas'
s = """  Theoretical and averaged speed distributions (meters/sec).
  Initially all atoms have the same speed, but collisions
  change the speeds of the colliding atoms. One of the atoms is
  marked and leaves a trail so you can follow its path.

"""
animation.caption = s

d = L / 2 + Ratom       # половина высоты цилиндра
cylinder_radius = 0.005 # радиус цилиндра

# прорисовка цилиндра
ringtop = ring(pos=vector(0, d, 0), axis=vector(0, -d, 0), radius=d,
    thickness=0.005)
ringbottom = ring(pos=vector(0, -d, 0), axis=vector(0, -d, 0), radius=d,
    thickness=0.005)
vert1 = curve(color=gray, radius=cylinder_radius)
vert2 = curve(color=gray, radius=cylinder_radius)
vert3 = curve(color=gray, radius=cylinder_radius)
vert4 = curve(color=gray, radius=cylinder_radius)
vert1.append([vector(0, -d, -d), vector(0, d, -d)])
vert2.append([vector(0, -d, d), vector(0, d, d)])
vert3.append([vector(d, -d, 0), vector(d, d, 0)])
vert4.append([vector(-d, -d, 0), vector(-d, d, 0)])

Atoms = []  # сферы vpython
p = []      # импульсы атомов - векторы vpython
apos = []   # позиции атомов - векторы vpython
pavg = sqrt(3 * mass * k * T)  # average kinetic energy p**2/(2mass) = (3/2)kT

#равномерное распределение частиц
for i in range(Natoms):
    qq = 2 * pi * random()

    x = sqrt(random()) * L * cos(qq) / 2
    y = L * random() - L / 2
    z = sqrt(random()) * L * sin(qq) / 2

    if i == 0:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom,
            color=color.cyan, make_trail=True, retain=100,
            trail_radius=0.3 * Ratom))
        # первая частица, за которой идет след
    else:
        Atoms.append(sphere(pos=vector(x, y, z), radius=Ratom, color=gray))

    apos.append(vector(x, y, z))
    # все импульсы изначально одинаковы, возможно, надо поменять хз
    theta = pi * random()
    phi = 2 * pi * random()

    px = pavg * sin(theta) * cos(phi)
    py = pavg * sin(theta) * sin(phi)
    pz = pavg * cos(theta)

    p.append(vector(px, py, pz))

deltav = 100  # binning for v histogram

#построение гистограммы
def barx(v):
    return int(v / deltav)  # index into bars array


nhisto = int(4500 / deltav)
histo = []
for i in range(nhisto):
    histo.append(0.0)
histo[barx(pavg / mass)] = Natoms

gg = graph(width=win, height=0.4 * win, xmax=3000, align='left',
    xtitle='speed, m/s', ytitle='Number of atoms', ymax=Natoms * deltav / 1000)

theory = gcurve(color=color.cyan)
dv = 10
for v in range(0, 3001 + dv, dv):  # theoretical prediction
    theory.plot(v, (deltav / dv) * Natoms * 4 * pi * ((mass / (2 * pi * k * T)) ** 1.5) *
        exp(-0.5 * mass * (v ** 2) / (k * T)) * (v ** 2) * dv)

accum = []
for i in range(int(3000 / deltav)):
    accum.append([deltav * (i + .5), 0])
vdist = gvbars(color=color.red, delta=deltav)

def interchange(v1, v2):  # remove from v1 bar, add to v2 bar
    barx1 = barx(v1)
    barx2 = barx(v2)
    if barx1 == barx2:
        return
    if barx1 >= len(histo) or barx2 >= len(histo):
        return
    histo[barx1] -= 1
    histo[barx2] += 1

# проверка на сталкивающиеся шары
def checkCollisions():
    hitlist = []
    r2 = 2 * Ratom
    for i in range(Natoms):
        for j in range(i):
            dr = apos[i] - apos[j]
            if dr.mag < r2:
                hitlist.append([i, j])
    return hitlist

nhisto = 0  # number of histogram snapshots to average
# основной цикл
while True:
    rate(50)
    # Accumulate and average histogram snapshots
    for i in range(len(accum)):
        accum[i][1] = (nhisto * accum[i][1] + histo[i]) / (nhisto + 1)
    
    if nhisto % 10 == 0:
        vdist.data = accum
    nhisto += 1

    # Update all positions
    for i in range(Natoms):
        Atoms[i].pos = apos[i] = apos[i] + (p[i] / mass) * dt

    # Check for collisions
    hitlist = checkCollisions()

    # непонятный цикл для столкнувшихся частиц
    # If any collisions took place, update momenta of the two atoms
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
        dx = dot(rrel, vrel.hat)  # rrel.mag*cos(theta)
        dy = cross(rrel, vrel.hat).mag  # rrel.mag*sin(theta)
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
        interchange(vi.mag, p[i].mag / mass)
        interchange(vj.mag, p[j].mag / mass)

    # столкновение со стенками
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
        # (будет изменено в связи с поршнем)
        if abs(loc.y) > L / 2:
            if loc.y < 0:
                p[i].y = abs(p[i].y)
            else:
                p[i].y = -abs(p[i].y)
