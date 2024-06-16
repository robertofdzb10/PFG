import rtde_receive
import yaml

ROBOT_IP="10.172.21.205"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# Función para registrar la configuración del robot
def registrar_config(nombre: str) -> None:
    try:
        with open("registro_configs","r") as f:
            data = yaml.load(f, yaml.Loader)        
    except:
        data = []
    data.append({nombre:rtde_r.getActualTCPPose()})
    with open("registro_configs","w") as f:
        yaml.dump(data,f)
            
registrar_config("config_33")