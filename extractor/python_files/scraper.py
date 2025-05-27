import requests
from bs4 import BeautifulSoup
import csv
import time
import re

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.productos = []

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def extract_all_brand_links(self, soup):
        # Buscar el div de marcas
        brand_div = None
        for div in soup.select('div.ui-search-filter-dl.shops__filter-items'):
            h3 = div.find('h3')
            if h3 and 'Marca' in h3.get_text():
                brand_div = div
                break
        if not brand_div:
            return []
        # Extraer todos los enlaces de marcas
        brand_links = brand_div.select('li.ui-search-filter-container.shops__container-lists a.ui-search-link')
        # Buscar si hay un enlace 'Mostrar más'
        show_more = brand_div.select_one('a.ui-search-modal__link')
        if show_more and 'Mostrar más' in show_more.get_text():
            more_url = show_more['href']
            if not more_url.startswith('http'):
                more_url = 'https://www.carlider.co' + more_url
            more_soup = self.get_soup(more_url)
            # Extraer marcas adicionales de la tabla modal
            grid = more_soup.select_one('div.ui-search-search-modal-grid-columns')
            if grid:
                modal_brand_links = grid.select('a.ui-search-search-modal-filter.ui-search-link')
                for link in modal_brand_links:
                    name_span = link.select_one('span.ui-search-search-modal-filter-name')
                    if name_span:
                        brand_links.append(link)
        # Filtrar solo marcas reales (que tengan span con la clase de nombre de marca)
        brands = []
        for link in brand_links:
            # Puede venir de la tabla modal o del sidebar
            name_span = link.select_one('span.ui-search-filter-name.shops-custom-secondary-font')
            if not name_span:
                name_span = link.select_one('span.ui-search-search-modal-filter-name')
            if name_span:
                brands.append({
                    'name': name_span.get_text(strip=True),
                    'url': link['href']
                })
        return brands

    def extract_titles(self, soup):
        titles = soup.select('.poly-component__title')
        return [title.get_text(strip=True) for title in titles]

    def extract_prices(self, soup):
        prices = soup.select('.andes-money-amount.andes-money-amount--cents-superscript .andes-money-amount__fraction')
        return [price.get_text(strip=True) for price in prices]

    def extract_links(self, soup):
        links = soup.select('.poly-card__content a')
        return [link['href'] for link in links if link.has_attr('href')]

    def next_page(self, soup):
        next_button = soup.select_one('li.andes-pagination__button--next a')
        if next_button and next_button.has_attr('href'):
            return next_button['href']
        return None

    def save_to_csv(self, car_name, filename=None):
        if not filename:
            # Limpiar el nombre del archivo: minúsculas, sin espacios ni caracteres especiales
            clean_name = re.sub(r'[^a-z0-9]', '', car_name.lower().replace(' ', ''))
            filename = f'{clean_name}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['nombre', 'valor', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for producto in self.productos:
                writer.writerow(producto)
        print(f"Se han guardado {len(self.productos)} productos en {filename}")

    def run(self):
        main_url = "https://www.carlider.co/listado/accesorios-vehiculos/repuestos-carros-camionetas/"
        soup = self.get_soup(main_url)
        brands = self.extract_all_brand_links(soup)
        print("Marcas disponibles:")
        for brand in brands:
            print(brand['name'])
        car_name = input("Escribe el nombre del carro: ")
        selected_brand = next((b for b in brands if car_name.lower() == b['name'].lower()), None)
        if not selected_brand:
            print(f"No se encontró la marca: {car_name}")
            return
        car_url = selected_brand['url']
        if not car_url.startswith('http'):
            car_url = 'https://www.carlider.co' + car_url
        while car_url:
            soup = self.get_soup(car_url)
            titles = self.extract_titles(soup)
            prices = self.extract_prices(soup)
            links = self.extract_links(soup)
            for title, price, link in zip(titles, prices, links):
                self.productos.append({
                    'nombre': title,
                    'valor': price,
                    'link': link
                })
                print(f"Producto extraído: {title}")
            car_url = self.next_page(soup)
            time.sleep(1)  # Espera para evitar bloqueo
        self.save_to_csv(car_name)

if __name__ == '__main__':
    scraper = Scraper()
    scraper.run() 