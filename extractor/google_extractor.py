import time
import random
import csv
import urllib.parse
import os
import unicodedata
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Entrada por consola ---
busqueda = input('¿Qué tipo de taller buscas? (ej: Taller de carros): ').strip()
ciudad = input('¿En qué ciudad? (ej: Bogotá): ').strip()

# --- Generar URL de búsqueda ---
query = f"{busqueda} en {ciudad}"
query_encoded = urllib.parse.quote_plus(query)
URL = f"https://www.google.com/search?tbm=lcl&q={query_encoded}"

print(f"\nURL generada para la búsqueda: {URL}\n")

# --- Configuración de Selenium ---
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

browser = webdriver.Chrome(options=chrome_options)
browser.get(URL)
time.sleep(random.uniform(3, 5))

# --- Esperar la lista de resultados ---
wait = WebDriverWait(browser, 10)
resultados = []
pagina = 1

def limpiar_texto(texto):
    if not texto:
        return ''
    # Normalizar a unicode, eliminar saltos de línea, tabs y espacios extra
    texto = unicodedata.normalize('NFKC', texto)
    texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    return texto

def limpiar_telefono(telefono):
    if not telefono:
        return ''
    # Dejar solo dígitos
    telefono_num = ''.join(filter(str.isdigit, telefono))
    # Asegurar prefijo +57
    if telefono_num.startswith('57'):
        telefono = '+' + telefono_num
    elif telefono_num:
        telefono = '+57' + telefono_num
    else:
        telefono = ''
    # Forzar que se guarde como texto en CSV (anteponer apóstrofe)
    if telefono:
        telefono = "'" + telefono
    return telefono

def es_nombre_valido(nombre):
    # Palabras que indican que el texto es una reseña o comentario
    palabras_resena = ['excelente', 'servicio', 'profesional', 'recomiendo', 'atención', 
                      'muy bueno', 'buen servicio', 'buena atención', 'recomendado']
    
    # Verificar si el nombre contiene palabras de reseña
    nombre_lower = nombre.lower()
    for palabra in palabras_resena:
        if palabra in nombre_lower:
            return False
    
    # Verificar longitud mínima y máxima
    if len(nombre) < 3 or len(nombre) > 100:
        return False
    
    # Verificar que contenga al menos una letra
    if not any(c.isalpha() for c in nombre):
        return False
    
    return True

while True:
    try:
        lista = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rl_tile-group')))
        items = lista.find_elements(By.CSS_SELECTOR, 'span.OSrXXb')
        print(f"\nPágina {pagina}: Se encontraron {len(items)} talleres.")
        for idx, item in enumerate(items):
            try:
                # Extraer el nombre del panel derecho
                browser.execute_script("arguments[0].scrollIntoView();", item)
                item.click()
                time.sleep(random.uniform(2, 3))
                
                try:
                    nombre_element = browser.find_element(By.CSS_SELECTOR, 'div.SPZz6b h2 span')
                    nombre = limpiar_texto(nombre_element.text)
                except:
                    nombre = limpiar_texto(item.text)
                
                # Validar el nombre
                if not es_nombre_valido(nombre):
                    print(f"Nombre inválido detectado y descartado: {nombre}")
                    continue
                
                # Extraer dirección
                try:
                    direccion = limpiar_texto(browser.find_element(By.CSS_SELECTOR, 'div.zloOqf.PZPZlf span.LrzXr').text)
                except:
                    direccion = ''
                
                # Extraer teléfono
                try:
                    telefono = limpiar_telefono(browser.find_element(By.CSS_SELECTOR, 'span.LrzXr.zdqRlf.kno-fv').text)
                except:
                    telefono = ''
                
                # Extraer redes sociales
                instagram = ''
                facebook = ''
                try:
                    redes = browser.find_elements(By.CSS_SELECTOR, 'a')
                    for red in redes:
                        href = red.get_attribute('href')
                        if href:
                            if 'instagram.com' in href:
                                instagram = href
                            if 'facebook.com' in href:
                                facebook = href
                except:
                    pass
                
                resultados.append({
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono,
                    'instagram': instagram,
                    'facebook': facebook
                })
                
                # Mostrar en consola la información estructurada
                print(f"\nTaller {len(resultados)}:")
                print(f"  Nombre: {nombre}")
                print(f"  Dirección: {direccion}")
                print(f"  Teléfono: {telefono}")
                print(f"  Instagram: {instagram}")
                print(f"  Facebook: {facebook}")
                print("-"*40)
                
            except Exception as e:
                print(f"Error en taller {idx+1} de la página {pagina}: {e}")
            time.sleep(random.uniform(1, 2))
            
        # Intentar ir a la siguiente página
        try:
            next_links = browser.find_elements(By.CSS_SELECTOR, 'a.fl')
            next_link = None
            for link in next_links:
                if link.text.strip() in [str(pagina+1), 'Siguiente', 'Next']:
                    next_link = link
                    break
            if next_link:
                print(f"\nPasando a la página {pagina+1}...")
                browser.execute_script("arguments[0].scrollIntoView();", next_link)
                next_link.click()
                pagina += 1
                time.sleep(random.uniform(3, 5))
            else:
                print("\nNo hay más páginas de resultados.")
                break
        except Exception:
            print("\nNo hay más páginas de resultados.")
            break
    except Exception as e:
        print(f"No se pudo obtener la lista de talleres en la página {pagina}: {e}")
        break

# --- Guardar resultados en CSV ---
filename = f"talleres_{ciudad.replace(' ', '_').lower()}.csv"
file_path = os.path.join(r"C:\Users\Joseg\Desktop\Carlider\MercadoLibre\result", filename)

# Guardar con BOM para mejor compatibilidad con Excel
with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['nombre', 'direccion', 'telefono', 'instagram', 'facebook']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in resultados:
        writer.writerow(row)

print(f"\nExtracción finalizada. Resultados guardados en {file_path}")
browser.quit()
