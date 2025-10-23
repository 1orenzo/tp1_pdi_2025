
import numpy as np
import cv2 
import matplotlib.pyplot as plt
import os 

def ecualizacion_local_del_histograma(imagen, ancho_ventana, alto_ventana):
    """
        Ecualización local del histograma
        Aplicamos la ecualización del histograma a una imagen en escala de rises.
        
        args: imagen(np array), el ancho y el alto de la ventana de procesamiento
        returns: la imagen(np array) con el histograma con el ecualizado local
    """
    if ancho_ventana % 2 == 0 or alto_ventana % 2 == 0: #verificamos que el ancho y el alto sean impares
        raise ValueError("Las dimensiones deben ser impares")
    
    alto_img, ancho_img = imagen.shape

    # Calculamos el padding necesario para los bordes
    pad_vertical = alto_ventana // 2
    pad_horizontal = ancho_ventana // 2

    # Agregamos borde con cv2.copyMakeBorder(), replicamos los valores
    imagen_con_borde = cv2.copyMakeBorder(
        imagen,
        pad_vertical,
        pad_vertical,
        pad_horizontal,
        pad_horizontal,
        cv2.BORDER_REPLICATE
    )
    

    # Crear una imagen vacia para luego almacenar el resultado
    imagen_salida = np.zeros_like(imagen)

    # Con un for recorremos cada pixel original con el fin de procesarlo
    for y in range(alto_img):
        for x in range(ancho_img):
            # Las coordenadas en la imagen con borde corresponden al centro de la ventana
            # Sumamos el padding para compensar el borde que se agrego
            centro_y = y + pad_vertical
            centro_x = x + pad_horizontal

            ventana = imagen_con_borde[
                centro_y - pad_vertical : centro_y + pad_vertical + 1,
                centro_x - pad_horizontal : centro_x +pad_horizontal + 1
                ]
            
            ventana_ecualizada = cv2.equalizeHist(ventana)

            imagen_salida[y, x] = ventana_ecualizada[pad_vertical, pad_horizontal]

    return imagen_salida



##### pruebas
nombre_archivo = "Imagen_con_detalles_escondidos.tif"
# Obtenemos y guardamos en una variable la ruta de la imagen
directorio_script = os.path.dirname(os.path.abspath(__file__))
archivo = os.path.join(directorio_script, nombre_archivo)

imagen_original = cv2.imread(archivo, cv2.IMREAD_GRAYSCALE)
if imagen_original is None:
    raise FileNotFoundError(f'El archivo no se ha encontrado')

prueba_1 = ecualizacion_local_del_histograma(imagen_original, 5, 5)
prueba_2 = ecualizacion_local_del_histograma(imagen_original, 25, 25)
prueba_3 = ecualizacion_local_del_histograma(imagen_original, 99, 99)

# Visualizamos las 3 pruebas
fig, axes = plt.subplots(1, 4, figsize=(20,5))

titulos = ['Imagen Original', 'Ventana 5x5', 'Ventana 25x25', 'Ventana 99x99']
imagenes = [imagen_original, prueba_1, prueba_2, prueba_3]

for i, (imagen, titulo) in enumerate(zip(imagenes, titulos)):
    axes[i].imshow(imagen, cmap='gray')
    axes[i].set_title(titulo)
    axes[i].axis('off')

plt.tight_layout()
plt.suptitle('Resultados de la Ecualizacion Local del Histograma', fontsize = 16, y=1.02)
plt.show()
