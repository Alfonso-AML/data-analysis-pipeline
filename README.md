![IronHack Logo](https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/upload_d5c5793015fec3be28a63c4fa3dd4d55.png)

# data-analysis-pipeline

## Project: Random film selector

In order to learn how to manage different APIs and how to prepare reports in PDF, I've decided to develop this project.

### Requirements:

For this project I've used Ubuntu 16.04 with Python 3.5.2
The libraries that are not included in this version and needs to be installed are:
* FPDF: For installing it run 'pip install fpdf'.

Additionally, I've used the OMBD API that requires a key to connect to the API. It is easy to get, you only need to go to following link 'http://www.omdbapi.com/apikey.aspx' and provide your email. Once you receive the key, place it in a text file and save it as key.txt in main folder (data-analysis-pipeline).


### Steps made:

First, I've obtained a dataframe from Kaggle that contains all IMDB movies from 1894 through 2017 including some titles announced for upcoming years.

Link:

https://www.kaggle.com/crescenzo/imdb-movies-through-2018

This dataset have some null values that I've corrected or dropped taking in account its importance for my purposes. As this dataset is a bit large, I've limited the films years that can be requested from 2000 to 2019, but it can be easily changed modifying dfcleaner function that can be found on AAML_functions in lines 33 to 40.

Next, I've created a function to connect to the OMBD API and to interact with the user.

Finally, I've used FPDF to store and display the user request in a pdf file.

### Folders and files:

* raw_data: This folder contains the dataset downloaded from Kaggle named as lst_films.csv
* v_data: This folder contains contains:
	- main.py: This file is the one you need to run. It runs all functions created in the other files.
	- AAML_functions.py: This file contains almost all functions I've created to develop this project.
	- PDF.py: This file contains the functions of FPDF that are used in AAML_functions.py to create the pdf.
* c_films.csv: This dataset is the result of cleaning the original one from Kaggle (lst_films.csv)
* def_pic.png: Not all films have a poster. So, instead leaving a blank space, I've decided to place a default pic, this pic is the one I've used.
* film_req.csv: This file contains the request you make when running main.py file.

### Usage:

In main folder (data-analysis-pipeline) run the following code and follow intructions given in terminal:

<div align="center">
'python3 ./v_data/main.py'
</div>
