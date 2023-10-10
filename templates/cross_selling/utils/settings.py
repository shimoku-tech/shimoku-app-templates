from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Shimoku Dashboard API credentials
access_token = getenv("SHIMOKU_TOKEN")
universe_id = getenv("UNIVERSE_ID")
workspace_id = getenv("WORKSPACE_ID")

# Workspace settings
workspace_name = "Cross Selling Dashboard"

# Data
data_folder = "data"
data_file = "data_fake_cross_selling"

# Variable types
nominal = ["Localización", "Comercial_Asignado"]
numerical = ["Edad", "Años_Socio"]

# numerical = ['Edad', 'Años_Socio', 'Ingresos', 'Último_Contacto']
