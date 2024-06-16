import os
import cv2

# Creamos el directorio de datos
DATA_DIR = './data'

# Si no existe el directorio, lo creamos
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Número de clases
number_of_classes = 4
# Tamaño del dataset
dataset_size = 1000

# Inicializamos la cámara
cap = cv2.VideoCapture(0)

# Recorremos todas las clases
for j in range(number_of_classes):
    # Creamos el directorio de la clase si no existe
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    # Mostramos un mensaje por pantalla
    print('Collecting data for class {}'.format(j))

    # Esperamos a que el usuario pulse la tecla 'q' para empezar a capturar imágenes
    while True:
        # Capturamos un frame de la cámara
        ret, frame = cap.read()
        # Mostramos el mensaje por pantalla para que el usuario sepa que tiene que hacer
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        # Mostramos el frame
        cv2.imshow('frame', frame)
        # Si el usuario pulsa la tecla 'q' salimos del bucle
        if cv2.waitKey(25) == ord('q'):
            break

    # Capturamos las imágenes
    counter = 0
    # Mientras no se haya capturado el número de imágenes deseado
    while counter < dataset_size:
        # Capturamos un frame de la cámara
        ret, frame = cap.read()
        # Mostramos el frame
        cv2.imshow('frame', frame)
        # Esperamos 25ms
        cv2.waitKey(25)
        # Guardamos la imagen en el directorio correspondiente
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        # Incrementamos el contador
        counter += 1

# Liberamos la cámara
cap.release()
# Cerramos todas las ventanas
cv2.destroyAllWindows()
