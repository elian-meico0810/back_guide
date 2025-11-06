from django.core.management.base import BaseCommand, CommandError
from meicobaseapi.scripts.views.BODEGAS_ZZZ_VIEW import BODEGAS_ZZZ_VIEW
from meicobaseapi.scripts.views.INFO_GUIA_ZZZ_VIEW import INFO_GUIA_ZZZ_VIEW
from meicobaseapi.scripts.tables.crear_tablas_gestion_guias import crear_tablas_gestion_guias
from meicobaseapi.scripts.sp.crear_sp_gestion_guias import crear_sp_gestion_guias

class Command(BaseCommand):
    """Exec command $ python manage.py db_factory --class <ClassName>"""
    help='Corre los scripts en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument('--class', nargs='+', type=str)


    def handle(self, *args, **options):

       try:
            print("Ejecutando Fatory...")
            class_seeder = options.get('class', None)
            if class_seeder is not None:
                globals()[class_seeder[0]]()
                pass
            else:
                # Vistas
                BODEGAS_ZZZ_VIEW()
                INFO_GUIA_ZZZ_VIEW()
                # Tablas 
                crear_tablas_gestion_guias()
                # SP 
                crear_sp_gestion_guias()
                #seeder de parametros y atributos
            self.stdout.write("Executed Fatory ", ending='\n')
       except KeyError:
        print("El Fatory especificado no existe")
       except Exception as e:
        raise e
        print("Ha ocurrido un error no previsto", type(e).__name__ )