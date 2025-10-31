import os
import importlib
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    """
    Ejecuta:
        python manage.py db_tables              → genera SQL para TODOS los modelos
        python manage.py db_tables --class X Y  → genera SQL solo para esos modelos
    """

    help = "Genera scripts CREATE TABLE desde los modelos definidos en meicobaseapi.models"

    def add_arguments(self, parser):
        parser.add_argument('--class', nargs='+', type=str, help="Nombre(s) de los modelos Django")

    def handle(self, *args, **options):
        try:
            print(" Generando script SQL desde meicobaseapi.models...")

            # Importar el módulo que contiene todos los modelos
            models_module = importlib.import_module("meicobaseapi.models")

            # Crear carpeta de salida
            output_dir = os.path.join(os.getcwd(), "generated_sql")
            os.makedirs(output_dir, exist_ok=True)

            # Si no se especifican modelos → procesar todos
            model_names = options.get('class', None)
            if not model_names:
                model_names = [
                    name for name, obj in models_module.__dict__.items()
                    if isinstance(obj, type) and issubclass(obj, models.Model) and not obj._meta.abstract
                ]
                print(f" No se especificó modelo. Se generarán todos: {', '.join(model_names)}")

            # Procesar modelos uno por uno
            for model_name in model_names:
                if not hasattr(models_module, model_name):
                    print(f" El modelo '{model_name}' no existe en meicobaseapi.models")
                    continue

                model_class = getattr(models_module, model_name)
                sql_script = self.generate_create_sql(model_class)

                output_path = os.path.join(output_dir, f"{model_name}.sql")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(sql_script)

                print(f" Script generado correctamente: {output_path}")

        except Exception as e:
            print(f" Error generando script: {e}")

    # ============================================================
    # FUNCIONES INTERNAS
    # ============================================================

    def generate_create_sql(self, model_class):
        try:
            """Genera el script CREATE TABLE para un modelo Django"""
            table_name = model_class._meta.db_table
            sql_lines = [f"CREATE TABLE dbo.{table_name} ("]
            pk_fields = []
            fk_constraints = []

            for field in model_class._meta.get_fields():
                if not isinstance(field, models.Field):
                    continue

                col_name = field.column
                # Detectar si es ForeignKey
                if isinstance(field, models.ForeignKey):
                    ref_field = field.target_field
                    col_type = self.map_field_type(ref_field, is_foreign_key=True)
                else:
                    col_type = self.map_field_type(field)

                null_sql = "NULL" if field.null else "NOT NULL"

                if field.primary_key:
                    pk_fields.append(col_name)

                sql_lines.append(f"    {col_name} {col_type} {null_sql},")

                if isinstance(field, models.ForeignKey):
                    ref_table = field.related_model._meta.db_table
                    ref_col = field.target_field.column
                    fk_name = f"FK_{table_name}_{col_name}_{ref_table}"
                    fk_constraints.append(
                        f"ALTER TABLE dbo.{table_name} ADD CONSTRAINT {fk_name} FOREIGN KEY ({col_name}) REFERENCES dbo.{ref_table} ({ref_col});"
                    )

            if pk_fields:
                pk_str = ", ".join(pk_fields)
                sql_lines.append(f"    PRIMARY KEY ({pk_str})")

            sql_lines.append(");\n")

            if fk_constraints:
                sql_lines.append("\n".join(fk_constraints))
            return "\n".join(sql_lines)
        except Exception as e:
            raise e
        

    def map_field_type(self, field, is_foreign_key=False):
        """Mapea tipos de Django a SQL Server"""
        # No permitir IDENTITY en claves foráneas
        if isinstance(field, models.AutoField):
            return "INT IDENTITY(1,1)" if not is_foreign_key else "INT"
        elif isinstance(field, models.BigAutoField):
            return "BIGINT IDENTITY(1,1)" if not is_foreign_key else "BIGINT"
        elif isinstance(field, models.IntegerField):
            return "INT"
        elif isinstance(field, models.BigIntegerField):
            return "BIGINT"
        elif isinstance(field, models.CharField):
            return f"VARCHAR({field.max_length or 255})"
        elif isinstance(field, models.TextField):
            return "TEXT"
        elif isinstance(field, models.DateTimeField):
            return "DATETIME"
        elif isinstance(field, models.BooleanField):
            return "BIT"
        elif isinstance(field, models.DecimalField):
            return f"DECIMAL({field.max_digits},{field.decimal_places})"
        elif isinstance(field, models.FloatField):
            return "FLOAT"
        elif isinstance(field, models.DateField):
            return "DATE"
        else:
            return "VARCHAR(255)"  # fallback