from django.core.management.base import BaseCommand, CommandError
from meicobaseapi.scripts.views.BODEGAS_ZZZ_VIEW import BODEGAS_ZZZ_VIEW

class Command(BaseCommand):
    """Exec command $ python manage.py db_factoy --class <ClassName>"""
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
                BODEGAS_ZZZ_VIEW()
                #seeder de parametros y atributos
            self.stdout.write("Executed Fatory ", ending='\n')
       except KeyError:
        print("El Fatory especificado no existe")
       except Exception as e:
        raise e
        print("Ha ocurrido un error no previsto", type(e).__name__ )