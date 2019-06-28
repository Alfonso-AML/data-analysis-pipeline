import pandas as pd
import numpy as np
import AAML_functions as aam
import requests

dfilms = pd.read_csv("./raw_data/lst_films.csv", encoding="utf8")
cols=list(dfilms.columns)

#print(cols)

films = aam.dfcleaner(dfilms)

print(films.head(-5))






