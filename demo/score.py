import os
import logging
import json
import numpy
import joblib
from azureml.core.model import Model

 
#Funcion de init ejecutada al hacer el despliegue
def init():

    global model
    model_dir = os.getenv('AZUREML_MODEL_DIR')
    model_path = os.path.join(model_dir, '4', 'svd_model.pkl')
    model = joblib.load(model_path)  
    model = joblib.load(model_path)
    logging.info("Init complete")

#Esta funcion handlea las solicitudes por POST del modelo para predecir
def run(raw_data):
    print(f"Estos son los datos en raw : {raw_data}\n")
    
    logging.info("model 1: request received")
    logging.info(f"Datos recibidos al ejecutar la funcion de run {raw_data}")
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    result = model.predict(data)
    logging.info("Request processed")
    return result.tolist()