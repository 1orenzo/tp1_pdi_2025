import cv2
import numpy as np
import os
import csv

# Obtenemos la ruta para guardar la variable
script_dir = os.path.dirname(os.path.abspath(__file__))
CARPETA_FORMS = "Formularios"
IMG_DIR = os.path.join(script_dir, CARPETA_FORMS)

import cv2
import numpy as np
import os
import csv

### configuracion

UMBRAL_BIN = 230
UMBRAL_PICO = 0.25
MIN_CHAR_AREA = 2
SPACE_THRESHOLD = 4
MARGEN = 3
    
### funciones basicas

def encontrar_centros_lineas(arr_bool):
    """Devuelve los centros de los picos detectados (Ayuda 1)."""
    lineas = []
    en_linea = False
    inicio = 0
    for i, val in enumerate(arr_bool):
        if val and not en_linea:
            inicio = i
            en_linea = True
        elif not val and en_linea:
            lineas.append((inicio + i) // 2)
            en_linea = False
    if en_linea:
        lineas.append((inicio + len(arr_bool)) // 2)
    return lineas

def detectar_lineas(img_bin):
    """Detecta líneas horizontales y verticales usando proyecciones (Ayuda 1)."""
    # Aseguramos que las líneas sean blancas sobre fondo negro
    if np.mean(img_bin) > 128:
        _, img_bin = cv2.threshold(img_bin, 128, 255, cv2.THRESH_BINARY_INV)

    kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    lineas_h = cv2.dilate(cv2.erode(img_bin, kernel_h), kernel_h)
    lineas_v = cv2.dilate(cv2.erode(img_bin, kernel_v), kernel_v)
    img_lineas = cv2.add(lineas_h, lineas_v)

    # Proyeccion de pixeles
    sum_rows = np.sum(img_lineas, axis=1)
    sum_cols = np.sum(img_lineas, axis=0)
    th_r = np.max(sum_rows) * UMBRAL_PICO
    th_c = np.max(sum_cols) * UMBRAL_PICO

    filas = encontrar_centros_lineas(sum_rows > th_r)
    cols = encontrar_centros_lineas(sum_cols > th_c)
    return filas, cols

def extraer_caracteres_y_palabras(img_bin):
    """Cuenta caracteres y palabras usando connectedComponents (Ayuda 2)."""
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bin, 8, cv2.CV_32S)
    stats = stats[1:]  # Ignorar fondo
    stats = stats[stats[:, cv2.CC_STAT_AREA] >= MIN_CHAR_AREA]
    c = len(stats)
    if c == 0:
        return 0, 0
    stats = stats[stats[:, cv2.CC_STAT_LEFT].argsort()]
    palabras = 1
    for i in range(1, len(stats)):
        prev = stats[i - 1]
        curr = stats[i]
        gap = curr[cv2.CC_STAT_LEFT] - (prev[cv2.CC_STAT_LEFT] + prev[cv2.CC_STAT_WIDTH])
        if gap > SPACE_THRESHOLD:
            palabras += 1
    return c, palabras

### validacion de campos

def validar_campos(datos):
    """Valida cada campo según el enunciado."""
    r = {}
    c, p = datos["nombre"]
    r["Nombre y Apellido"] = "OK" if (p >= 2 and c <= 25) else "MAL"

    c, p = datos["edad"]
    r["Edad"] = "OK" if ((c == 2 or c == 3) and p == 1) else "MAL"

    c, p = datos["mail"]
    r["Mail"] = "OK" if (p == 1 and 1 <= c <= 25) else "MAL"

    c, p = datos["legajo"]
    r["Legajo"] = "OK" if (c == 8 and p == 1) else "MAL"

    si1, no1 = datos["preg1_si"][0], datos["preg1_no"][0]
    si2, no2 = datos["preg2_si"][0], datos["preg2_no"][0]
    si3, no3 = datos["preg3_si"][0], datos["preg3_no"][0]
    r["Pregunta 1"] = "OK" if ((si1 == 1) ^ (no1 == 1)) else "MAL"
    r["Pregunta 2"] = "OK" if ((si2 == 1) ^ (no2 == 1)) else "MAL"
    r["Pregunta 3"] = "OK" if ((si3 == 1) ^ (no3 == 1)) else "MAL"

    c, p = datos["comentarios"]
    r["Comentarios"] = "OK" if (p >= 1 and c <= 25) else "MAL"

    return r

### procesamiento

archivos = sorted([f for f in os.listdir(IMG_DIR) if f.endswith(".png")])
csv_datos = [["ID", "Nombre y Apellido", "Edad", "Mail", "Legajo", "Pregunta 1", "Pregunta 2", "Pregunta 3", "Comentarios"]]
crops_nombres = []

for archivo in archivos:
    print(f"\nProcesando {archivo}...")
    form_id = archivo.replace("formulario_", "").replace(".png", "")
    img_gray = cv2.imread(os.path.join(IMG_DIR, archivo), cv2.IMREAD_GRAYSCALE)
    _, img_bin = cv2.threshold(img_gray, UMBRAL_BIN, 255, cv2.THRESH_BINARY_INV)

    # Detectamos lineas del formulario
    filas, cols =detectar_lineas(img_bin)
    if len(filas) < 11 or len(cols) < 4:
        print("  No se detectaron todas las líneas. Saltando...")
        continue

    # Mapeo de celdas 
    y = filas; x = cols; m = MARGEN
    rois = {
        "nombre": img_bin[y[1]+m:y[2]-m, x[1]+m:x[3]-m],
        "edad": img_bin[y[2]+m:y[3]-m, x[1]+m:x[3]-m],
        "mail": img_bin[y[3]+m:y[4]-m, x[1]+m:x[3]-m],
        "legajo": img_bin[y[4]+m:y[5]-m, x[1]+m:x[3]-m],
        "preg1_si": img_bin[y[6]+m:y[7]-m, x[1]+m:x[2]-m],
        "preg1_no": img_bin[y[6]+m:y[7]-m, x[2]+m:x[3]-m],
        "preg2_si": img_bin[y[7]+m:y[8]-m, x[1]+m:x[2]-m],
        "preg2_no": img_bin[y[7]+m:y[8]-m, x[2]+m:x[3]-m],
        "preg3_si": img_bin[y[8]+m:y[9]-m, x[1]+m:x[2]-m],
        "preg3_no": img_bin[y[8]+m:y[9]-m, x[2]+m:x[3]-m],
        "comentarios": img_bin[y[9]+m:y[10]-m, x[1]+m:x[3]-m]
    }

    # Extraemos contenido
    datos = {}
    for k, roi in rois.items():
        datos[k] = extraer_caracteres_y_palabras(roi)

    # Validamos
    resultados = validar_campos(datos)
    for campo, valor in resultados.items():
        print(f"  > {campo}: {valor}")

    # Guardamos en el CSV
    fila = [form_id] + [resultados[c] for c in csv_datos[0][1:]]
    csv_datos.append(fila)

    # Guardamos el crop de nombre y validez total
    crop_nombre = img_gray[y[1]+m:y[2]-m, x[1]+m:x[3]-m]
    es_valido = all(v == "OK" for v in resultados.values())
    color = (0, 255, 0) if es_valido else (0, 0, 255)
    crop_color = cv2.cvtColor(crop_nombre, cv2.COLOR_GRAY2BGR)
    crop_borde = cv2.copyMakeBorder(crop_color, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=color)
    crops_nombres.append(crop_borde)

### reportes

# CSV
with open("reporte_formularios.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_datos)
print("\n Archivo CSV generado: reporte_formularios.csv")

# Imagen resumen
if crops_nombres:
    img_final = cv2.vconcat(crops_nombres)
    cv2.imwrite("reporte_nombres.png", img_final)
    print("Imagen resumen generada: reporte_nombres.png")


