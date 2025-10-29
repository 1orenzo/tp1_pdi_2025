# TP1 – Procesamiento de Imágenes I (IA 4.4) – UNR 2025

Este repositorio contiene las soluciones del **Trabajo Práctico N.º 1** de la materia **Procesamiento de Imágenes I**, de la **Tecnicatura Universitaria en Inteligencia Artificial** (UNR, Año 2025).

**Grupo 9:** Lorenzo Bollini y Emanuel Speranza

---

## Contenido del repositorio

- **`problema1_ecualizacion_histograma.py`**  
  Programa que mejora el contraste de una imagen usando la técnica de *ecualización local del histograma*.

- **`problema2_validacion_formulario.py`**  
  Programa que revisa automáticamente formularios escaneados y verifica si los campos están correctamente completados.

- **`Formularios/`**  
  Carpeta con las imágenes de los formularios usados en el Problema 2.

- **`Imagen_con_detalles_escondidos.tif`**  
  Imagen usada para probar el Problema 1.

- **`README.md`**  
  Este archivo con la explicación del trabajo.

---

## Problema 1: Ecualización Local del Histograma

Este ejercicio aplica una técnica para **mejorar los detalles de una imagen** en zonas donde el contraste cambia mucho.  
La idea es aplicar una ecualización del histograma en pequeñas partes (ventanas) de la imagen, en lugar de hacerlo sobre toda la imagen completa.

### Explicación paso a paso

1. **Lectura y preparación de la imagen:**  
   Se carga una imagen en escala de grises (blanco y negro).

2. **Manejo de los bordes:**  
   Para evitar errores al trabajar con píxeles del borde, se agrega un borde artificial usando `cv2.copyMakeBorder`.

3. **Ecualización local:**  
   El programa recorre la imagen píxel por píxel.  
   Para cada píxel, toma una ventana a su alrededor y aplica `cv2.equalizeHist`, que mejora el contraste de esa pequeña zona.

4. **Pruebas con diferentes tamaños de ventana:**  
   Se prueba con ventanas de 5×5, 25×25 y 99×99 para ver cómo cambia el resultado.

5. **Visualización:**  
   Se muestran las imágenes resultantes con `matplotlib.pyplot` para comparar los efectos.

---

## Problema 2: Validación de Formularios

Este ejercicio crea un sistema para **revisar formularios escaneados automáticamente**, sin tener que hacerlo a mano.  
Cada formulario tiene casillas (celdas) con texto escrito a mano, y el programa revisa si están completas según ciertas reglas.

### Explicación paso a paso

1. **Detección de las líneas del formulario:**  
   El programa encuentra automáticamente las líneas que forman la tabla del formulario.  
   Para eso usa funciones de OpenCV como `cv2.erode` y `cv2.dilate`, que ayudan a resaltar las líneas horizontales y verticales.

2. **Extracción del contenido de cada celda:**  
   Se recorta cada parte del formulario donde hay texto.  
   Luego, usando `cv2.connectedComponentsWithStats`, se cuentan los caracteres y palabras encontrados.

3. **Validación de campos:**  
   Con los datos anteriores, se aplican las reglas del enunciado (a–f).  
   El resultado puede ser “OK” si cumple con las condiciones o “MAL” si no lo hace.

4. **Generación de reportes:**  
   - Se analizan todos los archivos que empiecen con `formulario_`.  
   - Se muestran los resultados por consola.  
   - Se guarda un archivo `reporte_simplificado.csv` con todos los resultados.  
   - También se crea una imagen `reporte_simplificado.png` que muestra un recorte del campo **“Nombre y Apellido”** con un borde verde si está OK o rojo si está MAL.

---

## Requisitos

Para ejecutar los programas se necesita tener instalado:

- **Python 3.x**  
- **OpenCV** (`opencv-python`)  
- **NumPy** (`numpy`)  
- **Matplotlib** (`matplotlib`) *(solo para el Problema 1)*  
- **os** y **csv** (módulos incluidos en Python por defecto)

### Instalación de librerías

Desde la terminal, ejecutar:

```bash
pip install opencv-python numpy matplotlib
