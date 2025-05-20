# API de Predicción de Temperatura con AWS Lambda


Sistema serverless para predecir temperatura utilizando:
- Modelo de ML empaquetado en Docker
- Infraestructura AWS (Lambda, S3, ECR, API Gateway)
- Autenticación via API Key

## 📋 Requisitos Técnicos

- Python 3.10.9
- Dependencias exactas:
  ```text
  joblib==1.2.0
  numpy==1.24.4
  scikit-learn==1.1.3
  boto3==1.26.0

## 🛠️ Configuración AWS
Servicios utilizados:

Lambda (Docker)

S3: s3://modelpredicts/modelsRepository/

ECR: Repositorio privado para la imagen

API Gateway: Endpoint REST con API Key


- Variables de entorno:
  ```text
   MODEL_S3_URI=s3://modelpredicts/modelsRepository/modelo_temperatura.pkl

# 🚀 Cómo Usar la API
- Estructura de la solicitud
  ```text
  import requests

  url = "https://smhdxgp506.execute-api.us-east-1.amazonaws.com/prod"
  headers = {
    "x-api-key": "JpFbj5x3uXaVVVP6XJwlz7WzLbbf54Do206KJ8bw",
    "Content-Type": "application/json"
  }

  data = {
    "temperaturas": [22.1, 22.0, ..., 16.2]  # 60 valores
  }

  response = requests.post(url, json=data, headers=headers)
  print(response.json())

- 📊 Ejemplo de Respuesta
  ```text
  {
  "statusCode": 200,
  "body": {
    "prediccion": 15.8,
    "unidad": "Celsius"
  }
  }
