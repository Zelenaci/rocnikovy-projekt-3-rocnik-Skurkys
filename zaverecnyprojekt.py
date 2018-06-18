# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:06:06 2018

@author: Tomas
"""
import pyglet as pg
from pyglet import gl

#Velikost okna

sirka = 900
vyska = 600

velikostmice= 20
sirkapalky = 10
delkapalky = 100
rychlost = 200
rychpalka = rychlost * 1.5

delkacarky = 20
velfont = 40
odsazenitextu = 30

pozice_palek = [vyska // 2, vyska // 2]  # vertikalni pozice palek
pozice_mice = [0, 0]  # souradnice micku 
rychlost_mice = [0, 0]   
stisknute_klavesy = set()  # sada stisknutych klaves
skore = [0, 0]  # skore hracu

#vykreslení hrací plochy

def nakresli_obdelnik(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    gl.glEnd()  # ukonci kresleni trojuhelniku

def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(1, 1, 1)  # nastav barvu kresleni na bilou

window = pyglet.window.Window(width=sirka, height=vyska)
window.push_handlers(
    on_draw=vykresli,
)

def vykresli():
    nakresli_obdelnik(
        pozice_mice[0] - velikostmice // 2,
        pozice_mice[1] - velikostmice // 2,
        pozice_mice[0] + velikostmice // 2,
        pozice_mice[1] + velikostmice // 2,
    )
    
def vykresli():
    for x, y in [(0, pozice_palek[0]), (sirka, pozice_palek[1])]:
        nakresli_obdelnik(
            x - sirkapalky,
            y - delkapalky // 2,
            x + sirkapalky,
            y + delkapalky // 2,
        )
        
def vykresli():
    for y in range(delkacarky // 2, vyska, delkacarky * 2):
        nakresli_obdelnik(
            sirka // 2 - 1,
            y,
            sirka // 2 + 1,
            y + delkacarky
        )
okno = pg.window.Window(width = sirka, height = vyska)
pg.app.run()