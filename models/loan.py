from models.base import Base

class Prestamo(Base):
    PREFIJO = "PRE"

    def __init__(self, empleado, monto, cuotas, fecha):
        self.id = self.generar_id()
        self.empleado = empleado
        self.fecha = fecha
        self.monto = monto
        self.cuotas = cuotas
        self.cuota = monto / cuotas
        self.saldo = monto

    def mostrar(self):
        estado = "🔴 Activo" if self.saldo > 0 else "✅ Pagado"
        return f"{self.id} | {self.empleado.nombre} | ${self.saldo:.2f} | {estado}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "empleado": self.empleado.to_dict(),
            "fecha": self.fecha,
            "monto": self.monto,
            "cuotas": self.cuotas,
            "cuota": self.cuota,
            "saldo": self.saldo
        }
    
    @staticmethod
    def from_dict(data, empleados_dict=None):
        from models.employee import Empleado
        
        empleado = None
        if empleados_dict and data["empleado"].get("id"):
            empleado = empleados_dict.get(data["empleado"]["id"])
        if not empleado:
            empleado = Empleado.from_dict(data["empleado"])
        
        prestamo = Prestamo(
            empleado=empleado,
            monto=data["monto"],
            cuotas=data["cuotas"],
            fecha=data["fecha"]
        )
        prestamo.id = data["id"]
        prestamo.saldo = data["saldo"]
        
        # Restaurar contador
        numero = int(data["id"].split("-")[1])
        if numero > Prestamo._contador:
            Prestamo._contador = numero
        
        return prestamo
    