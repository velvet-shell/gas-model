#coding=utf-8
from __future__ import unicode_literals, print_function, division
from visual import window, cylinder, ring, random, sphere, mag, sleep, rate, mag2, dot, norm, cross, exit, box
from visual.graph import display, vector, color, gdisplay, gcurve, ghistogram, arange
from math import sqrt, pi, cos, sin, exp, asin
import wx
import os

import config

config.w = window(title = 'Модель динамики газа в поршне',
            style = wx.CAPTION | wx.CLOSE_BOX)
config.w.win.ShowFullScreen(True)

width, height = config.w.win.GetSize()
config.w.width = width
config.w.height = height


def MenuInterface():
    """Create main menu interface"""
    
    def ModelButton(evt):
        """Go to simulation window"""
        config.menu_switch = 1

    def AuthorsButton(evt):
        """Go to authors window"""
        config.menu_switch = 2

    def TheoryButton(evt):
        """Go to theory window"""
        os.startfile("Theory.pdf")
        #config.menu_switch = 3

    def ExitButton(evt):
        """Exit program complerely"""
        exit()
    
    # Clear old widgets and scale font
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    width, height = config.w.win.GetSize()
    p.SetFont(config.w.win.GetFont().Scaled(0.0028 * height))

    config.menu_button_size = (width * 0.182, height * 0.074)
    offset = 10
    # Create new widgets and bind them
    model_button = wx.Button(p, label = 'Модель', size = config.menu_button_size)
    theory_button = wx.Button(p, label ='Теория', size = config.menu_button_size)
    authors_button = wx.Button(p, label = 'Авторы', size = config.menu_button_size)
    exit_button = wx.Button(p, label = 'Выход', size = config.menu_button_size)

    cmc_bmp = wx.Bitmap('cmc.bmp')
    cmc = wx.StaticBitmap(p, -1, cmc_bmp)
    cmc.SetPosition((offset, offset))

    phys_bmp = wx.Bitmap('phys.bmp')
    phys = wx.StaticBitmap(p, -1, phys_bmp)
    phys.SetPosition((width - phys_bmp.GetWidth() - offset, offset))

    year = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL, label='2019')

    main_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'МГУ им. М.В. Ломоносова\n Компьютерные демонстрации по курсу лекций\n Статистическая физика')
    main_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())         

    p.SetFont(p.GetFont().MakeBold())

    sub_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'Разогрев газа в результате периодического движения поршня')
    sub_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())

    model_button.Bind(wx.EVT_BUTTON, ModelButton)
    theory_button.Bind(wx.EVT_BUTTON, TheoryButton)
    authors_button.Bind(wx.EVT_BUTTON, AuthorsButton)
    exit_button.Bind(wx.EVT_BUTTON, ExitButton)

    # Add all widgets to sizer to properly place them in a window
    padding = height + config.w.dheight - main_title.GetSize()[1] - sub_title.GetSize()[1] -\
                4 * config.menu_button_size[1] - year.GetSize()[1] - 5 * offset

    control_box = wx.BoxSizer(wx.VERTICAL)

    #interface layout
    control_box.Add((-1, offset))

    control_box.Add(main_title, flag = wx.ALIGN_CENTER)
    control_box.Add(sub_title, flag = wx.ALIGN_CENTER)

    control_box.Add((-1, padding / 2))

    control_box.Add(model_button, flag = wx.ALIGN_CENTER)
    control_box.Add(theory_button, flag = wx.ALIGN_CENTER)
    control_box.Add(authors_button, flag = wx.ALIGN_CENTER)
    control_box.Add(exit_button, flag = wx.ALIGN_CENTER)

    control_box.Add((-1, padding / 2))

    control_box.Add(year, flag = wx.ALIGN_CENTER)

    p.SetSizer(control_box)
    p.Layout()

