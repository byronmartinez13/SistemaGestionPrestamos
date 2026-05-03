import re
from datetime import datetime

# =========================
# TUS MIXINS EXISTENTES
# =========================


class BuscarMixin:
    """Buscar objetos por nombre en una lista"""

    def buscar_por_nombre(self, lista, nombre):
        return next((obj for obj in lista if obj.nombre.lower() == nombre.lower()), None)


class BuscarPorIdMixin:
    """Buscar objetos por ID en una lista"""

    def buscar_por_id(self, lista, id_buscar):
        return next((obj for obj in lista if obj.id == id_buscar), None)


class MostrarMixin:
    """Mostrar todos los elementos de una lista"""

    def mostrar_lista(self, lista):
        for obj in lista:
            print(obj.mostrar())


class InputMixin:
    """Mixin con validaciones de input (tus funciones originales)"""

    def input_int(self, msg):
        while True:
            try:
                return int(input(msg))
            except ValueError:
                print("❌ Número entero requerido")

    def input_float(self, msg):
        while True:
            try:
                valor = float(input(msg))
                if valor < 0:
                    print("❌ No se permiten valores negativos")
                    continue
                return valor
            except ValueError:
                print("❌ Número válido requerido")

    def input_str(self, msg):
        while True:
            val = input(msg).strip()
            if val:
                return val
            print("❌ Campo vacío")

    def input_id(self, msg, prefijo):
        patron = f"^{prefijo}-\\d{{4}}$"
        while True:
            val = input(msg).strip()
            if re.match(patron, val):
                return val
            print(f"❌ Formato inválido. Ej: {prefijo}-0001")

    def input_cedula(self, msg):
        from core.decorators import es_cedula_ecuatoriana
        while True:
            cedula = input(msg).strip()
            if es_cedula_ecuatoriana(cedula):
                return cedula
            print("❌ Cédula ecuatoriana inválida")

    def input_fecha(self, msg):
        while True:
            fecha = input(msg).strip()
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
                return fecha
            except ValueError:
                print("❌ Formato inválido. Use YYYY-MM-DD")

    def input_nombre(self, msg):
        while True:
            nombre = input(msg).strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                continue
            if not all(c.isalpha() or c.isspace() for c in nombre):
                print("❌ El nombre solo debe contener letras")
                continue
            return nombre.title()


class ValidationMixin:
    """Mixin básico de validaciones (complementario a InputMixin)"""

    @staticmethod
    def validate_not_empty(value, field_name):
        if not value or not str(value).strip():
            raise ValueError(f"{field_name} no puede estar vacío")

    @staticmethod
    def validate_positive_number(value, field_name):
        if value <= 0:
            raise ValueError(f"{field_name} debe ser mayor a 0")


class LogMixin:
    """Registro de acciones del sistema"""
    LOG_PREFIX = "[LOG]"

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{self.LOG_PREFIX} [{timestamp}]: {message}")
