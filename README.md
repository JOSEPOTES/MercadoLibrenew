# Extractor de Datos de Talleres

Este proyecto es un sistema automatizado para extraer información de talleres mecánicos y otros negocios similares utilizando Google Maps y otras fuentes de datos.

## Estructura del Proyecto

```
MercadoLibre/
├── extractor/
│   ├── google_extractor.py    # Extractor principal de Google Maps
│   └── mercadolibre.py        # Extractor de MercadoLibre (en desarrollo)
├── result/                    # Directorio para archivos CSV generados
└── README.md                  # Este archivo
```

## Componentes Principales

### 1. Google Extractor (`extractor/google_extractor.py`)

Este script automatiza la extracción de datos de talleres desde Google Maps utilizando Selenium.

#### Características:
- Búsqueda automatizada por tipo de taller y ciudad
- Extracción de información detallada:
  - Nombre del taller
  - Dirección
  - Teléfono
  - Enlaces a redes sociales (Instagram, Facebook)
- Validación y limpieza de datos
- Guardado en formato CSV con codificación UTF-8

#### Tecnologías utilizadas:
- Python 3.x
- Selenium WebDriver
- Chrome en modo headless
- Manejo de codificación UTF-8 con BOM

#### Dependencias:
```python
selenium
urllib3
```

### 2. MercadoLibre Extractor (`extractor/mercadolibre.py`) - En desarrollo

Script para extraer información de talleres desde MercadoLibre.

#### Características planificadas:
- Búsqueda automatizada en MercadoLibre
- Extracción de:
  - Información del vendedor
  - Productos/servicios ofrecidos
  - Calificaciones y reseñas
  - Ubicación

## Uso

### Google Extractor

1. Asegúrate de tener instaladas las dependencias:
```bash
pip install selenium urllib3
```

2. Ejecuta el script:
```bash
python extractor/google_extractor.py
```

3. Sigue las instrucciones en pantalla:
   - Ingresa el tipo de taller que buscas
   - Especifica la ciudad

4. Los resultados se guardarán en la carpeta `result/` en formato CSV

## Características Técnicas

### Manejo de Datos
- Validación de nombres para evitar reseñas y comentarios
- Limpieza de caracteres especiales
- Formato consistente para números telefónicos
- Codificación UTF-8 con BOM para compatibilidad con Excel

### Automatización
- Navegación automatizada con Selenium
- Tiempos de espera aleatorios para evitar bloqueos
- Manejo de errores y excepciones
- Paginación automática de resultados

### Seguridad
- Modo headless para Chrome
- User-Agent personalizado
- Tiempos de espera aleatorios entre acciones

## Próximas Mejoras

1. Integración con base de datos
2. Sistema de deduplicación de registros
3. Exportación a múltiples formatos
4. Interfaz gráfica de usuario
5. Sistema de notificaciones
6. Integración con APIs de geolocalización

## Contribución

Si deseas contribuir al proyecto:
1. Haz fork del repositorio
2. Crea una rama para tu feature
3. Envía un pull request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 