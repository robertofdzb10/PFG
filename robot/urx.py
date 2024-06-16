import rtde_receive
import rtde_control
from time import sleep
from math import pi 
from typing import Any, Dict, List, Tuple
from subprocess import getstatusoutput
import yaml

ROBOT_IP="10.172.21.205"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)

# Inicializamos la lista que almacenará las acciones realizadas
acciones_realizadas = []

# Función para mover la pinza
def mover_pinza(width: float,force: float) -> Tuple[int, str]:
    if width < 0.0 or width > 100.0:
        return ()
    
    return getstatusoutput(f"xmlrpc http://{ROBOT_IP}:41414 rg_grip i/0 d/{width} d/{force}")

# Función para leer la configuración del robot
def leer_config() -> List[Dict[str, Any]]:
    try:
        with open("registro_configs", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except Exception as e:
        print(f"Error al leer el archivo de configuración: {e}")
        return []
          
# Función para cargar una configuración del robot
def cargar_config(nombre: str):
    configs = leer_config()
    for config in configs:
        if nombre in config:
            return config[nombre]
    return None

# Función para mover el robot a una configuración
def moveL_a_config(nombre: str) -> None:
    pose = cargar_config(nombre)
    if pose is None:
        print(f"No se encontró la configuración '{nombre}'")
    else:
        rtde_c.moveL(pose, 1.2, 0.25)

# Función para coger la pieza correspondiente
def coger_pieza(config):
    
    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "coger", "config": config})
    
    # Nos movemos a la posición inicial
    moveL_a_config("config_1")

    # Nos colocaamos encima de la pieza
    moveL_a_config("config_pre" + config)

    # Abrimos la pinza   
    mover_pinza(35,40.0)
    sleep(2)

    # Bajamos a la posición de la pieza
    moveL_a_config("config_" + config)

    # Cerramos la pinza
    mover_pinza(0.0, 5.0)
    sleep(2)

    # Nos volvemos a colocar encima de la pieza
    moveL_a_config("config_pre" + config)


# Función para mover la pieza en la casilla correspondiente
def dejar_pieza(config):
    
    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "dejar", "config": config})
    
    # Nos movemos a la posición inicial
    moveL_a_config("config_1")

    # Nos colocamos encima de la casilla correspondiente
    moveL_a_config("config_pre" + config)

    # Bajamos a la posición de la casilla
    moveL_a_config("config_" + config)

    # Abrimos la pinza   
    mover_pinza(35,40.0)
    sleep(2)

    # Nos volvemos a colocar encima de la casilla
    moveL_a_config("config_pre" + config)

    # Cerramos la pinza
    mover_pinza(0.0, 5.0)
    sleep(2)


# Función para restablecer el tablero
def recoger_tablero():

    # Recorremos la lista de acciones en orden inverso
    for accion in reversed(acciones_realizadas):

        # Si la acción fue coger una pieza, la dejamos
        if accion["accion"] == "coger":
            dejar_pieza(accion["config"])

        # Si la acción fue dejar una pieza, la cogemos
        elif accion["accion"] == "dejar":
            coger_pieza(accion["config"])
            
    # Vaciamos la lista de acciones
    acciones_realizadas.clear()