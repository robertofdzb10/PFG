import cv2
import mediapipe as mp

import numpy as np
from collections import deque

import pickle

# Se carga el modelo de clasificación
model_dict = pickle.load(open("./model.p", "rb"))

# Se obtiene el modelo de clasificación
model = model_dict['model']

import mediapipe as mp

# Creamos un objeto de la clase Hands
mp_hands = mp.solutions.hands # Importa funciones para detectar y rastrear manos
mp_drawing = mp.solutions.drawing_utils # Importa funciones para dibujar en la imagen
mp_drawing_styles = mp.solutions.drawing_styles # Importa estilos para dibujar en la imagen, como puntos, líneas, etc.

# Creamos un objeto de la clase Hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Diccionario con las etiquetas de las clases
labels_dict = {0: '0', 1: '1', 2: '2', 3: '3'}

# Historial de gestos
gesture_history = deque(maxlen=10)
sequence = []

# Función para determinar si un gesto se mantiene constante
def is_gesture_stable(gesture, history, threshold=5):
    return history.count(gesture) >= threshold

# Función para detectar gestos #TODO
def detect_gestures(callback):
    # Variables globales
    global sequence
    global gesture_history

    # Se crea un objeto de la clase VideoCapture, que se encarga de capturar el video de la cámara
    cap = cv2.VideoCapture(0)

    # Bucle para capturar frames de la cámara
    while True:
        
        # Creamos una lista auxiliar para guardar los datos de la imagen
        data_aux = []

        # Posiciones de los puntos de las manos
        x_ = []
        y_ = []

        # Se captura un frame de la cámara
        ret, frame = cap.read()

        # Se obtiene el frame de la cámara
        H, W, _ = frame.shape # Se obtiene el alto y ancho del frame (H = alto, w = ancho, se ignora el número de canales de color, _ sirve para ignorar valores que no se necesitan)

        # Convertimos el frame a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesamos el frame, para detectar las manos en la imagen
        results = hands.process(frame_rgb) 

        # Si se detectan manos en la imagen
        if results.multi_hand_landmarks:
            
            # Si se detectan manos en la imagen (Ya que puede haber más de una mano en la imagen)
            for hand_landmarks in results.multi_hand_landmarks:    
                
                # Dibujamos los puntos y las conexiones de las manos en la imagen
                mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # Recorremos todos los puntos de la mano
                for i in range(len(hand_landmarks.landmark)):

                    # Obtenemos las posiciones de los puntos
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    # Guardamos las posiciones de los puntos en la lista auxiliar
                    data_aux.append(x)
                    data_aux.append(y)

                    # Se obtienen las posiciones de los puntos de la mano
                    x_.append(x)
                    y_.append(y)
                
            # Se obtienen las posiciones mínimas y máximas de los puntos de la mano
            x1 = int(min(x_) * W) - 10
            x2 = int(max(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            y2 = int(max(y_) * H) - 10
            
            # Se realiza una predicción con el modelo
            prediction = model.predict([np.asarray(data_aux)])

            # Se obtiene la etiqueta predicha
            predicted_character = labels_dict[int(prediction[0])]

            # Se dibuja un rectángulo y se muestra la etiqueta predicha en el frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character, (x1, y1 -10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 2, cv2.LINE_AA)

            # Añadir el gesto predicho al historial si es un gesto distinto al último gesto o si el historial está vacío
            gesture_history.append(predicted_character)

            # Comprobar si el gesto predicho se mantiene constante
            if is_gesture_stable(predicted_character, gesture_history):

                # Comprobar si el gesto predicho es diferente al último gesto de la secuencia
                if not sequence or (sequence and sequence[-1] != predicted_character):
                    
                    # Mostramos el gesto predicho a la secuencia
                    print(f"Detected gesture: {predicted_character}")

                    # Añadir el gesto predicho a la secuencia
                    sequence.append(predicted_character)
                    print(f"Detected gesture: {predicted_character}")


        # Mostrar el frame
        cv2.imshow('frame', frame)

        # Comprobar si se ha detectado la secuencia "fila-0-columna"
        if len(sequence) == 3 and sequence[1] == '0':
            fila = int(sequence[0])
            columna = int(sequence[2])
            print(f"Insertar ficha en la posición: ({fila}, {columna})")
            callback(fila, columna)
            sequence = []  # Reiniciar la secuencia para la próxima detección
        elif len(sequence) == 3 and sequence[1] != '0':
            # Reiniciar la secuencia si no se detecta la secuencia "fila-0-columna"
            print("Secuencia de gestos reiniciada.")
            sequence = []
        cv2.waitKey(1)

    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()
