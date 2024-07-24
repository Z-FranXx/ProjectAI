import os
import logging
import json

import numpy
import joblib
from azureml.core.model import Model

 

def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # Please provide your model's folder name if there is one
    model_dir = os.getenv('AZUREML_MODEL_DIR')
    
    # Construye la ruta completa al modelo utilizando la variable de entorno
    model_path = os.path.join(model_dir, '4', 'svd_model.pkl')
    
    # Deserializar el archivo del modelo de vuelta en un modelo sklearn
    model = joblib.load(model_path)  
    
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    logging.info("Init complete")


def run(raw_data):
    print(f"Estos son los datos en raw : {raw_data}\n")
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("model 1: request received")
    logging.info(f"Datos recibidos al ejecutar la funcion de run {raw_data}")
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    result = model.predict(data)
    logging.info("Request processed")
    return result.tolist()