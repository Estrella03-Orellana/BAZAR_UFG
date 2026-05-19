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




def add_categoria(categoria):

    ruta = os.path.join(DATA_DIR, 'categorias.csv')

    categorias = get_categorias()

    nuevo_id = 1

    if categorias:
        nuevo_id = max(int(c['id']) for c in categorias) + 1

    with open(ruta, mode='a', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow([
            nuevo_id,
            categoria['nombre']
        ])


def update_categoria(categoria_actualizada):

    ruta = os.path.join(DATA_DIR, 'categorias.csv')

    categorias = get_categorias()

    with open(ruta, mode='w', newline='', encoding='utf-8') as file:

        fieldnames = ['id', 'nombre']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for categoria in categorias:

            if int(categoria['id']) == int(categoria_actualizada['id']):

                categoria['nombre'] = categoria_actualizada['nombre']

            writer.writerow(categoria)


def delete_categoria(id):

    ruta = os.path.join(DATA_DIR, 'categorias.csv')

    categorias = get_categorias()

    categorias_filtradas = [
        categoria for categoria in categorias
        if int(categoria['id']) != int(id)
    ]

    with open(ruta, mode='w', newline='', encoding='utf-8') as file:

        fieldnames = ['id', 'nombre']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(categorias_filtradas)




def add_producto(producto):

    ruta = os.path.join(DATA_DIR, 'productos.csv')

    productos = get_productos()

    nuevo_id = 1

    if productos:
        nuevo_id = max(int(p['id']) for p in productos) + 1

    with open(ruta, mode='a', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow([
            nuevo_id,
            producto['nombre'],
            producto['precio'],
            producto['categoria_id']
        ])


def update_producto(producto_actualizado):

    ruta = os.path.join(DATA_DIR, 'productos.csv')

    productos = get_productos()

    with open(ruta, mode='w', newline='', encoding='utf-8') as file:

        fieldnames = ['id', 'nombre', 'precio', 'categoria_id']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for producto in productos:

            if int(producto['id']) == int(producto_actualizado['id']):

                producto['nombre'] = producto_actualizado['nombre']
                producto['precio'] = producto_actualizado['precio']
                producto['categoria_id'] = producto_actualizado['categoria_id']

            writer.writerow(producto)


def delete_producto(id):

    ruta = os.path.join(DATA_DIR, 'productos.csv')

    productos = get_productos()

    productos_filtrados = [
        producto for producto in productos
        if int(producto['id']) != int(id)
    ]

    with open(ruta, mode='w', newline='', encoding='utf-8') as file:

        fieldnames = ['id', 'nombre', 'precio', 'categoria_id']

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(productos_filtrados)