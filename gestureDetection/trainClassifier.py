import pickle
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression 

# Cargamos los datos y las etiquetas
data_dict = pickle.load(open("./data.pickle", "rb"))

# Convertimos los datos y las etiquetas a arrays de numpy
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Dividimos los datos en datos de entrenamiento y datos de test (conjunto de validación)
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Función para realizar validación cruzada y ajuste de hiperparámetros
def evaluate_model(model, param_grid):

    # Validación cruzada
    cv_scores = cross_val_score(model, x_train, y_train, cv=5) # cv_scores es un array con los resultados de la validación cruzada
    print(f'Precisión de Validación Cruzada: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}')
    
    # Ajuste de hiperparámetros 
    start_time = time.time()
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
    grid_search.fit(x_train, y_train)
    end_time = time.time()
    hyperparam_search_time = end_time - start_time
    
    best_model = grid_search.best_estimator_
    
    return best_model, hyperparam_search_time, cv_scores.std() # Devolvemos el mejor modelo, el tiempo de búsqueda de hiperparámetros y la desviación estándar de la validación cruzada

# Definir las cuadrículas de parámetros para cada modelo
param_grids = {
    'rf': {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'svm': {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'],
        'gamma': ['scale', 'auto']
    },
    'knn': {
        'n_neighbors': [3, 5, 7],
        'weights': ['uniform', 'distance']
    },
    'lr': {
        'penalty': ['l1', 'l2'],
        'C': [0.1, 1, 10],
        'solver': ['liblinear']
    },
    'gb': {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7]
    }
}

# Lista de modelos a evaluar
models = {
    'Random Forest': (RandomForestClassifier(), param_grids['rf']),
    'SVM': (SVC(), param_grids['svm']),
    'KNN': (KNeighborsClassifier(), param_grids['knn']),
    'Logistic Regression': (LogisticRegression(max_iter=1000), param_grids['lr']),
    'Gradient Boosting': (GradientBoostingClassifier(), param_grids['gb'])
}

# Lista para almacenar la precisión, tiempo de entrenamiento, desviación estándar, si hubo búsqueda de hiperparámetros, el modelo correspondiente y el nombre del modelo
model_results = []

# Evaluar cada modelo
for model_name, (model, param_grid) in models.items():
    print(f'Evaluando {model_name}...')
    
    if param_grid:  # Realizar ajuste de hiperparámetros si param_grid no está vacío
        best_model, hyperparam_search_time, cv_std = evaluate_model(model, param_grid) # Evaluar el modelo y ajustar hiperparámetros 
        hyperparam_search_done = True
    else:
        best_model = model
        start_time = time.time()
        best_model.fit(x_train, y_train)
        end_time = time.time()
        hyperparam_search_time = 0  # No se realiza búsqueda de hiperparámetros
        training_time = end_time - start_time
        cv_std = 0
        hyperparam_search_done = False # No se realiza búsqueda de hiperparámetros
    
    if hyperparam_search_done:  # Si hubo búsqueda de hiperparámetros
        # Tiempo de entrenamiento del modelo final
        start_time = time.time()
        best_model.fit(x_train, y_train)
        end_time = time.time()
        training_time = end_time - start_time
    else:
        # Tiempo de entrenamiento ya calculado
        training_time = end_time - start_time
    
    # Predecir y calcular precisión
    y_predict = best_model.predict(x_test)
    accuracy = accuracy_score(y_test, y_predict)
    
    # Guardar los resultados en la lista
    model_results.append((accuracy, training_time, cv_std, hyperparam_search_done, best_model, model_name))
    
    # Imprimir resultados
    print(f'{model_name}: {accuracy*100:.2f}% de los datos de test han sido clasificados correctamente.')
    print(f'Tiempo de búsqueda de hiperparámetros: {hyperparam_search_time:.2f} segundos')
    print(f'Tiempo de entrenamiento: {training_time:.2f} segundos\n')

# Encontrar el mejor modelo basado en precisión, tiempo de entrenamiento, desviación estándar y si hubo búsqueda de hiperparámetros
best_model_info = min(
    model_results, # Iteramos sobre los resultados de los modelos
    key=lambda item: (-item[0], not item[3], item[1], item[2]) # Se selecciona el elemento con el valor máximo en la posición 0 (precisión), mínimo en la posición 3 (si hubo búsqueda de hiperparámetros), máximo en la posición 1 (tiempo de entrenamiento) y máximo en la posición 2 (desviación estándar)
)
best_model = best_model_info[4] # Una vez encontrado el mejor modelo, obtenemos el modelo en sí
best_model_name = best_model_info[5] # Obtenemos el nombre del mejor modelo

# Guardar el mejor modelo en un archivo
with open('model.p', 'wb') as f:
    pickle.dump(best_model, f)

print(f"El mejor modelo ({best_model_name}) ha sido guardado en 'model.p'")
