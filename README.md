# PDF a CSV

Esta aplicación convierte un PDF en un CSV extrayendo múltiples tipos de datos:

1. **Texto** de cada página
2. **Gráficos** detectados en imágenes (puntos, etiquetas)
3. **Tablas** incrustadas en el PDF
4. **Metadatos** (título, autor, fechas)
5. **Estructura del documento** (títulos, párrafos, niveles)

Optimizada para informes científicos sobre envejecimiento activo y documentos similares. La app está diseñada para ser modular y fácil de extender, basada en composición y principios de Clean Architecture.

---

## ¿Cómo funciona?

La app se divide en capas y responsabilidades:

- `main.py`: punto de entrada. Recibe rutas del PDF y CSV, arma la app y ejecuta.
- `csv_app/entities.py`: define modelos de dominio (`TextBlock`, `GraphPoint`, `Table`, `DocumentMetadata`, `DocumentStructure`).
- `csv_app/ports.py`: define contratos (protocolos) que cumplen los componentes.
- `csv_app/adapters.py`: implementa adaptadores concretos para PDF, imágenes, OCR, tablas, metadatos y CSV.
- `csv_app/use_cases.py`: contiene lógica de extracción y generación del CSV.
- `csv_app/composition.py`: conecta todos los componentes.

Cada parte se encarga de una responsabilidad y se puede reemplazar sin afectar el resto.

---

## Requisitos

Python 3 y librerías:

- `pdfplumber` — extrae texto del PDF
- `pdf2image` — convierte páginas a imágenes
- `pytesseract` — OCR de etiquetas en gráficos
- `opencv-python-headless` — detecta puntos en gráficos
- `camelot-py` — extrae tablas
- `pandas` — genera CSV
- `Pillow` — maneja imágenes
- `pytest` — tests unitarios

En Windows necesitas instalar Poppler.

## Instalación

1. Abre una terminal en la carpeta del proyecto `c:\wamp64\programacion\Master\csv`.
2. Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

1. Instala Poppler en Windows si no lo tienes. Descarga desde:

- <https://poppler.freedesktop.org/>

Luego apunta al directorio `bin` de Poppler cuando ejecutes la app.

---

## Uso

Ejecuta el script desde la carpeta `csv` con estas rutas:

```powershell
python main.py "C:\ruta\al\archivo.pdf" "C:\ruta\de\salida.csv" --poppler-path "C:\ruta\a\poppler\bin"
```

- `"C:\ruta\al\archivo.pdf"`: ruta del archivo PDF de entrada.
- `"C:\ruta\de\salida.csv"`: ruta del archivo CSV que se creará.
- `--poppler-path "C:\ruta\a\poppler\bin"`: ruta opcional a la carpeta `bin` de Poppler en Windows.

Si Poppler ya está en tu variable `PATH`, puedes omitir `--poppler-path`:

```powershell
python main.py "C:\ruta\al\archivo.pdf" "C:\ruta\de\salida.csv"
```

---

## Qué genera el CSV

El CSV contiene filas de varios tipos:

- `metadata`: metadatos del PDF (título en `x_label`, autor en `y_label`)
- `structure`: estructura del documento (títulos/párrafos con nivel en `x`)
- `table`: datos de tablas (encabezados en `x_label`, fila de datos en `value`)
- `text`: texto extraído de cada página
- `graph_point`: puntos detectados en gráficos

Columnas en el CSV:

- `type`: tipo de fila (`metadata`, `structure`, `table`, `text`, `graph_point`)
- `page`: número de página
- `graph_index`: índice del elemento (tabla, gráfico)
- `value`: contenido (texto, datos de tabla)
- `x`: coordenada X o nivel de estructura
- `y`: coordenada Y
- `x_label`: etiqueta eje X de gráfico / encabezados de tabla / tipo de contenido
- `y_label`: etiqueta eje Y de gráfico

---

## Ejemplo

Si el PDF tiene 2 páginas con metadatos, estructura, tabla y gráfico, el CSV puede verse así:

| type       | page | graph_index | value                    | x     | y     | x_label    | y_label |
|------------|------|-------------|--------------------------|-------|-------|------------|---------|
| metadata   |      |             |                          |       |       | Envejecimiento Activo | Dr. García |
| structure  | 1    |             | Introducción             | 0     |       | heading    |         |
| table      | 1    | 1           | Dato1\|Dato2             | 0     |       | Col1\|Col2 |         |
| text       | 1    |             | Texto de la página 1     |       |       |            |         |
| graph_point| 1    | 1           |                          | 152.4 | 98.7  | Edad       | Actividad |
| structure  | 2    |             | Conclusiones             | 0     |       | heading    |         |
| text       | 2    |             | Texto de la página 2     |       |       |            |         |

---

## Mejoras implementadas

- ✅ Extracción de tablas con Camelot
- ✅ Extracción de metadatos (título, autor, fechas)
- ✅ Estructura del documento (niveles de encabezados)
- ✅ Suite de tests completa (unitarios + integración)
- ✅ Arquitectura modular con composición (sin herencia)

## Posibles mejoras futuras

- Mejorar detección de gráficos (círculares, dispersión, etc.)
- OCR mejorado para etiquetas complejas
- Exportar a múltiples formatos (JSON, Excel)
- CLI interactiva con progreso
- Caché para documentos procesados
