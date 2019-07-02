import pandas as pd
import numpy as np
import math
import requests
from io import BytesIO
from fpdf import FPDF 

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
    col_names = ['ID', 'synopsis', 'poster', 'av_rating']
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

    fl_count = 0
    for request in fin_films:
    

        url_data = "http://www.omdbapi.com/?i={}&apikey={}".format(request, key)  
        
        req_data = requests.get(url_data)
        film_info = req_data.json()
        # Esta funcion de a continuación, va a permitir evitar  que el error pare el proceso
        if('Error' in film_info):
            print('Una de las películas no está disponible: %s' % film_info['Error'])
        else:
            fl_count += 1

            synopsis = film_info['Plot']

            #poster = requests.get(film_info['Poster'])
            #img = Image.open(BytesIO(poster.content))
            #img.save("./img.jpg")

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
            

            filmbag.append ([request, synopsis, film_info['Poster'], average])
            
            if(fl_count > fl_num):
                # Si tenemos el número de películas solicitadas, paramos.
                break

    film_req = pd.DataFrame(filmbag,columns=col_names)
    print("Resultado: ", film_req)
    film_req.to_csv('./film_req.csv')
    
    return film_req

def pdfcreator():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_margins()
    