import os
import importlib
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = "Genera scripts CREATE TABLE solo para los modelos definidos en meicobaseapi.models (sin ejecutar en la DB)."

    def add_arguments(self, parser):
        parser.add_argument('--class', nargs='+', type=str, help="Nombre(s) específicos de modelos a generar")

    def handle(self, *args, **options):
        try:
            print(" Generando script SQL desde meicobaseapi.models...")

            # Importamos el módulo de modelos principal
            models_module = importlib.import_module("meicobaseapi.models")

            # Crear carpeta de salida
            output_dir = os.path.join(os.getcwd(), "generated_sql")
            os.makedirs(output_dir, exist_ok=True)

            # Obtener solo los modelos definidos en ese archivo (no los del core de Django)
            module_models = [
                m for m in apps.get_models()
                if m.__module__ == "meicobaseapi.models" and not m._meta.abstract
            ]

            if not module_models:
                print(" No se encontraron modelos definidos en meicobaseapi.models.")
                return

            # Filtramos si se pasan nombres de clases
            model_names = options.get("class", None)
            if model_names:
                models_to_process = [m for m in module_models if m.__name__ in model_names]
            else:
                models_to_process = module_models

            if not models_to_process:
                print(" Ningún modelo coincide con los nombres indicados.")
                return

            print(f" Modelos detectados: {', '.join([m.__name__ for m in models_to_process])}")

            # Ordenar modelos según dependencias de ForeignKey
            models_to_process = self.sort_by_dependencies(models_to_process)

            # Crear un único archivo SQL
            output_path = os.path.join(output_dir, "create_all_tables.sql")
            with open(output_path, "w", encoding="utf-8") as f:
                for model_class in models_to_process:
                    sql_script = self.generate_create_sql(model_class)
                    f.write(sql_script + "\n\n")
                    print(f" Script generado para: {model_class.__name__}")

            print(f"\n Archivo final generado en: {output_path}")

        except Exception as e:
            print(f" Error generando script: {e}")

    # ============================================================
    # FUNCIONES AUXILIARES
    # ============================================================

    def sort_by_dependencies(self, model_list):
        try:
            """Ordena modelos respetando dependencias de claves foráneas."""
            dependency_graph = {m.__name__: set() for m in model_list}

            for model in model_list:
                for field in model._meta.get_fields():
                    if isinstance(field, models.ForeignKey):
                        ref_name = field.related_model.__name__
                        if ref_name in dependency_graph:
                            dependency_graph[model.__name__].add(ref_name)

            sorted_models = []
            while dependency_graph:
                independents = [m for m, deps in dependency_graph.items() if not deps]
                if not independents:
                    independents = [list(dependency_graph.keys())[0]]  # rompe ciclos
                sorted_models.extend(independents)
                for indep in independents:
                    dependency_graph.pop(indep, None)
                for deps in dependency_graph.values():
                    deps.difference_update(independents)

            name_to_model = {m.__name__: m for m in model_list}
            return [name_to_model[n] for n in sorted_models if n in name_to_model]
        except Exception as e:
            raise e
        


    def generate_create_sql(self, model_class):
        try:
            """Genera el SQL CREATE TABLE para un modelo Django."""
            table_name = model_class._meta.db_table
            sql_lines = [f"CREATE TABLE dbo.{table_name} ("]
            pk_fields = []
            fk_constraints = []

            for field in model_class._meta.get_fields():
                if not isinstance(field, models.Field):
                    continue

                col_name = field.column
                if isinstance(field, models.ForeignKey):
                    ref_field = field.target_field
                    col_type = self.map_field_type(ref_field, is_foreign_key=True)
                else:
                    col_type = self.map_field_type(field)

                null_sql = "NULL" if field.null else "NOT NULL"
                sql_lines.append(f"    {col_name} {col_type} {null_sql},")

                if field.primary_key:
                    pk_fields.append(col_name)

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
        """Convierte tipos de Django a tipos SQL Server."""
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
            return "VARCHAR(255)"
