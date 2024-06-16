import mediapipe as mp
import cv2
import os
import matplotlib.pyplot as plt
import pickle

# Creamos un objeto de la clase Hands
mp_hands = mp.solutions.hands # Importa funciones para detectar y rastrear manos
mp_drawing = mp.solutions.drawing_utils # Importa funciones para dibujar en la imagen
mp_drawing_styles = mp.solutions.drawing_styles # Importa estilos para dibujar en la imagen, como puntos, líneas, etc.

# Creamos un objeto de la clase Hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Dirección de los datos
DATA_DIR = './data' 
data = [] # Datos de las imágenes, posiciones de los puntos de las manos
labels = [] # Etiquetas de las imágenes

# Recorremos todas las carpetas de la dirección de los datos
for dir_ in os.listdir(DATA_DIR):

    # Recorremos la primera imagen de cada carpeta
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):  # Cuando solo queramos mostrar una [:1]:
        
        # Creamos una lista auxiliar para guardar los datos de la imagen
        data_aux = []
        
        # Leemos la imagen
        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))

        # Convertimos la imagen a RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Procesamos la imagen, para detectar las manos en la imagen
        results = hands.process(img_rgb) 

        # Si se detectan manos en la imagen
        if results.multi_hand_landmarks:

            # Si se detectan manos en la imagen (Ya que puede haber más de una mano en la imagen)
            for hand_landmarks in results.multi_hand_landmarks:    

                # Dibujamos los puntos y las conexiones de las manos en la imagen
                mp_drawing.draw_landmarks(
                    img_rgb, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # Recorremos todos los puntos de la mano
                for i in range(len(hand_landmarks.landmark)):

                    # Mostramos la posición de cada punto
                    print(hand_landmarks.landmark[i])

                    # Obtenemos las posiciones de los puntos
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    # Guardamos las posiciones de los puntos en la lista auxiliar
                    data_aux.append(x)
                    data_aux.append(y)

            # Guardamos la lista auxiliar en la lista de datos, la lista contendrá las posiciones de los puntos de la mano
            data.append(data_aux)
            # Guardamos la etiqueta de la imagen, correspondiente a la carpeta en la que se encuentra, que es el gesto que se está realizando
            labels.append(dir_)
                

        # Creamos una figura
        plt.figure()
        # Mostramos la imagen
        plt.imshow(img_rgb)

# Mostramos la figura
# plt.show()

# Guardamos los datos y las etiquetas en un archivo pickle
f = open('data.pickle', 'wb') # Se abre el archivo en modo de escritura binaria, borrando el contenido del archivo si ya existe
pickle.dump({'data': data, 'labels': labels}, f) # Guardamos los datos y las etiquetas en el archivo
f.close() # Cerramos el archivo