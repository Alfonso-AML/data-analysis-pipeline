import pandas as pd
import numpy as np
import math
import AAML_functions as aam
import requests
from PIL import Image
from io import BytesIO
from fpdf import FPDF 
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter



dfilms = aam.getdf()

films = aam.dfcleaner(dfilms)
aam.filesaver(films)

aam.pelisapi()
aam.pdfcreator()


