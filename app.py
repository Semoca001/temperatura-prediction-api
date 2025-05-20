import os
import boto3
from predictor import predecir_temperatura, set_model
import joblib
import tempfile

def load_model_from_s3():
    s3_uri = os.environ['MODEL_S3_URI']
    if not s3_uri.startswith('s3://'):
        raise ValueError("MODEL_S3_URI debe comenzar con s3://")
    
    bucket, key = s3_uri[5:].split('/', 1)
    
    s3 = boto3.client('s3')
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        s3.download_fileobj(bucket, key, tmp_file)
        tmp_file.flush()
        model = joblib.load(tmp_file.name)
    
    return model

# Cargar el modelo y configurarlo en predictor.py
modelo = load_model_from_s3()
set_model(modelo)  # Inyectar el modelo cargado

def lambda_handler(event, context):
    try:
        ultimas_60_temp = event.get('temperaturas', [])
        
        if len(ultimas_60_temp) != 60:
            return {
                'statusCode': 400,
                'body': 'Error: Se requieren exactamente 60 valores de temperatura'
            }
        
        prediccion = predecir_temperatura(ultimas_60_temp)
        
        return {
            'statusCode': 200,
            'body': {
                'prediccion': prediccion,
                'unidad': 'Celsius'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }