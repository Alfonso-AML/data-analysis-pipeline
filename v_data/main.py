import pandas as pd
import numpy as np
import math
import AAML_functions as aam
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF 


dfilms = aam.getdf()

films = aam.dfcleaner(dfilms)
aam.filesaver(films)

aam.pelisapi()



