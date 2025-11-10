
import uuid
import base64
from datetime import datetime
from django.core import serializers as django_serializer
from azure.storage.blob import BlobServiceClient
from meicobaseapi.enums.GoAnWhere.gaw_enum import CredencialesAzure

def setActorRequest(request_data, user, update=False):
   
    """
    Funcion que setea el objeto request agregando los campos del usuario de creacion y actualizacion
    :params
    :request: request.data
    """
    request_data = request_data.copy()
    if update:
        if 'created_by' in request_data : request_data.__delitem__('created_by')
        request_data.__setitem__('updated_by', user.id)
        if 'creation_at' in request_data : request_data.__delitem__('creation_at')
        request_data.__setitem__('updated_at',str(datetime.now()))
    else :
        request_data.__setitem__('created_by', user.id)
        request_data.__setitem__('updated_by', user.id)
        if 'creation_at' in request_data : request_data.__delitem__('creation_at')
        if 'updated_at' in request_data : request_data.__delitem__('updated_at')
   
    if 'estado' in request_data : request_data.__delitem__('estado')
   
    return request_data


def formatErrors(errors):
   
    """
    Funcion que formatea los errores proporcionado por los serializadores
    """
    first_error_key =next(iter(errors))
    fisrt_error = errors[first_error_key]
   
    if isinstance(fisrt_error,dict) : custom_message_error=fisrt_error[list(fisrt_error.keys())[0]][0]
    else : custom_message_error=fisrt_error[0]
   
    if custom_message_error == 'Este campo es requerido.':
        custom_message_error = f'El campo {first_error_key} es requerido.'
    if custom_message_error == 'Este campo no puede ser nulo.':
        custom_message_error = f'El campo {first_error_key} es requerido.'
    return custom_message_error


def model_to_dict(model,foreign_keys=None)->dict:
    """Funcion que convierte un modelo en un diccionario"""
    model_formatted = django_serializer.serialize('python', [ model])
    model_formatted = model_formatted[0]
    model_formatted["fields"]['pk']= model_formatted['pk']
    model_formatted["fields"]['model']= model_formatted['model']
    if foreign_keys :
        for field in foreign_keys :
            model_formatted["fields"][field+'_id'] =model_formatted["fields"].pop(field)
    
    return model_formatted['fields']



def upload_to_azure(file_data, blob_name=None, subfolder=""):
    try:
        print("upload_to_azure: ")

        # Procesar el data URI
        info = get_content_info(file_data)
        file_bytes = base64.b64decode(info['content'])
        file_ext = info['file_format']

        # Si no se pasó un nombre personalizado, generamos uno con fecha + UUID
        if not blob_name:
            fecha_hoy = datetime.now().strftime("%Y%m%d")
            blob_name = f"{fecha_hoy}_{uuid.uuid4()}.{file_ext}"
        else:
            # Agregamos la extensión
            blob_name = f"{blob_name}.{file_ext}"

        if subfolder:
            blob_name = f"{subfolder}/{blob_name}"

        # Conexión a Azure
        connection_string = CredencialesAzure.STOREGE_AZURE.value
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "gestorguiasdev"
        container_client = blob_service_client.get_container_client(container_name)

        if not container_client.exists():
            print(f"El contenedor '{container_name}' no existe. Creándolo...")
            blob_service_client.create_container(container_name)

        # Subir archivo
        container_client.upload_blob(
            name=blob_name,
            data=file_bytes,
            overwrite=True
        )

        # URL pública
        url_completa = f"{CredencialesAzure.BASE_URL_AZURE.value}{blob_name}"
        return {
            "url": url_completa,
            "file_name": blob_name,
            "content_type": info['content_type']
        }
    except Exception as e:
        raise Exception(f"Error al subir archivo a Azure: {e}")

    

def get_content_info(data_uri: str = ""):
    try:
        print("entrara a la funcion  get_content_info ")
        for_semicolon = data_uri.split(";")
        for_forward_slash = for_semicolon[0].split("/")
        for_two_points = for_forward_slash[0].split(":")
        for_comma = for_semicolon[1].split(",")
        
        result = {
            "content_type": for_two_points[1],
            "file_format": for_forward_slash[1],
            "content": for_comma[1]
        }
        return result
    except Exception as e:
        raise Exception("Error al procesar el contenido del archivo") from e
    
    