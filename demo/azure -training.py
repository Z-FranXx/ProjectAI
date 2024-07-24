from azureml.core import Workspace, Model
from dotenv import load_dotenv
import os

from azureml.core import Environment
from azureml.core.webservice import AciWebservice
from azureml.core.environment import Environment
from azureml.core.webservice import Webservice
from azureml.core import Workspace, ScriptRunConfig, Environment
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies

from azureml.core.model import InferenceConfig

# Datos de conexión
subscription_id = os.getenv('SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
workspace_name = os.getenv('WORKSPACE_NAME')

# Conectar al espacio de trabajo|
ws = Workspace(subscription_id=subscription_id,
                      resource_group=resource_group,
                      workspace_name=workspace_name)

# Registrar el modelo
model = Model.register(workspace=ws,
                       model_path="C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/svd_model.pkl",  # Ruta local del modelo
                       model_name="recom")

# Crear un objeto de un entorno para entrenar el modelo
env = Environment.from_conda_specification(name='myenv', file_path='C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/conda_dependencies.yml')

# Registramos el entorno en el que se subira el modelo para el despliegue
env.register(workspace=ws)

# Crear el objeto de entorno
env = Environment.from_conda_specification(name='myenv', file_path='C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/conda_dependencies.yml')

#configuirar el deploy para el servicion en azure
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)



# Creamos el entorno nuevamente con nuestro nombre de my-environment
my_environment = Environment(name="my-environment")
conda_dep = CondaDependencies()

# Agregar las dependencias necesarias al entorno registrado
conda_dep.add_pip_package("azureml-core")
conda_dep.add_pip_package("scikit-learn")
conda_dep.add_pip_package("numpy")

# agregar otras las dependencias al entorno
my_environment.python.conda_dependencies = conda_dep



# Crear la configuración de inferencia para poder predicir con el modelo mediante el archivo del scoring.py
inference_config = InferenceConfig(
    entry_script="score.py",
    environment=my_environment
)

# Desplegar el modelo dentro de nuestro servicio, le pasamos las instancias necesarias como la inferencia etc
service = Model.deploy(
    workspace=ws,
    name="my-service",
    models=[model],
    inference_config=inference_config,
    deployment_config=aci_config,
    overwrite=True
)

# esperamos a que se complete el despliegue
service.wait_for_deployment(show_output=True)

#Imprimimos mensajes de informacion acerca del despliegue
print(f"Service state: {service.state}")
print(f"Scoring URI: {service.scoring_uri}")
