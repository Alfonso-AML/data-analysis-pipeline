import pandas as pd
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF

def getinfo():
    films = pd.read_csv('./c_films.csv')
    r_films = pd.read_csv('./film_req.csv')
    


# Crear pdf


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


    def chapter_title(self, numero, etiqueta):                                 # titulo del capitulo
        self.set_font('Arial', '', 12)                                         # fuente Arial 12
        self.set_fill_color(200, 220, 255)                                     # color del fondo
        self.cell(0, 6, 'Chapter %d : %s' % (numero, etiqueta), 0, 1, 'L', 1)  # titulo
        self.ln(4)                                                             # salto de linea


    def chapter_body(self, nombre, numero):                      # cuerpo del capitulo
        with open(nombre, 'rb') as f:                            # se lee el archivo de texto
            txt=f.read().decode('latin-1')
        self.set_font('Times', '', 12)                           # fuente Times 12
        self.multi_cell(0, 5, txt)                               # texto con saltos de linea (multicelda)
        self.ln()                                                # salto de linea
        self.set_font('', 'I')                                   # alusion en fuente italica
        self.cell(0, 5, '(fin del capitulo {})'.format(numero))


    def print_chapter(self, numero, titulo, nombre):     # imprime el capitulo
        self.add_page()                                  # añade pagina
        self.chapter_title(numero, titulo)               # numero y titulo de capitulo
        self.chapter_body(nombre, numero)                # cuerpo del capitulo



pdf=PDF()                                                             # inicia clase PDF
pdf.set_title(titulo)                                                 # titulo
pdf.set_author('Jake VanderPlas')                                     # autor
pdf.print_chapter(1, 'IPython: Beyond Normal Python', 'c1.txt')       # capitulo 1
pdf.print_chapter(2, 'Introduction to NumPy', 'c2.txt')               # capitulo 2
pdf.output('libro.pdf', 'F')                                          # guarda pdf


