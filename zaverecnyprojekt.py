# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:06:06 2018

@author: Tomas
"""
import pyglet
from pyglet import gl
from pyglet.window.key import W,S,UP,DOWN
import random

sirka = 1600
vyska = 900
velmic = 18
sirkapalky = 15
delkapalky = 120
rychlost = 300
rychpalky = rychlost * 1.2
velfont = 40
delkapulcary = 20
odsazenitextu = 30

pozicepalek = [vyska // 2, vyska // 2]  # vertikalni pozice palek
pozicemice = [0, 0]  # souradnice micku 
rychlostmice = [0, 0]   
stiskklavesy = set()  # sada stisknutych klaves
skore = [0, -1]  # skore hracu



#vykreslení hrací plochy
def nakresli_obdelnik(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    gl.glEnd()  # ukonci kresleni trojuhelniku

#smazáni plochy
def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna
    gl.glColor3f(1, 1, 1)  # barva kresleni - bila
    
#vykreslení míče     
    nakresli_obdelnik(
            pozicemice[0] - velmic // 2,
            pozicemice[1] - velmic // 2,
            pozicemice[0] + velmic // 2,
            pozicemice[1] + velmic // 2,)
    
#vykreslení pálek      
    for x, y in [(0, pozicepalek[0]), (sirka, pozicepalek[1])]:
        nakresli_obdelnik(
                x - sirkapalky,
                y - delkapalky // 2,
                x + sirkapalky,
                y + delkapalky // 2,)
        
#vykreslení půlící čáry               
    for y in range(delkapulcary // 2, vyska, delkapulcary * 2):
        nakresli_obdelnik(
                sirka // 2 - 1,
                y,
                sirka // 2 + 1,
                y + delkapulcary)
        
#vykreslení skóre               
    nakresli_text(
        str(skore[0]),
        x=odsazenitextu,
        y=vyska - odsazenitextu - velfont,
        pozice_x='left')

    nakresli_text(
        str(skore[1]),
        x=sirka - odsazenitextu,
        y=vyska - odsazenitextu - velfont,
        pozice_x='right')
        
        
def nakresli_text(text, x, y, pozice_x):
    napis = pyglet.text.Label(
            text,
            font_size=velfont,
            x=x, y=y, anchor_x=pozice_x)
    napis.draw()

#klavesy    
def stisk_klavesy(symbol, modifikatory):
    if symbol == W:
        stiskklavesy.add(('nahoru', 0))
    if symbol == S:
        stiskklavesy.add(('dolu', 0))
    if symbol == UP:
        stiskklavesy.add(('nahoru', 1))
    if symbol == DOWN:
        stiskklavesy.add(('dolu', 1))

def pusteni_klavesy(symbol, modifikatory):
    if symbol == W:
        stiskklavesy.discard(('nahoru', 0))
    if symbol == S:
        stiskklavesy.discard(('dolu', 0))
    if symbol == UP:
        stiskklavesy.discard(('nahoru', 1))
    if symbol == DOWN:
        stiskklavesy.discard(('dolu', 1))
        
#rychlost míče na začátku
def reset():
    pozicemice[0] = sirka // 2
    pozicemice[1] = vyska // 2

    if random.randint(0, 1):
        rychlostmice[0] = rychlost
    else:
        rychlostmice[0] = -rychlost

    rychlostmice[1] = random.uniform(-1, 1) * rychlost
        
def obnov_stav(dt): 
#pohyb pálek
    for cislo_palky in (0, 1):
        if ('nahoru', cislo_palky) in stiskklavesy:
            pozicepalek[cislo_palky] += rychpalky * dt
        if ('dolu', cislo_palky) in stiskklavesy:
            pozicepalek[cislo_palky] -= rychpalky * dt

        if pozicepalek[cislo_palky] < delkapalky / 2:
            pozicepalek[cislo_palky] = delkapalky / 2
        if pozicepalek[cislo_palky] > vyska - delkapalky / 2:
            pozicepalek[cislo_palky] = vyska - delkapalky / 2
            

#pohyb míče      
    pozicemice[0] += rychlostmice[0] * dt
    pozicemice[1] += rychlostmice[1] * dt  
    
#odraz míče
    if pozicemice[1] < velmic // 2:
        rychlostmice[1] = abs(rychlostmice[1])
    if pozicemice[1] > vyska - velmic // 2:
        rychlostmice[1] = -abs(rychlostmice[1])
    
    palka_min = pozicemice[1] - velmic / 2 - delkapalky / 2
    palka_max = pozicemice[1] + velmic / 2 + delkapalky / 2
    
#odražení vlevo
    if pozicemice[0] < sirkapalky + velmic / 2:
        if palka_min < pozicepalek[0] < palka_max:
            rychlostmice[0] = abs(rychlostmice[0])
        else:
            skore[1] += 1
            reset()

#odražení vpravo
    if pozicemice[0] > sirka - (sirkapalky + velmic / 2):
        if palka_min < pozicepalek[1] < palka_max:
            rychlostmice[0] = -abs(rychlostmice[0])
        else:
            skore[0] += 1
            reset()
            
pyglet.clock.schedule(obnov_stav)
window = pyglet.window.Window(width=sirka, height=vyska)
window.push_handlers(
    on_draw=vykresli,
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy)

pyglet.app.run()