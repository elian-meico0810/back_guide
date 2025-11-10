import os
from enum import Enum

class GawEnums(Enum):
    # Ruta de inforamcion de guias
    GET_INFO_GUIAS = os.getenv("RUTA_INFO_GUIAS")
    
    
class CredencialesGaw(Enum):
    #Usuarios y contraseñas GoAnywhere
    USER_GAW = os.getenv("USER_GAW")
    PASSWORD_GAW = os.getenv("PASSWORD_GAW")
    
    
class CredencialesAzure(Enum):
    #Crenciales Azure
    STOREGE_AZURE = os.getenv("STOREGE_AZURE")
    BASE_URL_AZURE = os.getenv("BASE_URL_AZURE") 