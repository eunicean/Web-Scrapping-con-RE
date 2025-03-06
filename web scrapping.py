import re
import csv
from bs4 import BeautifulSoup

BUFFER_SIZE = 50
MAX_IMAGENES = 1000

def limpiar(texto):
    return re.sub(r'[^a-zA-Z0-9\s]', '', texto)

def cargar_html(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        return f.read()

def extraer_productos(soup):
    datos = []
    contador = 0

    for div in soup.find_all('div'):
        if contador >= MAX_IMAGENES:
            print("Ya son muchas imágenes, paro.")
            break

        img = div.find('img')
        if img:
            url = img.get('data-a-hires') or img.get('src')
            alt = img.get('alt', '').strip()

            if alt:
                nombre = limpiar(alt)
            else:
                a = div.find_parent('a')
                span = a.find('span', class_='a-truncate-full') if a else None
                nombre = limpiar(span.text.strip()) if span else 'Sin nombre'

            datos.append({'Nombre de la imagen': nombre, 'URL de la Imagen': url})
            contador += 1

            if len(datos) >= BUFFER_SIZE:
                guardar_csv(datos, 'productos.csv', False)
                datos.clear()

    return datos, contador

def guardar_csv(productos, nombre_archivo, escribir_cabecera=True):
    with open(nombre_archivo, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, ['Nombre de la imagen', 'URL de la Imagen'])
        if escribir_cabecera:
            writer.writeheader()
        writer.writerows(productos)


html = cargar_html('Rech.html')
sopa = BeautifulSoup(html, 'html.parser')

# Primero creo el archivo y escribo la cabecera
guardar_csv([], 'productos.csv')

info, total = extraer_productos(sopa)

if info:
    guardar_csv(info, 'productos.csv', False)

print(f"Total de imágenes guardadas: {total}")
