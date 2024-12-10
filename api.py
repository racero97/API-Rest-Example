# Escriba (o pegue) aquí su solución
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/") 
def main(limit:int | None = None , search: str = ""):
    response = requests.get('https://elpais.com/')
    soup=BeautifulSoup(response.text,'html5lib')
    articulos = soup.find_all('article','c')
    row=[]
    for articulo in articulos:
        titulo = articulo.find('h2', class_='c_t').text
        autor= articulo.find('div', class_='c_a')
        if autor:
            try:
                autor=autor.a.text
            except AttributeError:
                autor=""
        else:
            autor=""        
        descripcion= articulo.find('p', class_='c_d')
        
        if descripcion:
            descripcion= descripcion.text
        else:
            descripcion=""
         
        if search:
            if search.lower() in titulo.lower():
                row.append({"titulo": titulo, "autor": autor, "descripcion": descripcion})
            else:
                continue
        else:
            row.append({"titulo": titulo, "autor": autor, "descripcion": descripcion})
        
        if len(row)==limit:
            break

    resultado = json.dumps(row,ensure_ascii=False)
    return {resultado}


@app.get("/{categoria}/")
def read_categoria(categoria: str,limit:int | None = None, search: str = ""):
    response = requests.get(f'https://elpais.com/{categoria}')
    soup=BeautifulSoup(response.text,'html5lib')
    articulos = soup.find_all('article','c')
    row=[]
    for articulo in articulos:
        titulo = articulo.find('h2', class_='c_t').text
        autor= articulo.find('div', class_='c_a')
        if autor:
            try:
                autor=autor.a.text
            except AttributeError:
                autor=""
        else:
            autor=""        
        descripcion= articulo.find('p', class_='c_d')
        if descripcion:
            descripcion= descripcion.text
        else:
            descripcion=""
            
        if search:
            if search.lower() in titulo.lower():
                row.append({"titulo": titulo, "autor": autor, "descripcion": descripcion})
            else:
                continue
        else:
            row.append({"titulo": titulo, "autor": autor, "descripcion": descripcion})
    
        if len(row)==limit:
            break

    resultado = json.dumps(row,ensure_ascii=False)
    return {resultado}    
