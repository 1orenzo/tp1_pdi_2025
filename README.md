# TP1 - Procesamiento de Imágenes I (IA 4.4) - UNR 2025

Este repositorio contiene las soluciones para el Trabajo Práctico N° 1 de la materia Procesamiento de Imágenes I, correspondiente a la Tecnicatura Universitaria en Inteligencia Artificial de la Universidad Nacional de Rosario (Año 2025, 2° Semestre).

**Autores:** Bollini Lorenzo, Speranza Emanuel

---

## Contenido del Repositorio

* **`problema1_ecualizacion_histograma.py`**: Script que implementa y analiza la ecualización local del histograma.
* **`problema2_validacion_formulario.py`**: Script que valida automáticamente formularios escaneados según las reglas especificadas.
* **`Formularios/`**: Directorio que contiene las imágenes de los formularios (`formulario_<id>.png`, `formulario_vacio.png`) utilizadas por el Problema 2.
* **`Imagen_con_detalles_escondidos.tif`**: Imagen de entrada utilizada por el Problema 1.
* **`README.md`**: Este archivo.

---

## Problema 1: Ecualización Local del Histograma

Este script aborda la técnica de ecualización local del histograma, diseñada para realzar detalles en imágenes con variaciones locales de contraste.

### Implementación

1.  **Función Principal:** Se define `ecualizacion_local_del_histograma` que toma la imagen en escala de grises y las dimensiones (impares) de la ventana como entrada.
2.  **Manejo de Bordes:** Se utiliza `cv2.copyMakeBorder` con `cv2.BORDER_REPLICATE` para gestionar los píxeles cercanos a los bordes de la imagen, siguiendo la sugerencia del enunciado.
3.  **Proceso Local:** El script itera sobre cada píxel de la imagen original. Para cada píxel, extrae la ventana correspondiente de la imagen con borde y aplica `cv2.equalizeHist` a esa ventana. El valor resultante del píxel central de la ventana ecualizada se asigna a la imagen de salida.
4.  **Análisis:** El script carga la imagen `Imagen_con_detalles_escondidos.tif` y ejecuta la función con diferentes tamaños de ventana (5x5, 25x25, 99x99) para analizar visualmente la influencia de este parámetro en la revelación de detalles, utilizando `matplotlib.pyplot` para mostrar los resultados.

---

## Problema 2: Validación de Formularios

Este script automatiza la validación de formularios escaneados, verificando si el contenido de cada campo cumple con un conjunto de reglas predefinidas. Implementa todos los puntos (A, B, C, D) y sigue las ayudas técnicas del enunciado.

### Implementación

1.  **Detección Automática de Celdas (Ayuda 1):** En lugar de coordenadas fijas, el script utiliza la función `detectar_lineas` para encontrar dinámicamente la estructura de la tabla en cada formulario. Esta función aísla las líneas horizontales y verticales mediante operaciones morfológicas (`cv2.erode`, `cv2.dilate`) y luego aplica la técnica de proyección de píxeles (`np.sum`) y detección de picos (`_encontrar_centro_lineas`).
2.  **Extracción de Contenido (Ayuda 2):** Una vez detectadas las coordenadas, se extraen las regiones de interés (ROIs). La función `extraer_caracteres_y_palabras` analiza cada ROI binarizada usando `cv2.connectedComponentsWithStats`, filtra componentes pequeños por área (`MIN_CHAR_AREA`) y cuenta caracteres (`c`) y palabras (`p`) basándose en el espaciado (`SPACE_THRESHOLD`).
3.  **Validación Estricta (Punto A):** La función `validar_campos` recibe los conteos `(c, p)` y_
