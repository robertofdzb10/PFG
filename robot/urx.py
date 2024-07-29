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

# Función para mover el robot a una configuración
def moveL_a_config(nombre: str) -> None:
    pose = cargar_config(nombre)
    if pose is None:
        print(f"No se encontró la configuración '{nombre}'")
    else:
        rtde_c.moveL(pose, 1.2, 0.25)

# Función para mover el robot a una configuración utilizando otra como punto de Blending #NEW
def moveL_with_blending(blending_point: str) -> None:
    blend_pose = cargar_config(blending_point)
    if blend_pose is None:
        print(f"No se encontró la configuración '{blending_point}'")
    else:
        # Mueve al punto de blending
        rtde_c.moveL(blend_pose, 1.2, 0.25, 0.005)

# Función para coger la pieza correspondiente
def coger_pieza(config):
     
    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "coger", "config": config})
     
    moveL_a_config("config_1")
    moveL_with_blending("config_pre" + config)
    # Abrimos la pinza   
    mover_pinza(35,40.0)
    sleep(2)
    moveL_a_config("config_" + config)
    # Cerramos la pinza
    mover_pinza(0.0, 5.0)
    sleep(2)
    moveL_with_blending("config_pre" + config)
    #moveL_a_config("config_1")


# Función para mover la pieza en la casilla correspondiente
def dejar_pieza(config):
    
    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "dejar", "config": config})
    
    moveL_a_config("config_1")
    moveL_with_blending("config_pre" + config)
    moveL_a_config("config_" + config)
    # Abrimos la pinza   
    mover_pinza(35,40.0)
    sleep(2)
    moveL_with_blending("config_pre" + config)
    # Cerramos la pinza
    mover_pinza(0.0, 5.0)
    sleep(2)
    #moveL_a_config("config_1")

    
def recoger_tablero(): #NEW
    # Recorremos la lista de acciones en orden inverso
    for accion in reversed(acciones_realizadas):
        # Si la acción fue coger una pieza, la dejamos
        if accion["accion"] == "coger":
            dejar_pieza(accion["config"])
        # Si la acción fue dejar una pieza, la cogemos
        elif accion["accion"] == "dejar":
            coger_pieza(accion["config"])
        # Si la acción fue desapilar una pieza, la apilamos de vuelta
        elif accion["accion"] == "desapilar":
            apilar_pieza_de_vuelta(accion["pila"], accion["contador"])
    # Vaciamos la lista de acciones
    acciones_realizadas.clear()


# Función para detectar fuerza sobre el robot #NEW
def monitor_force(force_threshold, first_move):
    while True:
        # Obtenemos la fuerza actual que se le esta aplicando al robot
        force = rtde_r.getActualTCPForce()
        if any(f > force_threshold for f in force):
            print("Fuerza aplicada")
            if first_move:
                print(True)
                return True
            else:
                print(False)
                return False

# Función para desapilar una pieza de una pila y moverla a la posición indicada
def desapilar_pieza(pila, contador):
    origenes = {
        "X": ["preApilarX1", "preApilarX2"],
        "O": ["preApilarO1", "preApilarO2"]
    }

    pila_actual = origenes[pila][0] if contador <= 4 else origenes[pila][1]
    moveL_a_config("config_1")
    # Primero que nada cerramos la pinza
    mover_pinza(0.0, 5.0)
    sleep(2)
    
    moveL_a_config(f"config_{pila_actual}")
    speed = [0, 0, -0.050, 0, 0, 0]
    rtde_c.moveUntilContact(speed)
    # Abrimos la pinza   
    mover_pinza(35,40.0)
    sleep(2)
    # Bajamos un poco en el eje Z
    target = rtde_r.getActualTCPPose()
    target[2] -= 0.025
    rtde_c.moveL(target, 0.25, 0.5, True)
    # Cerramos la pinza
    mover_pinza(0.0, 5.0)
    # Esperamos a que cierre la pinza
    sleep(2)
    # Vuelve a subir para evitar chocarse
    moveL_a_config(f"config_{pila_actual}")

    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "desapilar", "pila": pila, "contador": contador})

    return pila_actual

# Función para apilar una pieza de vuelta
def apilar_pieza_de_vuelta(pila, contador):
    origenes = {
        "X": ["preApilarX1", "preApilarX2"],
        "O": ["preApilarO1", "preApilarO2"]
    }

    pila_actual = origenes[pila][0] if contador <= 4 else origenes[pila][1]
    moveL_a_config("config_1")
    moveL_a_config(f"config_{pila_actual}")
    speed = [0, 0, -0.050, 0, 0, 0]
    rtde_c.moveUntilContact(speed)
    sleep(1)
    mover_pinza(35, 40.0)  # Abre la pinza para dejar la pieza
    sleep(2)
    moveL_a_config(f"config_{pila_actual}")
    mover_pinza(0.0, 5.0)  # Cierra la pinza
    moveL_with_blending(f"config_{pila_actual}")

    # Registramos la acción realizada
    acciones_realizadas.append({"accion": "apilar", "pila": pila, "contador": contador})
