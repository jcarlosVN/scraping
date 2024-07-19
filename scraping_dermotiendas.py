import requests
from bs4 import BeautifulSoup
import re

#funciones para descargar la base con productos de manera diaria---------------------------------
def obtener_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def extraer_info_producto(product):
    img = product.find('img', class_='product-image-photo')
    name = product.find('a', class_='product-item-link')
    price = product.find('span', class_='price')
    link = product.find('a', class_='product photo product-item-photo')

    lista = {
        'producto': name.get_text(strip=True),
        'precio_txt': price.get_text(strip=True),
        'img': img['src'],
        'link': link.get('href')
    }
    return lista

def extraer_precio(texto):
    match = re.search(r'S/\xa0(\d+\.\d{2})', texto)
    return float(match.group(1)) if match else None

def obtener_productos(url):
    lista_productos = []
    for i in range(1, 999):
        url_p = f'{url}?p={i}'
        soup = obtener_soup(url_p)
        grilla_products = soup.find('div', class_='products wrapper grid products-grid')
        
        if grilla_products is None:
            break
        else:
            print('lleno')
            print(url_p)
            products = grilla_products.find_all('div', class_='product-item-info')
            for product in products:
                lista = extraer_info_producto(product)
                lista_productos.append(lista)
    return lista_productos