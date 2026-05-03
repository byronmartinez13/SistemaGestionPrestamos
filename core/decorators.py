import re

# =========================
# DECORADORES
# =========================


def validar_no_negativo(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                print("❌ Valores negativos no permitidos")
                return None
        return func(*args, **kwargs)
    return wrapper


def validar_formato_id(prefijo, index_param=0):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if len(args) <= index_param:
                print("❌ ID no proporcionado")
                return None
            patron = f"^{prefijo}-\\d{{4}}$"
            if not re.match(patron, args[index_param]):
                print(f"❌ Formato inválido. Ej: {prefijo}-0001")
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def validar_existencia(lista_attr, index_param=0):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            lista = getattr(self, lista_attr)
            if len(args) <= index_param:
                print("❌ ID no proporcionado")
                return None
            if not any(obj.id == args[index_param] for obj in lista):
                print("❌ ID no encontrado")
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def validar_pago(func):
    def wrapper(self, prestamo_id, valor):
        prestamo = next(
            (p for p in self.prestamos if p.id == prestamo_id), None)
        if prestamo and valor > prestamo.saldo:
            print("❌ Pago mayor al saldo")
            return None
        return func(self, prestamo_id, valor)
    return wrapper


def es_cedula_ecuatoriana(cedula):
    """Valida cédula ecuatoriana"""
    if not cedula or not str(cedula).isdigit() or len(str(cedula)) != 10:
        return False

    cedula = str(cedula)
    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor >= 10:
            valor -= 9
        suma += valor

    digito_verificador = (10 - (suma % 10)) % 10

    return digito_verificador == int(cedula[9])
