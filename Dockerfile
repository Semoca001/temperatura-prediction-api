FROM public.ecr.aws/lambda/python:3.10

# Instalar dependencias del sistema si las hay
# RUN yum -y install ... 

# Copiar los archivos necesarios
COPY predictor.py ./
COPY app.py ./
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install -r requirements.txt

# Establecer la variable de entorno para la ubicación del modelo
ENV MODEL_S3_URI=s3://modelpredicts/modelsRepository/modelo_temperatura.pkl

# Comando por defecto para Lambda
CMD ["app.lambda_handler"]