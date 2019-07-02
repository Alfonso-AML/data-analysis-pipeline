import pandas as pd
import numpy as np
import AAML_functions as aam
import requests
from PIL import Image
from io import BytesIO



dfilms = pd.read_csv("./raw_data/lst_films.csv", encoding="utf8")
cols=list(dfilms.columns)

films = aam.dfcleaner(dfilms)
films.to_csv('./c_films.csv')

aam.pelisapi()

