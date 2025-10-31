
from datetime import datetime


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
