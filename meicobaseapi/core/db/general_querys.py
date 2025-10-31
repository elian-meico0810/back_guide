from django.db import connection,connections
from django.core.management.color import no_style
class CDB:

    def __init__(self,):
        pass

    def truncate(table):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(table))
    
    def restart_sequence(models):
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), models)
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

    def row(sql,params,connection='default'):
        try:
            with connections[connection].cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()
            return results
        
        except Exception as e:
            if str(e) == 'no results to fetch':
                return[]
            else:
                raise e