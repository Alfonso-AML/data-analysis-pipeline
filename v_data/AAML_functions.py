import pandas as pd
import numpy as np
import math
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
 

# Funcion para obtener el csv
def getdf():
    dr_file = pd.read_csv("./raw_data/lst_films.csv", encoding="utf8")
    cols=list(dr_file.columns)
    return dr_file

# Funcion para guardar el csv
def filesaver(file_n):
    file_n.to_csv('./c_films.csv')

def dfcleaner(df):
    cols=list(df.columns)
    df1 = df.dropna(axis=0, subset=[cols[2]])
    df1[cols[2]] = df1[cols[2]].apply(np.int64)
    df1[cols[4]].fillna(" ", inplace=True)
    df1[cols[3]].fillna(" ", inplace=True)
    df2 = df1[df1['YEAR'] > 1999]
    df3 = df2[df2['YEAR'] < 2019]

    return df3




# A partir de aqui, es toda la operación para trabajar la API

def pelisapi():
    films = pd.read_csv('./c_films.csv')
    col_names = ['ID', 'title', 'synopsis', 'av_rating', 'col_n']
    film_req = pd.DataFrame(columns = col_names)
    filmbag = []

    year_value = int(input("Seleccione un año entre 2000 y 2018: "))
    filt_films = films.loc[films['YEAR'] == year_value]

    print('Hay %s películas' % (len(filt_films)))

    fl_num = int(input("¿Cuantas películas quieres que muestre? (1-%s): " % (len(filt_films)-100)))
    fin_films = filt_films['ID'].sample(n = fl_num+100)
    # Como anteriormente he tenido problemas al lanzar solicitudes, vamos a solicitar algunas películas más para tener de backup 
    
    with open ("./key2.txt", "r") as archivo:
        access = archivo.readlines()

    key = access[-1].strip()
    row_count = -1

    fl_count = 0
    for request in fin_films:
        row_count+=1
  
        url_data = "http://www.omdbapi.com/?i={}&apikey={}".format(request, key)  
        
        req_data = requests.get(url_data)
        film_info = req_data.json()
        # Esta funcion de a continuación, va a permitir evitar  que el error pare el proceso
        if('Error' in film_info):
            print('Una de las películas no está disponible: %s' % film_info['Error'])
        else:
            fl_count += 1

            title = film_info['Title']

            synopsis = film_info['Plot']

            poster = film_info['Poster']

       
            if len(poster)<10:
                poster = shutil.copy('def_pic.png', "./{}.jpg".format(film_info['imdbID']))
            elif len(poster):
                flg = requests.get(film_info['Poster'])
                img = Image.open(BytesIO(flg.content))
                img.save("./{}.jpg".format(film_info['imdbID']))

            ratings = film_info['Ratings']
            rat_values = []

            for i in range(len(ratings)):
                rat_values.append(ratings[i]['Value'])

            values = []
            for i in rat_values:
                if '%' in i:
                    values += [float(i.strip('%'))/10]
                if "/100" in i:
                    values += [float(i.replace('/100', ''))/10]
                elif "/10" in i:
                    values += [float(i.replace('/10', ''))]
            
            average = np.mean(values) 
            
            
            filmbag.append ([request, title, synopsis, average, row_count])
            
            if(fl_count > fl_num):
                # Si tenemos el número de películas solicitadas, paramos.
                break

    film_req = pd.DataFrame(filmbag,columns=col_names)
    print("Resultado: ", film_req)
    film_req.to_csv('./film_req.csv')
    
    return film_req


# Crear pdf
def pdfcreator():
    films = pd.read_csv('./c_films.csv')
    r_films = pd.read_csv('./film_req.csv')
    title = r_films['title']
    synopsis = r_films['synopsis']
    rating = r_films['av_rating']

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
            for xs in r_films['col_n']:                                         # Aqui hago un ciclo for para añadir el numero de fila
                cartel = Image.open("./{}.jpg".format(r_films['ID'][xs]))       # genera el pdf
            c.drawImage(cartel, 0, 0, width=600, height=350)                    # pinta la imagen
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



    