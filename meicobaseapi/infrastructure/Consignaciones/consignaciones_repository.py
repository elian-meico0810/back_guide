import uuid
from datetime import datetime
from django.utils import timezone
from meicobaseapi.core.helpers.utils import upload_to_azure
from meicobaseapi.models import Consignaciones

class ConsignacionesRepository:
    
    
    def get_all(self):
        try:
            data = Consignaciones.objects.filter(Estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    
    
    def upload_file(self , data):
        try:
            consignacion = Consignaciones.objects.create(**data) 
            # Extraer variables
            file_data = data.get('RutaArchivoSoporte')
            numero_guia = data.get('NumeroGuia')
            numero_planilla = data.get('NumeroPlanilla')
            nombre_archivo = data.get('NombreArchivo')
            date = datetime.now().strftime("%Y%m%d")
            date_time = datetime.now().strftime("%Y-%m-%d")

            numero_consignacion = consignacion.id

            if file_data:
                # Generar el nombre del archivo usando tus variables
                nombre_archivo = f"{date}_{numero_planilla}_{numero_guia}_{numero_consignacion}_{nombre_archivo}_{uuid.uuid4()}"
                upload_result = upload_to_azure(file_data, blob_name=nombre_archivo, subfolder="Consignaciones")
                consignacion.RutaArchivoSoporte = upload_result['file_name']
      
            consignacion.FechaRegistroCorta = date_time
            consignacion.FechaConsignacionCorta = date_time
            consignacion.save()  

            return consignacion
        except Exception as e:
            raise e
        
        
    def group_parameer(self):
        """
            - Funcion que agrupa paramtros para llenar 
            los filtros del modulo de consignaciones 
        """
        try:
            data = Consignaciones.objects.filter(Estado=True).values(
                'FechaConsignacionCorta',
                'ValorConsignacion',
                'TipoConsignacion',
                'NombreArchivo'
            ).distinct()

            return data           
        except Exception as e:
            raise e
        
        
    def delete(self, id: int):
        try:
            consignacion = Consignaciones.objects.filter(id=id).first()
            if not consignacion:
                raise Exception("El registro no existe.")
            
            # Registrar información de eliminación
            
            # consignacion.deleted_by = user
            consignacion.DeletedAt = timezone.now()
            consignacion.save()
    
            # Eliminar el registro (opcional, si deseas borrado físico)
            consignacion.delete()

            return True
        except Exception as e:
            raise e
  
