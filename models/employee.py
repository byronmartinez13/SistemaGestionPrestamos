from models.base import Base

class Empleado(Base):
    PREFIJO = "EMP"

    def __init__(self, cedula, nombre, sueldo):
        self.id = self.generar_id()
        self.cedula = cedula
        self.nombre = nombre
        self.sueldo = sueldo

    def mostrar(self):
        return f"{self.id} | {self.nombre} | ${self.sueldo}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombre": self.nombre,
            "sueldo": self.sueldo
        }
    
    @staticmethod
    def from_dict(data):
        empleado = Empleado(
            cedula=data["cedula"],
            nombre=data["nombre"],
            sueldo=data["sueldo"]
        )
        empleado.id = data["id"]
        # Restaurar el contador para mantener IDs consistentes
        numero = int(data["id"].split("-")[1])
        if numero > Empleado._contador:
            Empleado._contador = numero
        return empleado
    
    @property
    def max_loan_amount(self):
        """50% del sueldo anual"""
        return round(self.sueldo * 0.5 * 12, 2)