def AuthorsInterface():
    def BackToMenu(evt):
        """Switch back to the main menu"""
        config.menu_switch = 0
    
    # Clear old widgets and scale font
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    width, height = config.w.win.GetSize()
    p.SetFont(config.w.win.GetFont().Scaled(0.0028 * height))
    offset = 10

    andrew = wx.Image('Andrew.jpg')
    andrew.Rescale(0.22 * height, 0.22 * width)
    andrew_bmp = wx.BitmapFromImage(andrew)
    andrew = wx.StaticBitmap(p, -1, andrew_bmp)
    andrew.SetPosition((width / 4 - andrew_bmp.GetWidth() / 2, height / 3))
    andrew_text = wx.StaticText(p, pos = (width / 4 - andrew_bmp.GetWidth() / 2, height / 3 + andrew_bmp.GetHeight()), 
                style = wx.ALIGN_CENTRE_HORIZONTAL, label = 'Антипов Андрей')

    roma = wx.Image('roma.jpg')
    roma.Rescale(0.16 * width, 0.41 * height)
    roma_bmp = wx.BitmapFromImage(roma)
    roma = wx.StaticBitmap(p, -1, roma_bmp)
    roma.SetPosition((width / 2 - roma_bmp.GetWidth() / 2, height / 3))
    roma_text = wx.StaticText(p, pos = (width / 2 - roma_bmp.GetWidth() / 2, height / 3 + roma_bmp.GetHeight()), 
                style = wx.ALIGN_CENTRE_HORIZONTAL, label = 'Шаповалов Роман')

    vlados = wx.Image('Vladosik.jpg')
    vlados.Rescale(0.13 * width, 0.4 * height)
    vlados_bmp = wx.BitmapFromImage(vlados)
    vlados = wx.StaticBitmap(p, -1, vlados_bmp)
    vlados.SetPosition((3 * width / 4 - vlados_bmp.GetWidth() / 2, height / 3))
    vlados_text = wx.StaticText(p, pos = (3 * width / 4 - vlados_bmp.GetWidth() / 2, height / 3 + vlados_bmp.GetHeight()), 
                style = wx.ALIGN_CENTRE_HORIZONTAL, label = 'Черкасов Владислав')

    cmc_bmp = wx.Bitmap('cmc.bmp')
    cmc = wx.StaticBitmap(p, -1, cmc_bmp)
    cmc.SetPosition((offset, offset))

    phys_bmp = wx.Bitmap('phys.bmp')
    phys = wx.StaticBitmap(p, -1, phys_bmp)
    phys.SetPosition((width - phys_bmp.GetWidth() - offset, offset))

    main_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'МГУ им. М.В. Ломоносова\n Компьютерные демонстрации по курсу лекций\n Статистическая физика')
    main_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())   

    authors_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL, label = 'Авторы:')
    teacher_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL, label = 'Научный руководитель:\n Чичигина Ольга Александровна')

    back_button = wx.Button(p, pos=(width - config.menu_button_size[0] - offset, height - config.menu_button_size[1] - offset),
                label = 'Назад', size = config.menu_button_size)
    back_button.Bind(wx.EVT_BUTTON, BackToMenu)

    p.SetFont(p.GetFont().MakeBold())

    sub_title = wx.StaticText(p, style = wx.ALIGN_CENTRE_HORIZONTAL,
                label = 'Разогрев газа в результате периодического движения поршня')
    sub_title.Wrap(width - phys_bmp.GetWidth() - cmc_bmp.GetWidth())


    control_box = wx.BoxSizer(wx.VERTICAL)
    control_box.Add((-1, offset))

    control_box.Add(main_title, flag = wx.ALIGN_CENTER)
    control_box.Add(sub_title, flag = wx.ALIGN_CENTER)

    control_box.Add((-1, height / 3 - main_title.GetSize()[1] - sub_title.GetSize()[1] - authors_title.GetSize()[1] - 2 * offset))

    control_box.Add(authors_title, flag = wx.ALIGN_CENTER)
    
    control_box.Add((-1, 2 * height / 3 - teacher_title.GetSize()[1] - 2 * offset))

    control_box.Add(teacher_title, flag = wx.ALIGN_CENTER)

    p.SetSizer(control_box)
    p.Layout()

def TheoryInterface():
    def BackToMenu(evt):
        """Switch back to the main menu"""
        config.menu_switch = 0
    
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    width, height = config.w.win.GetSize()
    p.SetFont(config.w.win.GetFont().Scaled(0.0028 * height))
    offset = 10
    
    theo = wx.Image('теория1.png')
    theo.Rescale(0.6 * height, 0.52 * width)
    theo_bmp = wx.BitmapFromImage(theo)
    theo = wx.StaticBitmap(p, -1, theo_bmp)
    theo.SetPosition((0, 0))

    back_button = wx.Button(p, pos=(width - config.menu_button_size[0] - offset, height - config.menu_button_size[1] - offset),
                label = 'Назад', size = config.menu_button_size)
    back_button.Bind(wx.EVT_BUTTON, BackToMenu)

