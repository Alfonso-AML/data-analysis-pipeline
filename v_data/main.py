import pandas as pd
import numpy as np
import AAML_functions as aam
import PDF as pdf_class
import requests
from io import BytesIO
import warnings
import webbrowser

warnings.filterwarnings('ignore')


dfilms = pd.read_csv("./raw_data/lst_films.csv", encoding="utf8")

films = aam.dfcleaner(dfilms)
films.to_csv('./c_films.csv')

films = aam.pelisapi()
aam.create_pdf(films)

webbrowser.open('./Films Book.pdf')


