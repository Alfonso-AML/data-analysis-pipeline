
# A partir de aqui, es toda la operación para trabajar la API

import requests
from PIL import Image
from io import BytesIO

with open ("./key.txt", "r") as archivo:
    access = archivo.readlines()

key = access[-1].strip()

request = 'tt0859635'
url_data = "http://www.omdbapi.com/?i=" + request + "&apikey=82aef24e" 


req_data = requests.get(url_data)
film_info = req_data.json()

synopsis = film_info['Plot']
poster = requests.get(film_info['Poster'])
img = Image.open(BytesIO(poster.content))
img.save("./img.jpg")
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


print("film rating: ", average)    

print("SYNOPSIS: ",synopsis)
print(type(values))