def ModelInterface():
    """Create interface for model showcase"""

    # Declare functions to bind with widgets later
    def SetMode(evt):
        config.model = model_choice.GetSelection()
        if config.model == 1:
            control_box.ShowItems(show = True)
            piston_mode_choice.SetItems(['Гармоническое', 'Равномерное', 'Интенсивное сжатие', 'Интенсивное расшир.'])
            piston_mode_choice.SetSelection(0)
            config.piston_mode = 0
        else:
            piston_mode_choice.SetItems(['Нет', 'Гармоническое', 'Равномерное', 'Интенсивное сжатие', 'Интенсивное расшир.'])
            piston_mode_choice.SetSelection(0)

            control_box.ShowItems(show = True)
            piston_box.ShowItems(show = False)
            config.piston_mode = 0


    def SetPiston(evt):
        config.piston_mode = piston_mode_choice.GetSelection()
        if config.model == 0:
            if config.piston_mode >= 1:
                if config.model == 0:
                    ratom_temp_box.ShowItems(show = False)
                piston_box.ShowItems(show = True)
                if config.model == 0:
                    config.Ratom = 0.01
                    config.T = 300
                ratom_slider.SetMax(1)
                temp_slider.SetMax(300)
            else:
                piston_box.ShowItems(show = False)
                ratom_temp_box.ShowItems(show = True)
                ratom_slider.SetMax(6)
                temp_slider.SetMax(1000)


    def SetAmp(evt):
        """Set default amplitude of a piston"""
        #todo
        config.ampl = amp_slider.GetValue()

    def SetPeriod(evt):
        """Set default period of a piston"""
        config.period = 10 * per_slider.GetValue()
        
    def SetNum(evt):
        """Set default number of atoms"""
        config.Natoms = number_spinctrl.GetValue()

    def SetAtomRadius(evt):
        """Set default radius of an atom"""
        config.Ratom = ratom_slider.GetValue() / 100

    def SetTemp(evt):
        """Set default temperature"""
        config.T = temp_slider.GetValue()

    def PressStart(evt):
        """Start and stop the simulation"""
        if config.start == 0:
            config.start = 1
        elif config.pause == 0:
            config.pause = 1
        else:
            config.pause = 0

    def ClearButton(evt):
        """Clear screen to completely restart simulation"""
        config.pause = 0
        config.start = 0

    def BackToMenu(evt):
        """Switch back to the main menu"""
        config.pause = 0
        config.start = 0
        config.menu_switch = 0
        config.model = 0
    
    def ExitButton(evt):
        """Exit program completely"""
        exit()

    # Clear old widgets and scale font
    config.w.win.DestroyChildren()
    p = config.w.panel = wx.Panel(config.w.win, size = config.w.win.GetSize())
    width, height = config.w.win.GetSize()
    p.SetFont(config.w.win.GetFont().Scaled(0.0019 * height))

    config.button_size = (width * 0.14, height * 0.046)
    config.slider_size = (width * 0.14, height * 0.046)

    # Create new widgets and bind them
    model_text = wx.StaticText(p, label = 'Режим моделирования:')
    piston_mode_text = wx.StaticText(p, label = 'Движение поршня:')
    per_text = wx.StaticText(p, label = 'Период:')
    amp_text = wx.StaticText(p, label = 'Амплитуда:')
    number_text = wx.StaticText(p, label = 'Число частиц:')
    ratom_text = wx.StaticText(p, label = 'Размер частицы:')
    temp_text = wx.StaticText(p, label = 'Начальная температура:')

    model_choice = wx.Choice(p, choices = ['Наблюдение', 'Статистика'], size = config.button_size)
    model_choice.SetSelection(0)

    piston_mode_choice = wx.Choice(p, choices = ['Нет', 'Гармоническое', 'Равномерное', 'Интенсивное сжатие', 'Интенсивное расшир.'], size = config.button_size)
    piston_mode_choice.SetSelection(0)

    number_spinctrl = wx.SpinCtrl(p, size = config.button_size,
                min = 1, max = 30, initial = 10)

    per_slider = wx.Slider(p, size = config.slider_size,
                minValue = 15, maxValue = 20)
    amp_slider = wx.Slider(p, size = config.slider_size,
                minValue = 5, maxValue = 20)
    ratom_slider = wx.Slider(p, size = config.slider_size,
                minValue = 1, maxValue = 6)
    temp_slider = wx.Slider(p, size = config.slider_size,
                minValue = 300, maxValue = 1000)

    per_slider.SetValue(15)
    amp_slider.SetValue(5)
    ratom_slider.SetValue(1)
    temp_slider.SetValue(300)

    start_button = wx.Button(p, label = 'Старт / Пауза', size = config.button_size)
    back_button = wx.Button(p, label = 'Меню', size = config.button_size)
    exit_button = wx.Button(p, label = 'Выход', size = config.button_size)
    clear_button = wx.Button(p, label = 'Сброс', size = config.button_size)

    model_choice.Bind(wx.EVT_CHOICE, SetMode)
    piston_mode_choice.Bind(wx.EVT_CHOICE, SetPiston)
    per_slider.Bind(wx.EVT_SCROLL, SetPeriod)
    amp_slider.Bind(wx.EVT_SCROLL, SetAmp)
    ratom_slider.Bind(wx.EVT_SCROLL, SetAtomRadius)
    temp_slider.Bind(wx.EVT_SCROLL, SetTemp)
    number_spinctrl.Bind(wx.EVT_SPINCTRL, SetNum)
    start_button.Bind(wx.EVT_BUTTON, PressStart)
    clear_button.Bind(wx.EVT_BUTTON, ClearButton)
    exit_button.Bind(wx.EVT_BUTTON, ExitButton)
    back_button.Bind(wx.EVT_BUTTON, BackToMenu)

    # Add all widgets to sizer to properly place them in a window
    h_offset = (width / 3 - 100 - config.button_size[0]) / 2
    v_offset = config.w.dheight
    main_box = wx.BoxSizer(wx.VERTICAL)
    control_box = wx.BoxSizer(wx.VERTICAL)
    ratom_temp_box = wx.BoxSizer(wx.VERTICAL)
    piston_box = wx.BoxSizer(wx.VERTICAL)
    choice_box = wx.BoxSizer(wx.VERTICAL)

    main_box.Add((-1, v_offset))
    main_box.Add(model_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    main_box.Add(model_choice, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    choice_box.Add(piston_mode_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    choice_box.Add(piston_mode_choice, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(choice_box, flag = wx.ALIGN_RIGHT | wx.RIGHT)

    piston_box.Add(per_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    piston_box.Add(per_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    piston_box.Add(amp_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    piston_box.Add(amp_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(piston_box, flag = wx.ALIGN_RIGHT | wx.RIGHT)

    control_box.Add(number_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    control_box.Add(number_spinctrl, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    ratom_temp_box.Add(ratom_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    ratom_temp_box.Add(ratom_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    ratom_temp_box.Add(temp_text, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    ratom_temp_box.Add(temp_slider, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    control_box.Add(ratom_temp_box, flag = wx.ALIGN_RIGHT | wx.RIGHT)

    main_box.Add(control_box, flag = wx.ALIGN_RIGHT | wx.RIGHT)

    main_box.Add(start_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    main_box.Add(clear_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    padding = height - 7 * temp_text.GetSize()[1] -\
        4 * temp_slider.GetSize()[1] - number_spinctrl.GetSize()[1] -\
        2 * piston_mode_choice.GetSize()[1] - 4 * start_button.GetSize()[1] - 2 * v_offset
    
    main_box.Add((-1, padding))

    main_box.Add(back_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)
    main_box.Add(exit_button, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = h_offset)

    p.SetSizer(main_box)
    p.Layout()
    piston_box.ShowItems(show = False)

    
def Simulation():

    config.Atoms = []  # spheres
    p = []      # momentums (vectors)
    apos = []   # positions (vectors)
    ampl = 0 #амплитуда движения
    period = 5
    k = 1.4E-23 # Boltzmann constant
    R = 8.3
    dt = 1E-5
    time = 0
    
    def checkCollisions(Natoms, Ratom):
        hitlist = []
        r2 = 2 * Ratom
        for i in range(Natoms):
            for j in range(i):
                dr = apos[i] - apos[j]
                if dr.mag < r2:
                    hitlist.append([i, j])
        return hitlist
    
    def speed(time, piston_mode, period, ampl, temp):
        if (piston_mode == 0):
            return 0
        if (piston_mode == 1):
            return ampl / 10 * 3 * sin(time / period * 2 * pi) * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
        if (piston_mode == 2):
            if (time % period < period // 2):
                return 1.5 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
            else:
                return -1.5 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
        if (piston_mode == 3):
            if (time % period < period // 5):
                return 5 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
            else:
                return -5 / 4 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
        if (piston_mode == 4):
            if (time % period < 4* period // 5):
                return 5 / 4 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
            else:
                return -5 * ampl / 10 * sqrt(3 * config.mass * k * temp) / (5 * config.mass) / period * 100
            
    width, height = config.w.win.GetSize()
    
    offset = config.w.dheight
    deltav = 100 # histogram bar width
    
    disp = display(window = config.w, x = offset, y = offset, forward = vector(0,-0.05, -1),
                range = 1, # userspin = False,
                width = width / 3, height = height)

    g1 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = 2 * offset,
                background = color.white,
                xtitle = 't', ytitle = 'v',
                foreground = color.black,
                width = width / 3, height = height / 2 - 2 * offset)
    
    g2 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = height / 2 + offset,
                background = color.white,
                foreground = color.black,
                width = width / 3, height = height / 2 - 2 * offset)

    # adding empty dots to draw axis
    graph_average_speed = gcurve(gdisplay = g1, color=color.white)
    graph_average_speed.plot(pos = (3000, 1500))
    graph_temp = gcurve(gdisplay = g2, color=color.white)
    graph_temp.plot(pos = (3000, config.Natoms * deltav / 1000))
    
    speed_text = wx.StaticText(config.w.panel, pos = (width / 3 + 2 * offset, offset), label = "Средняя скорость")
    graph_text = wx.StaticText(config.w.panel, pos = (width / 3 + 2 * offset, height / 2), label = "")

    L = 1 # container is a cube L on a side
    d = L / 2 + config.Ratom # half of cylinder's height
    topborder = d
    gray = color.gray(0.7) # color of edges of container

    # cylinder drawing
    cylindertop = cylinder(pos = (0, d - 0.001, 0), axis = (0, 0.005, 0), radius = d)
    ringtop = ring(pos = (0, d, 0), axis = (0, -d, 0), radius = d,
                thickness = 0.005)
    ringbottom = ring(pos = (0, -d, 0), axis = (0, -d, 0), radius = d,
                thickness = 0.005)
    body = cylinder(pos = (0, -d, 0), axis = (0, 2 * d, 0), radius = d,
                opacity = 0.2)
    
    # body_tmp = cylinder(pos = (0, d, 0), axis = (0, 2 * d, 0), radius = d + 0.1, color = (0, 0, 0))
    # ceil = box(pos = (0, d, 0), length = 5, height = 0.005, width = 5, color = (0, 0, 0))
    # floor = box(pos = (0, -d, 0), length = 100, height = 0.005, width = 100, color = (0, 0, 0))
    # left = box(pos = (d + 0.005, 0, 0), axis = (0, 1, 0), length = 100, height = 0.005, width = 100, color = (0, 0, 0))
    # right = box(pos = (-d - 0.005, 0, 0), axis = (0, 1, 0), length = 100, height = 0.005, width = 100, color = (0, 0, 0))


    # uniform particle distribution
    for i in range(config.Natoms):
        qq = 2 * pi * random.random()

        x = sqrt(random.random()) * L * cos(qq) / 2
        y = L * random.random() - L / 2
        z = sqrt(random.random()) * L * sin(qq) / 2

        if i == 0:
            # particle with a trace
            config.Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                        color = color.cyan, make_trail = False, retain = 100,
                        trail_radius = 0.3 * config.Ratom))
        else:
            config.Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                        color = gray))

        apos.append(vector(x, y, z))


    # waiting to start, adjusting everything according to changing variables
    """WAITING TO START"""
    last_Natoms = config.Natoms
    last_Ratom = config.Ratom
    while config.start == 0:
        if config.menu_switch == 0:
            disp.delete()
            g1.display.delete()
            g2.display.delete()

            graph_text.Destroy()
            speed_text.Destroy()
            return
        
        if config.Natoms > last_Natoms:
            for i in range(config.Natoms - last_Natoms):
                qq = 2 * pi * random.random()
                x = sqrt(random.random()) * L * cos(qq) / 2
                y = L * random.random() - L / 2
                z = sqrt(random.random()) * L * sin(qq) / 2
    
                if last_Natoms == 0:
                    # particle with a trace
                    config.Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                                color = color.cyan, make_trail = False, retain = 100,
                                trail_radius = 0.3 * config.Ratom))
                else:
                    config.Atoms.append(sphere(pos = vector(x, y, z), radius = config.Ratom,
                                color = gray))
                apos.append(vector(x, y, z))
            last_Natoms = config.Natoms
            
        elif config.Natoms < last_Natoms:
            for i in range(last_Natoms - config.Natoms):
                config.Atoms.pop().visible = False
                apos.pop()
            last_Natoms = config.Natoms

        if last_Ratom != config.Ratom:
            for i in range(last_Natoms):
                config.Atoms[i].radius = config.Ratom
            last_Ratom = config.Ratom
        
        if config.model == 0:
            if config.piston_mode >= 1:
                graph_text.SetLabel("Температура")
            else:
                graph_text.SetLabel("Распределение скоростей частиц")            
        sleep(0.1)

    # freezed all variables, ready to start
    last_T = config.T
    last_ampl = config.ampl
    last_period = config.period
    last_piston_mode = config.piston_mode
    last_model = config.model

    pavg = sqrt(3 * config.mass * k * last_T)  # average kinetic energy p**2/(2config.mass) = (3/2)kT

    for i in range(last_Natoms):
        theta = pi * random.random()
        phi = 2 * pi * random.random()

        px = pavg * sin(theta) * cos(phi)
        py = pavg * sin(theta) * sin(phi)
        pz = pavg * cos(theta)

        p.append(vector(px, py, pz))

    if last_model == 1:
        disp.delete()
        unavail = wx.StaticText(config.w.panel, style = wx.ALIGN_CENTRE_HORIZONTAL,
                    label = "Отображение модели недоступно в режиме статистики",
                    pos = (offset, height / 2 - offset))
        unavail.Wrap(width / 3)
        last_period = last_period / 10
        last_piston_mode += 1
        graph_text.SetLabel("Температура")

    """ DRAW GRAPHS """

    g1.display.delete()
    g2.display.delete()

    if last_piston_mode == 0:
        g1 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = 2 * offset,
                background = color.white,
                xtitle = 't', ytitle = 'v',
                foreground = color.black,
                width = width / 3, height = height / 2 - 2 * offset,
                ymin = 0.7 * pavg / config.mass, ymax = 1.3 * pavg / config.mass)
        
        g2 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = height / 2 + offset,
                    background = color.white,
                    foreground = color.black,
                    xtitle = 'v', ytitle = 'Frequency',
                    width = width / 3, height = height / 2 - 2 * offset,
                    xmax = 3000 / 300 * last_T, ymax = last_Natoms * deltav / 1000)
        
    else:
        g1 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = 2 * offset,
                background = color.white,
                xtitle = 't', ytitle = 'v',
                foreground = color.black,
                width = width / 3, height = height / 2 - 2 * offset)
        
        g2 = gdisplay(window = config.w, x = width / 3 + 2 * offset, y = height / 2 + offset,
                    background = color.white,
                    xtitle = 't', ytitle = 'T',
                    foreground = color.black,
                    width = width / 3, height = height / 2 - 2 * offset)
        
    graph_average_speed = gcurve(gdisplay = g1, color=color.black)

    if last_piston_mode:
        graph_temp = gcurve(gdisplay = g2, color=color.black)
    else:
        theory_speed = gcurve(gdisplay = g2, color = color.black)
        dv = 10
        for v in range(0, int(3000 / 300 * last_T), dv):
            theory_speed.plot(pos=(v, (deltav / dv) * last_Natoms *
                        4 * pi * ((config.mass / (2 * pi * k * last_T)) ** 1.5) *
                        exp(-0.5 * config.mass * (v ** 2) / (k * last_T)) * (v ** 2) * dv))

        hist_speed = ghistogram(gdisplay = g2, bins = arange(0, int(3000 / 300 * last_T), 100),
                    color = color.red, accumulate = True, average = True)

        speed_data = [] # histogram data
        for i in range(last_Natoms):
            speed_data.append(pavg / config.mass)
            # speed_data.append(0)

    
    """ MAIN CYCLE """
    while config.start:

        while config.pause:
            sleep(0.1)
        
        rate(100)
        
        sp = speed(time, last_piston_mode, last_period, last_ampl, 300)
        cylindertop.pos.y -= sp * dt
        time += 1

        for i in range(last_Natoms):
            config.Atoms[i].pos = apos[i] = apos[i] + (p[i] / config.mass) * dt

            if last_piston_mode == 0:
                speed_data[i] = mag(p[i]) / config.mass


        total_momentum = 0
        v_sum = 0
        for i in range(last_Natoms):
            total_momentum += mag2(p[i])
            v_sum += sqrt(mag2(p[i])) / config.mass

        graph_average_speed.plot(pos = (time, v_sum / last_Natoms))
        
        if last_piston_mode:
            graph_temp.plot(pos = (time, total_momentum / (3 * k * config.mass) / last_Natoms))
        else:
            hist_speed.plot(data = speed_data)

        hitlist = checkCollisions(last_Natoms, last_Ratom)

        for ij in hitlist:
            
            i = ij[0]
            j = ij[1]
            ptot = p[i] + p[j]
            posi = apos[i]
            posj = apos[j]
            vi = p[i] / config.mass
            vj = p[j] / config.mass
            vrel = vj - vi
            a = vrel.mag2
            if a == 0: # exactly same velocities
                continue
            rrel = posi - posj
            if rrel.mag > config.Ratom: # one atom went all the way through another
                continue

            # theta is the angle between vrel and rrel:
            dx = dot(rrel, norm(vrel))  # rrel.mag*cos(theta)
            dy = cross(rrel, norm(vrel)).mag  # rrel.mag*sin(theta)
            # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
            #   from the center of atom i to the center of atom j where atome j hits atom i:
            alpha = asin(dy / (2 * config.Ratom))
            d = (2 * config.Ratom) * cos(alpha) - dx  # distance traveled into the atom from first contact
            deltat = d / vrel.mag  # time spent moving from first contact to position inside atom

            posi = posi - vi * deltat  # back up to contact configuration
            posj = posj - vj * deltat
            mtot = 2 * config.mass
            pcmi = p[i] - ptot * config.mass / mtot  # transform momenta to cm frame
            pcmj = p[j] - ptot * config.mass / mtot
            rrel = norm(rrel)
            pcmi = pcmi - 2 * pcmi.dot(rrel) * rrel  # bounce in cm frame
            pcmj = pcmj - 2 * pcmj.dot(rrel) * rrel
            p[i] = pcmi + ptot * config.mass / mtot  # transform momenta back to lab frame
            p[j] = pcmj + ptot * config.mass / mtot
            apos[i] = posi + (p[i] / config.mass) * deltat  # move forward deltat in time
            apos[j] = posj + (p[j] / config.mass) * deltat

        # collisions with walls
        for i in range(last_Natoms):

            # проекция радиус-вектора на плоскость
            loc = vector(apos[i])
            loc.y = 0

            # вылет за боковую стенку (цилиндр радиуса L / 2 + config.Ratom)
            if (mag(loc) > L / 2 + 0.01 - last_Ratom + sqrt(p[i].x**2 + p[i].z**2) / config.mass * dt):

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
            if loc.y + p[i].y / config.mass * dt < - L / 2 - 0.01 + last_Ratom:
                p[i].y = abs(p[i].y)

            if loc.y + p[i].y / config.mass * dt > cylindertop.pos.y - last_Ratom:
                v_otn = p[i].y / config.mass + sp
                if v_otn > 0:
                    p[i].y = (-v_otn - sp) * config.mass
        
        # type here

    if last_model == 0:
        disp.delete()
    else:
        unavail.Destroy()

    g1.display.delete()
    g2.display.delete()

    graph_text.Destroy()
    speed_text.Destroy()

MenuInterface()

while True:
    if config.menu_switch == 1:
        ModelInterface()
        while config.menu_switch:
            Simulation()
            sleep(0.1)
        MenuInterface()
    
    if config.menu_switch == 2:
        AuthorsInterface()
        while config.menu_switch:
            sleep(0.1)
        MenuInterface()

    if config.menu_switch == 3:
        TheoryInterface()
        while config.menu_switch:
            sleep(0.1)
        MenuInterface()

    sleep(0.1)