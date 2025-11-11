import uuid
from datetime import datetime
from meicobaseapi.core.helpers.utils import upload_to_azure
from meicobaseapi.models import Consignaciones

class ConsignacionesRepository:
    
    def get_all(self):
        try:
            data = Consignaciones.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
    
    
    def upload_file(self , data):
        try:
            consignacion = Consignaciones.objects.create(**data) 
            # Extraer variables
            file_data = data.get('ruta_archivo_soporte')
            numero_guia = data.get('numero_guia')
            numero_planilla = data.get('numero_planilla')
            nombre_archivo = data.get('nombre_archivo')
            date = datetime.now().strftime("%Y%m%d")
            date_time = datetime.now().strftime("%Y-%m-%d")

            numero_consignacion = consignacion.id

            if file_data:
                # Generar el nombre del archivo usando tus variables
                nombre_archivo = f"{date}_{numero_planilla}_{numero_guia}_{numero_consignacion}_{nombre_archivo}_{uuid.uuid4()}"
                upload_result = upload_to_azure(file_data, blob_name=nombre_archivo, subfolder="Consignaciones")
                consignacion.ruta_archivo_soporte = upload_result['file_name']
            
            consignacion.fecha_registro_corta = date_time
            consignacion.fecha_consignacion_corta = date_time
            consignacion.save()  

            return consignacion
        except Exception as e:
            raise e
  
