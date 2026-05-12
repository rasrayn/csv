# PDF a CSV

Esta aplicación convierte un PDF en un CSV extrayendo dos tipos de datos:

1. Texto de cada página.
2. Datos de gráficos detectados en cada página.

Está diseñada para ser fácil de usar y entender, con una estructura modular basada en composición y principios de Clean Architecture.

---

## ¿Cómo funciona?

La app se divide en capas y responsabilidades:

- `main.py`: punto de entrada. Recibe las rutas del PDF y del CSV, arma la aplicación y ejecuta el proceso.
- `csv_app/entities.py`: define los datos que utiliza la aplicación, como `TextBlock`, `GraphPoint` y `ExtractedPage`.
- `csv_app/ports.py`: define los contratos (protocolos) que deben cumplir los componentes técnicos.
- `csv_app/adapters.py`: implementa los adaptadores concretos que trabajan con PDF, imágenes, OCR y CSV.
- `csv_app/use_cases.py`: contiene la lógica principal de extracción y la generación del CSV.
- `csv_app/composition.py`: conecta todos los componentes entre sí.

Con esta organización, cada parte se encarga de una sola responsabilidad y se puede cambiar o mejorar sin alterar el resto.

---

## Requisitos

La app está escrita en Python 3 y usa estas librerías:

- `pdfplumber` para extraer texto del PDF.
- `pdf2image` para convertir páginas PDF en imágenes.
- `pytesseract` para leer texto en imágenes (OCR).
- `opencv-python-headless` para detectar puntos en gráficos.
- `pandas` para generar el archivo CSV.
- `Pillow` para manejar imágenes.

Además, en Windows necesitas instalar Poppler si no está disponible en el sistema.

---

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

El CSV tiene filas de dos tipos:

- `text`: contiene el texto extraído de cada página.
- `graph_point`: contiene los puntos detectados en gráficos dentro de la página.

Cada fila tiene estas columnas:

- `type`: `text` o `graph_point`
- `page`: número de página
- `graph_index`: índice del punto en el gráfico
- `value`: el texto extraído (solo para filas `text`)
- `x`: coordenada X del punto del gráfico
- `y`: coordenada Y del punto del gráfico
- `x_label`: texto del eje X detectado en la imagen
- `y_label`: texto del eje Y detectado en la imagen

---

## Ejemplo

Si el PDF tiene 2 páginas y la primera contiene un gráfico, el CSV puede tener este aspecto:

| type       | page | graph_index | value                    | x     | y     | x_label | y_label |
|------------|------|-------------|--------------------------|-------|-------|---------|---------|
| text       | 1    |             | Texto de la página 1     |       |       |         |         |
| graph_point| 1    | 1           |                          | 152.4 | 98.7  | Tiempo  | Ventas  |
| graph_point| 1    | 2           |                          | 279.7 | 120.3 | Tiempo  | Ventas  |
| text       | 2    |             | Texto de la página 2     |       |       |         |         |

---

## Notas

- La extracción de texto funciona bien con PDFs que contienen texto real. Si el PDF solo tiene imágenes escaneadas, el texto extraído puede ser limitado.
- La detección de gráficos es básica: busca puntos y etiquetas en la imagen. Dependiendo del diseño del gráfico, puede requerir ajustes.
- La app está diseñada para ser extensible: puedes cambiar el adaptador de gráficos o el exportador sin tocar la lógica de uso.

---

## Estructura de archivos

- `main.py`
- `csv_app/__init__.py`
- `csv_app/composition.py`
- `csv_app/entities.py`
- `csv_app/ports.py`
- `csv_app/adapters.py`
- `csv_app/use_cases.py`
- `requirements.txt`

---

## ¿Necesitas más mejoras?

Si quieres, puedo ayudarte a:

- agregar tests automáticos,
- mejorar la detección de gráficos,
- extraer tablas del PDF,
- o generar un CSV con estructura más avanzada.
