from tkinter import *
from tkinter import font
import pygame
import subprocess
from tkinter import Tk, PhotoImage, Button, Label
from file_checker import checkFile
import os



def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load('C:/Users/Makbaba/Downloads/1.mp3')
    pygame.mixer.music.play(-1)

def open():
    windowDesign.destroy()
    os.system("python gui2.py")


windowDesign = Tk()
IconPhoto = PhotoImage(master = windowDesign, file = 'C:/Users/Makbaba/Downloads/vir.png')
windowDesign.title('Virus Vigilante')
windowDesign.resizable(width = True, height = True)
windowDesign.iconphoto(False, IconPhoto)
windowDesign.geometry('500x400')

windowDesign.configure(bg='black')



selectedFont2 = font.Font(name = 'font_2', family = 'Berlin Sans FB', size = 24, weight = 'normal', slant = 'roman', underline = 0, overstrike = 0)
selectedFont4 = font.Font(name = 'font_4', family = 'Impact', size = 18, weight = 'normal', slant = 'roman', underline = 0, overstrike = 0)
Image4 = PhotoImage(name = 'image_4', file = 'C:/Users/Makbaba/Desktop/vir.png')
Button1 = Button(background = '#ff0000', font = 'font_4', image = '', takefocus = True, text = 'SCAN', command=open )
Button1.place(x = 163, y = 297, height = 53, width = 165, anchor = 'nw')
Label1 = Label(font = 'TkDefaultFont', image = 'image_4', takefocus = True, text = 'Label2',bg="black" )
Label1.place(x = 84, y = 52, height = 228, width = 317, anchor = 'nw')
Label2 = Label(font = 'font_2', image = '', takefocus = True, text = 'Virus Vigilante',fg="red", bg="black" )
Label2.place(x = 144, y = 13, height = 47, width = 200, anchor = 'nw')

windowDesign.after(0, play_music)


windowDesign.mainloop()