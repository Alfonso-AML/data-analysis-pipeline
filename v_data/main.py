import pandas as pd
import numpy as np
import AAML_functions as aam
import requests
from PIL import Image
from io import BytesIO



dfilms = pd.read_csv("./raw_data/lst_films.csv", encoding="utf8")
cols=list(dfilms.columns)

#print(cols)

films = aam.dfcleaner(dfilms)

#print(films.head())
# Hasta aqui, es toda la operación para trabajar el dataframe
# Aqui vamos a intentar establecer los parametros para poder llamar a la API

## Vamos a empezar filtrando por año

year_value = int(input("Seleccione un año entre 2000 y 2018: "))

filt_films = films.loc[films['YEAR'] == year_value]

#print(filt_films.head())

fl_num = int(input("¿Cuantas películas quieres que muestre?  "))
fin_films = filt_films['ID'].sample(n = fl_num)
print(fin_films)
print(type(fin_films))

