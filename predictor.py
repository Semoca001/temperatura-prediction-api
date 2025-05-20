import numpy as np

# Variable para almacenar el modelo
_modelo = None

def set_model(modelo_externo):
    global _modelo
    _modelo = modelo_externo

def predecir_temperatura(ultimas_60_temp):
    """
    Recibe una lista o array con 60 temperaturas recientes (últimos 60 minutos),
    y devuelve la predicción de temperatura para dentro de 1 hora.
    """
    if _modelo is None:
        raise ValueError("El modelo no ha sido cargado")
    
    if len(ultimas_60_temp) != 60:
        raise ValueError("La lista debe contener exactamente 60 valores de temperatura.")

    entrada = np.array(ultimas_60_temp).reshape(1, -1)
    prediccion = _modelo.predict(entrada)[0]
    return round(prediccion, 2)