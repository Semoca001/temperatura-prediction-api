# API de Predicción de Temperatura con AWS Lambda

🎓 **Cloud Computing, Software (AWS + IoT + AI)**  
📚 **Desarrollado por:** Sebastian Morea Cañon 

## 📝 Descripción del Proyecto

Sistema serverless para predicción de temperatura basado en series temporales. Este proyecto forma parte de la actividad de **Cloud Computing** donde se implementó la dockerización y despliegue en AWS de un modelo de Machine Learning pre-entrenado.

### 🎯 Alcance del Trabajo Realizado
- ✅ **Dockerización** del modelo pre-entrenado proporcionado
- ✅ **Adaptación** de función básica para entorno AWS Lambda  
- ✅ **Configuración** de infraestructura serverless en AWS
- ✅ **Implementación** de API REST con autenticación
- ✅ **Despliegue** en producción con monitoreo

## 🏗️ Arquitectura

```
Cliente → API Gateway → AWS Lambda (Docker) → Modelo ML → S3
```

**Tecnologías utilizadas:**
- **AWS Lambda** (Container Image)
- **Amazon S3** (almacenamiento de modelo)
- **Amazon ECR** (registro de contenedores)
- **API Gateway** (endpoint REST)
- **scikit-learn** (framework del modelo)

## 📋 Especificaciones Técnicas

### Modelo de Machine Learning
| Característica | Valor |
|----------------|-------|
| **Framework** | scikit-learn 1.1.3 |
| **Tipo** | Regresión para series temporales |
| **Entrada** | 60 valores de temperatura consecutivos |
| **Salida** | Predicción para 1 hora futura |
| **Unidad** | Celsius |
| **Precisión** | 2 decimales |

### Configuración AWS
| Servicio | Configuración |
|----------|---------------|
| **Python Runtime** | 3.10.9 |
| **Lambda Memory** | 1024 MB |
| **Lambda Timeout** | 60 segundos |
| **Container Type** | Docker Image |

## 🛠️ Dependencias y Configuración

### requirements.txt
```text
boto3==1.26.0
joblib==1.2.0
numpy==1.24.4
pandas==1.5.3
python-dateutil==2.9.0.post0
pytz==2025.2
scikit-learn==1.1.3
scipy==1.10.1
six==1.17.0
threadpoolctl==3.6.0
```

### Variables de Entorno AWS
```bash
MODEL_S3_URI=s3://modelpredicts/modelsRepository/modelo_temperatura.pkl
```

### Recursos AWS Configurados
- **Endpoint API:** `https://smhdxgp506.execute-api.us-east-1.amazonaws.com/prod`
- **Repositorio ECR:** `824867646208.dkr.ecr.us-east-1.amazonaws.com/juancastro/temperatura-predict-v3`
- **Bucket S3:** `s3://modelpredicts/modelsRepository/`
- **API Key:** `JpFbj5x3uXaVVVP6XJwlz7WzLbbf54Do206KJ8bw`

## 🚀 Cómo Usar la API

### Estructura de Request
```json
{
  "temperaturas": [
    22.1, 22.0, 21.9, 21.8, 21.7,
    // ... exactamente 60 valores consecutivos
    16.5, 16.3, 16.2
  ]
}
```

### Headers Requeridos
```http
Content-Type: application/json
x-api-key: JpFbj5x3uXaVVVP6XJwlz7WzLbbf54Do206KJ8bw
```

### Ejemplo con Python
```python
import requests

# Configuración del endpoint
url = "https://smhdxgp506.execute-api.us-east-1.amazonaws.com/prod"
headers = {
    "x-api-key": "JpFbj5x3uXaVVVP6XJwlz7WzLbbf54Do206KJ8bw",
    "Content-Type": "application/json"
}

# Datos de ejemplo (60 valores de temperatura)
data = {
    "temperaturas": [
        22.1, 22.0, 21.9, 21.8, 21.7, 21.6, 21.5, 21.4, 21.3, 21.2,
        21.1, 21.0, 20.9, 20.8, 20.7, 20.6, 20.5, 20.4, 20.3, 20.2,
        20.1, 20.0, 19.9, 19.8, 19.7, 19.6, 19.5, 19.4, 19.3, 19.2,
        19.1, 19.0, 18.9, 18.8, 18.7, 18.6, 18.5, 18.4, 18.3, 18.2,
        18.1, 18.0, 17.9, 17.8, 17.7, 17.6, 17.5, 17.4, 17.3, 17.2,
        17.1, 17.0, 16.9, 16.8, 16.7, 16.6, 16.5, 16.4, 16.3, 16.2
    ]
}

# Realizar petición
response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Predicción: {result['body']['prediccion']}°C")
```

### Ejemplo con cURL
```bash
curl -X POST \
  https://smhdxgp506.execute-api.us-east-1.amazonaws.com/prod \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: JpFbj5x3uXaVVVP6XJwlz7WzLbbf54Do206KJ8bw' \
  -d '{
    "temperaturas": [22.1, 22.0, 21.9, /* ... 57 valores más ... */, 16.2]
  }'
```

## 📊 Respuestas de la API

### Respuesta Exitosa (200)
```json
{
  "statusCode": 200,
  "body": {
    "prediccion": 15.85,
    "unidad": "Celsius"
  }
}
```

### Respuesta de Error (400)
```json
{
  "statusCode": 400,
  "body": "Error: Se requieren exactamente 60 valores de temperatura"
}
```

### Respuesta de Error (500)
```json
{
  "statusCode": 500,
  "body": "Error interno del servidor"
}
```

## 🐳 Implementación Docker

### Dockerfile
```dockerfile
FROM public.ecr.aws/lambda/python:3.10

# Copiar archivos del proyecto
COPY predictor.py ./
COPY app.py ./
COPY requirements.txt ./

# Instalar dependencias
RUN pip install -r requirements.txt

# Configurar variable de entorno
ENV MODEL_S3_URI=s3://modelpredicts/modelsRepository/modelo_temperatura.pkl

# Definir handler de Lambda
CMD ["app.lambda_handler"]
```

### Comandos de Build y Deploy
```bash
# Build de la imagen
docker build -t temperatura-predict .

# Tag para ECR
docker tag temperatura-predict:latest 824867646208.dkr.ecr.us-east-1.amazonaws.com/juancastro/temperatura-predict-v3:latest

# Push a ECR
docker push 824867646208.dkr.ecr.us-east-1.amazonaws.com/juancastro/temperatura-predict-v3:latest
```

## 📈 Monitoreo y Logs

### CloudWatch Metrics
- **Invocaciones por minuto**
- **Duración de ejecución** 
- **Errores y timeouts**
- **Uso de memoria**

### Logs Disponibles
```bash
# Ver logs de Lambda
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/temperatura-predict"
```

## 🔧 Troubleshooting

### Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `403 Forbidden` | API Key incorrecta | Verificar header `x-api-key` |
| `400 Bad Request` | Datos inválidos | Enviar exactamente 60 valores |
| `500 Internal Error` | Error de modelo | Revisar logs CloudWatch |
| `Timeout` | Cold start | Esperar y reintentar |

### Validación de Datos
```python
def validar_entrada(temperaturas):
    if not isinstance(temperaturas, list):
        return False, "Debe ser una lista"
    
    if len(temperaturas) != 60:
        return False, "Se requieren exactamente 60 valores"
    
    if not all(isinstance(temp, (int, float)) for temp in temperaturas):
        return False, "Todos los valores deben ser numéricos"
    
    return True, "Válido"
```
