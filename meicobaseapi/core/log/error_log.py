import traceback
from meicobaseapi.models import ErrorLog

class DjangoLogs():
    
    def log_error(request, exception, funcion=None):
        try:
            log = ErrorLog.objects.create(
                RequestData=request.path if request else None,
                Funcion=funcion,
                ErrorTipo=type(exception).__name__,
                Mensaje=str(exception),
                Stacktrace=traceback.format_exc()
            )
            
            log.Consecutivo = log.id
            log.save()
        
            return log
        except Exception as e:
            raise e