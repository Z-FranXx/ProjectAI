from azureml.core import Workspace, Model

# Datos de conexión
subscription_id = 'd1bea4f5-48e7-4a5b-a667-f228cb71d697'
resource_group = 'proyectofinalia'
workspace_name = 'Proyecto-Final-IA'

# Conectar al espacio de trabajo|
ws = Workspace(subscription_id=subscription_id,
                      resource_group=resource_group,
                      workspace_name=workspace_name)

# Registrar el modelo
model = Model.register(workspace=ws,
                       model_path="C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/svd_model.pkl",  # Ruta local del modelo
                       model_name="recom")




from azureml.core import Environment

# Crear el objeto de entorno
env = Environment.from_conda_specification(name='myenv', file_path='C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/conda_dependencies.yml')

# Registrar el entorno
env.register(workspace=ws)


from azureml.core.webservice import AciWebservice
from azureml.core.environment import Environment
from azureml.core.webservice import Webservice
from azureml.core import Workspace, ScriptRunConfig, Environment


# Crear el objeto de entorno
env = Environment.from_conda_specification(name='myenv', file_path='C:/Users/epera/OneDrive/Escritorio/ProjectAI/demo/conda_dependencies.yml')

# Configurar el servicio web
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)


from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies

# Crear un entorno
my_environment = Environment(name="my-environment")
conda_dep = CondaDependencies()

# Agregar las dependencias necesarias
conda_dep.add_pip_package("azureml-core")
conda_dep.add_pip_package("scikit-learn")
conda_dep.add_pip_package("numpy")

# Agregar las dependencias al entorno
my_environment.python.conda_dependencies = conda_dep


from azureml.core.model import InferenceConfig

# Crear la configuración de inferencia
inference_config = InferenceConfig(
    entry_script="score.py",
    environment=my_environment
)

# Desplegar el modelo
service = Model.deploy(
    workspace=ws,
    name="my-service",
    models=[model],
    inference_config=inference_config,
    deployment_config=aci_config,
    overwrite=True
)
# Esperar a que se complete el despliegue
service.wait_for_deployment(show_output=True)

print(f"Service state: {service.state}")
print(f"Scoring URI: {service.scoring_uri}")
