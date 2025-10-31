from rest_framework.response import Response
from rest_framework import status

class APIResponse():
    
    @staticmethod
    def throwEceptionMessage(error:Exception):
        """
        Funcion que permite personalizar el mensaje de validacion y persolaizarlo siempre y cuando se utlize el bloque try catch
        param $error , hace referencia a el error capturado por un catch, dentro de un bloque try catch.
        @return  $custom_message , hace referencia a el mensaje personalalizado que devolvera el api o endpoint.
        """
        try:
            word_message = "Error : "
            message = str(error)
            settings = 'local'

            # Verificamos el entorno
            if settings == 'local' or settings is False:
                return message

            else:
                return "Error interno en el servidor"
        except:
             return "Error interno en el servidor_"
    
    
    def successful(message="", data={},status=status.HTTP_200_OK):
        """
        * Funcion que permite responder de manera exitosa a una solicitud http
        * @param $message , hace referencia a el mensaje personalizado con el cual se le respondera a el host cliente
        * @param $data , hace referencia a el payload o data que se le proporcionara a el host cliente.
        """
        return Response({
        "statusCode": status,
        'success': True,
        'messages': message,
        'data': data,
        })
        
        
    def failed(error:Exception,status=status.HTTP_400_BAD_REQUEST):
        """
        Funcion que permite responder de manera fallida a una solicitud http
        @param $error , hace referencia a el error capturado por un catch, dentro de un bloque try catch.
        """
       
        return Response({
        "statusCode": status,
        'success': False,
        'messages': APIResponse.throwEceptionMessage(error),
        'data': {} ,
        })

   
    def error(message="",  data={},status=status.HTTP_400_BAD_REQUEST):
        return Response({
            'success': False,
            'messages': [message],
            'data': data
        }, status=status)