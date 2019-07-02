import pandas as pd
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter

"""
def getinfo():
"""
films = pd.read_csv('./c_films.csv')

r_films = pd.read_csv('./film_req.csv')


'''
for x in r_films['poster']:
    if len(x)<5:
        x = './def_pic.jpg'

print(r_films)
'''
title = r_films['title']
synopsis = r_films['synopsis']
rating = r_films['av_rating']

    #return title, poster, av_rating, synopsis
cartel = Image.open("./{}.jpg".format(r_films['ID']))

# Crear pdf

'''
titulo='REQUESTED FILMS'

class PDF(FPDF):
    def header(self):                              # cabecera
        self.set_font('Arial', 'B', 18)            # fuente Arial negrita 15  
        ancho=self.get_string_width(titulo)+6      # calcula el ancho del titulo y su posicion
        self.set_x((210-ancho)/2)
        self.set_draw_color(0, 80, 180)            # colores del marco, fondo y texto
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(3)                     # ancho del marco (1 mm)
        self.cell(ancho, 9, titulo, 1, 1, 'C', 1)  # titulo
        self.ln(10)                                # salto de linea


    def footer(self):                                                # pie de pagina
        self.set_y(-15)                                              # posicion a 1.5 cm desde abajo
        self.set_font('Arial', 'I', 8)                               # fuente Arial italica 8
        self.set_text_color(128)                                     # color texto en gray
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')   # numero de pagina

    def fimg(self):
        c=canvas.Canvas("imagen.pdf", pagesize=A4)
        cartel = Image.open("./{}.jpg".format(r_films['ID']))                                             # genera el pdf
        c.drawImage(cartel, 0, 0, width=600, height=350)             # pinta la imagen
        c.showPage()                 
        c.save()

    def ftitle(self, title):                                                    # titulo de la pelicula
        self.set_font('Arial', '', 12)                                         # fuente Arial 12
        self.set_fill_color(200, 220, 255)                                     # color del fondo
        self.cell(0, 6, title, 0, 1, 'L', 1)                                   # titulo
        self.ln(4)                                                             # salto de linea

    def frating(self, rating):                                                 # titulo de la pelicula
        self.set_font('Arial', '', 12)                                         # fuente Arial 12
        self.set_fill_color(200, 220, 255)                                     # color del fondo
        self.cell(0, 6, ("Film average rating: {}".format(rating), 0, 1, 'L', 1))       # titulo
        self.ln(4)                                                             # salto de linea
    
    def fsynopsis(self, synopsis):                                                 # titulo de la pelicula
        self.set_font('Arial', '', 12)                                         # fuente Arial 12
        self.set_fill_color(200, 220, 255)                                     # color del fondo
        self.cell(0, 6, ("SYNOPSIS: {}".format(synopsis), 0, 1, 'L', 1))       # titulo
        self.ln(4) 

    def print_page(self, ftitle, frating, fsynopsis):     # imprime el capitulo
        self.add_page()                                  # añade pagina
        self.fimg ()
        self.ftitle (title)
        self.fsynopsis(synopsis)                # numero y titulo de capitulo
        


    
    



pdf=PDF()                                                             # inicia clase PDF
pdf.set_title(titulo)                                                 # titulo
pdf.print_page(title, rating, synopsis)         # capitulo 1
pdf.output('requested_films.pdf', 'F')                                # guarda pdf


'''