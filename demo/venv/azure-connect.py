import azureml.core
import pkg_resources
from azureml.core import Workspace, Dataset

# Datos de conexión
subscription_id = 'd1bea4f5-48e7-4a5b-a667-f228cb71d697'
resource_group = 'proyectofinalia'
workspace_name = 'Proyecto-Final-IA'

# Conectar al espacio de trabajo
workspace = Workspace(subscription_id=subscription_id,
                      resource_group=resource_group,
                      workspace_name=workspace_name)



# Cargar el primer dataset
dataset1 = Dataset.Tabular.from_delimited_files(path=[('https://proyectofinali2203117751.blob.core.windows.net/azureml-blobstore-f02ac145-b36e-49b4-b453-0870afb17383/UI/2024-07-22_031035_UTC/Caribbean-Ratings.csv')])
df1 = dataset1.to_pandas_dataframe()

# Cargar el segundo dataset
dataset2 = Dataset.Tabular.from_delimited_files(path=[('https://proyectofinali2203117751.blob.core.windows.net/azureml-blobstore-f02ac145-b36e-49b4-b453-0870afb17383/UI/2024-07-21_231445_UTC/Netflix_Dataset_Movie.csv')])
df2 = dataset2.to_pandas_dataframe()

