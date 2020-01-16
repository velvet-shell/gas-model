#coding=utf-8
start = 0
pause = 0

ampl = 3
period = 150
piston_mode = 0
model = 0

Natoms = 10 # change this to have more or fewer atoms
mass = 4E-3 / 6E23 # helium mass
Ratom = 0.01 # wildly exaggerated size of helium atom
T = 300 # around room temperature

Atoms = []

menu_switch = 0

button_size = (270, 50)
slider_size = (270, 50)

menu_button_size = (350, 80)

w = None