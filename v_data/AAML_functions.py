import pandas as pd
import numpy as np
import pprint

from PDF import PDF


def download_poster(file_link, ref):
    print(file_link)
    file_type = ""
    file_type = file_link.split('.')
    file_type = '.%s' % (file_type[-1])
    r = requests.get(file_link, verify=False, stream=True)
    with open("./posters/%s%s" % (ref, file_type), 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024): 
          if chunk: # filter out keep-alive new chunks
              f.write(chunk)      

def create_pdf(filmbag):
    
    pdf = PDF()
    title = 'Films Book'
    pdf.set_title(title)
    pdf.set_author('Alfonso') 
    x = 0
    for film in filmbag:
        x += 1
        pdf.new_page(film['title'])
        pdf.print_film(film,x)
    pdf.output('%s.pdf' % (title), 'F')                                          # guarda pdf


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

import requests
from io import BytesIO

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
    
    with open ("./key.txt", "r") as archivo:
        access = archivo.readlines()

    key = access[-1].strip()

    fl_count = 0
    for request in fin_films:

        url_data = "http://www.omdbapi.com/?i={}&apikey={}".format(request, key)  
        
        req_data = requests.get(url_data)
        film_info = req_data.json()
        
        if('Error' in film_info):
            print('Una de las películas no está disponible: %s' % film_info['Error'])
        else:
            fl_count += 1

            synopsis = film_info['Plot']

            if(film_info['Poster'] != 'N/A'):
                download_poster(film_info['Poster'],request)

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

            film_data = films.loc[films['ID'] == request]
            film_data = film_data.values.tolist()

            filmbag.append ({'id': request, 
                            'title': film_data[0][2],
                            'synopsis': synopsis, 
                            'poster': film_info['Poster'],
                            'average': average,
                            'year': film_data[0][3],
                            'duration': film_data[0][4],
                            'type': film_data[0][5]
                            })
            
            if(fl_count == fl_num):
                # Si tenemos el número de películas solicitadas, paramos.
                break

    pprint.pprint(filmbag)
    return filmbag
    