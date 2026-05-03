from models.base import Base

class Pago(Base):
    PREFIJO = "PAG"

    def __init__(self, prestamo, valor, fecha):
        self.id = self.generar_id()
        self.prestamo = prestamo
        self.fecha = fecha
        self.valor = valor

    def mostrar(self):
        return f"{self.id} | ${self.valor:.2f} | Préstamo: {self.prestamo.id} | Fecha: {self.fecha}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "prestamo_id": self.prestamo.id,
            "fecha": self.fecha,
            "valor": self.valor
        }
    
    @staticmethod
    def from_dict(data, prestamos_dict=None):
        from models.loan import Prestamo
        
        prestamo = None
        if prestamos_dict and data.get("prestamo_id"):
            prestamo = prestamos_dict.get(data["prestamo_id"])
        
        pago = Pago(
            prestamo=prestamo,
            valor=data["valor"],
            fecha=data["fecha"]
        )
        pago.id = data["id"]
        
        # Restaurar contador
        numero = int(data["id"].split("-")[1])
        if numero > Pago._contador:
            Pago._contador = numero
        
        return pago