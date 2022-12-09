from fastapi import FastAPI, Path, UploadFile, File
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import numpy as np
from collections import Counter
import itertools

app=FastAPI(title='TPI #1',
            description='Aqui realizamos las consultas solicitadas')


dataframe = pd.read_csv("C:/Users/Predator/Desktop/Lauti/Programación/SoyHenry/Clases/61._TPI_#1/df_definitivo.csv")

@app.get("/get_max_duration/")
async def get_max_duration(año:int, plataforma:str, min_o_season:str):
    mascara_movie = dataframe['Type'] == 'Movie'
    mascara_season = dataframe['Type'] == 'TV Show'
    mascara1 = dataframe['Release_Year'] == año
    mascara2 = dataframe['Platform'] == plataforma
    mascara3 = dataframe['Duration'].max()
    if min_o_season == 'season':
        print(dataframe[mascara1&mascara2&mascara_season].sort_values('Duration')['Duration'].tail(1).to_dict())
    else:
        return dataframe[mascara1&mascara2&mascara_movie].sort_values('Duration')['Duration'].tail(1).to_dict()

@app.get("/get_count_platform/")
async def get_count_platform(plataforma):
    mascaro1 = dataframe['Platform'] == plataforma
    mascaro_peliculas = dataframe['Type'] == 'Movie'
    mascaro_seasons = dataframe['Type'] == 'TV Show'
    return {f"Peliculas: {dataframe[mascaro1&mascaro_peliculas].count()[0].tolist()}",
            f"Series:, {dataframe[mascaro1&mascaro_seasons].count()[0].tolist()}"}

@app.get("/get_listedin/")
async def get_listedin(genero):
    mas = dataframe['Listed_in'].str.contains(genero, case=False)
    mas_amazonprime = dataframe['Platform'] == 'Amazon_Prime'
    mas_disneyplus = dataframe['Platform'] == 'Disney_Plus'
    mas_hulu = dataframe['Platform'] == 'Hulu'
    mas_netflix = dataframe['Platform'] == 'Netflix'
    return f"Amazon Prime cuenta con {dataframe[mas&mas_amazonprime].count()[0].tolist()}, Disney PLus {dataframe[mas&mas_disneyplus].count()[0].tolist()}, Hulu {dataframe[mas&mas_hulu].count()[0].tolist()} y Netflix {dataframe[mas&mas_netflix].count()[0].tolist()}"

@app.get("/get_actor/")
async def get_actor(plataforma:str, año:int):
    prueba = itertools.chain(*dataframe['Cast'].str.split(','))
    hola = Counter(list(prueba)).most_common()[1]
    mas_platform = dataframe['Platform'] == plataforma
    mas_year = dataframe['Release_Year'] == año
    prueba2 = list(itertools.chain(*dataframe[mas_platform&mas_year]['Cast'].str.split(',')))
    return f"Los dos actores que mas se repiten son {Counter(prueba2).most_common()[0:2]}"   