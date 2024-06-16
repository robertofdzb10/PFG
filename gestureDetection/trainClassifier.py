import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Cargamos los datos y las etiquetas
data_dict = pickle.load(open("./data.pickle", "rb"))

# Mostramos las claves del diccionario para comprobar que se han cargado correctamente
#print(data_dict.keys())
#print(data_dict)

# Convertimos los datos y las etiquetas a arrays de numpy
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Dividimos los datos en datos de entrenamiento y datos de test
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels) # Se escogio un tamaño de test del 20% (Shuffle para que los datos se mezclen, útil para garantizar que los modelos de aprendizaje automático no aprendan patrones erróneos basados en el orden de los datos.)

# Se crea un modelo de clasificación de Random Forest
model = RandomForestClassifier() 
# Se entrena el modelo
model.fit(x_train, y_train)

# Se realizan predicciones con el modelo
y_predict = model.predict(x_test)

# Se calcula la precisión del modelo
accuracy_score = accuracy_score(y_predict, y_test)
# Se muestra la precisión del modelo
print('{}% de los datos de test han sido clasificados correctamente'.format(accuracy_score*100))

