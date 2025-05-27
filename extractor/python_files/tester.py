import requests
from bs4 import BeautifulSoup
import csv

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.productos = []

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def extract_car_names(self, soup):
        car_names = soup.select('.ui-search-filter-name.shops-custom-secondary-font')
        return [car.get_text(strip=True) for car in car_names]

    def search_car(self, car_name, soup):
        car_links = soup.select('.ui-search-filter-container.shops__container-lists a')
        for link in car_links:
            if car_name.lower() in link.get_text(strip=True).lower():
                return link['href']
        return None

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
        next_button = soup.select_one('.andes-pagination__button.andes-pagination__button--current')
        if next_button and next_button.has_attr('href'):
            return next_button['href']
        return None

    def save_to_csv(self, filename='productos.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['nombre', 'valor', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for producto in self.productos:
                writer.writerow(producto)

    def run(self):
        main_url = "https://www.carlider.co/listado/accesorios-vehiculos/repuestos-carros-camionetas/"
        soup = self.get_soup(main_url)
        car_names = self.extract_car_names(soup)
        print("Carros disponibles:")
        for car in car_names:
            print(car)

        car_name = input("Escribe el nombre del carro: ")
        car_url = self.search_car(car_name, soup)
        if not car_url:
            print(f"No se encontró el carro: {car_name}")
            return

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

        self.save_to_csv()
        print(f"Se han guardado {len(self.productos)} productos en productos.csv")

if __name__ == '__main__':
    scraper = Scraper()
    scraper.run()
