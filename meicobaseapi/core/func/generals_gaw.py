import requests
import json
from requests.auth import HTTPBasicAuth

class GoAnyWhere():
    
    @staticmethod
    def request_with_basic_auth(url, username, password, method="GET", validate=False, data=None, headers=None):
        """
            Hace una petición HTTP con Basic Auth.

            :param url: URL del endpoint
            :param username: Usuario para Basic Auth
            :param password: Contraseña para Basic Auth
            :param method: Método HTTP ('GET', 'POST', etc.)
            :param data: Diccionario o string con body (para POST/PUT)
            :param headers: Diccionario con headers adicionales
            :return: Response como texto
        """
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                auth=HTTPBasicAuth(username, password),
                json=data if isinstance(data, dict) else None,
                data=data if isinstance(data, str) else None,
                headers=headers
            )
            response.raise_for_status()  
            response_dict = json.loads(response.text)
            value= None
            # Acceder a los campos
            if not validate:
                
                payload_id = response_dict['data']['payloadId']
                value = response_dict['data']['submitFormLink']  
                
                if not value or not response_dict['data']:
                    raise Exception("Hubo un error en el Endpoint de GoAnyWhere")
            else:
                
                value = response.text
                
            return value
        except Exception as e:
            raise e


