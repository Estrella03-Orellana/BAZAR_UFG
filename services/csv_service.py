import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def leer_csv(nombre_archivo):
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    datos = []
    if not os.path.exists(ruta):
        return datos
        
    with open(ruta, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            datos.append(row)
    return datos

def get_categorias():
    return leer_csv('categorias.csv')

def get_productos():
    return leer_csv('productos.csv')

def get_usuarios():
    return leer_csv('usuarios.csv')