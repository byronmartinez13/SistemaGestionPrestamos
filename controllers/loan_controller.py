from core import JsonManager, LogMixin, InputMixin, MostrarMixin, BuscarPorIdMixin
from models import Prestamo


class LoanController(InputMixin, MostrarMixin, BuscarPorIdMixin, LogMixin):
    DATA_FILE = "data/loans.json"

    def __init__(self, employee_controller):
        self.employee_controller = employee_controller
        self.db = JsonManager(LoanController.DATA_FILE)
        self.prestamos = []
        self._load_data()

    def _load_data(self):
        """Cargar préstamos desde JSON"""
        data = self.db.load()
        empleados_dict = {
            emp.id: emp for emp in self.employee_controller.empleados}
        self.prestamos = [Prestamo.from_dict(
            item, empleados_dict) for item in data]

    def _save_data(self):
        """Guardar préstamos a JSON"""
        data = [p.to_dict() for p in self.prestamos]
        self.db.save(data)

    # ✅ MÉTODO FALTANTE - Buscar préstamo por ID
    def get_prestamo_by_id(self, prestamo_id):
        """Retorna un préstamo por su ID"""
        return self.buscar_por_id(self.prestamos, prestamo_id)

    def crear_prestamo(self):
        """Flujo completo para crear un préstamo"""
        print("\n--- EMPLEADOS DISPONIBLES ---")
        self.employee_controller.listar_empleados()

        if not self.employee_controller.empleados:
            print("❌ No hay empleados registrados")
            return

        emp_id = self.input_id("ID empleado: ", "EMP")
        emp = self.buscar_por_id(self.employee_controller.empleados, emp_id)

        if emp is None:
            print("❌ ID no encontrado")
            return

        monto = self.input_float("Monto: ")
        cuotas = self.input_int("Cuotas: ")
        fecha = self.input_fecha("Fecha préstamo (YYYY-MM-DD): ")

        print(f"\nResumen:")
        print(f"Empleado: {emp.nombre}")
        print(f"Monto: {monto}")
        print(f"Cuotas: {cuotas}")
        print(f"Fecha: {fecha}")

        confirm = input("¿Guardar? (1=Sí / 2=No): ")

        if confirm != "1":
            print("❌ Operación cancelada")
            return

        p = Prestamo(emp, monto, cuotas, fecha)
        self.prestamos.append(p)
        self._save_data()

        self.log(f"Préstamo creado | ID: {p.id}")
        print(f"✅ Préstamo creado | ID: {p.id}")
        print(f"💰 Cuota mensual: ${p.cuota:.2f}")

    def listar_prestamos(self, solo_activos=False):
        """Listar préstamos"""
        print("\n--- PRÉSTAMOS ---")
        if not self.prestamos:
            print("No hay préstamos registrados")
            return

        prestamos_a_mostrar = self.prestamos
        if solo_activos:
            prestamos_a_mostrar = [p for p in self.prestamos if p.saldo > 0]

        for p in prestamos_a_mostrar:
            print(p.mostrar())

    # ✅ MÉTODO ACTUALIZAR PRÉSTAMO
    def actualizar_prestamo(self, loan_id):
        """Actualizar datos de un préstamo"""
        prestamo = self.buscar_por_id(self.prestamos, loan_id)

        if not prestamo:
            print("❌ Préstamo no encontrado")
            return

        print(f"\n--- ACTUALIZANDO: {prestamo.mostrar()} ---")
        print("(Deje en blanco para mantener el valor actual)")

        nuevo_monto = input(f"Nuevo monto ({prestamo.monto}): ").strip()
        if nuevo_monto:
            try:
                monto = float(nuevo_monto)
                if monto > 0:
                    diferencia = monto - prestamo.monto
                    prestamo.monto = monto
                    prestamo.saldo += diferencia
                    prestamo.cuota = prestamo.monto / prestamo.cuotas
                    print(
                        f"✅ Monto actualizado. Nuevo saldo: ${prestamo.saldo:.2f}")
                else:
                    print("❌ Monto debe ser positivo")
                    return
            except ValueError:
                print("❌ Valor numérico requerido")
                return

        nuevas_cuotas = input(f"Nuevas cuotas ({prestamo.cuotas}): ").strip()
        if nuevas_cuotas:
            try:
                cuotas = int(nuevas_cuotas)
                if cuotas > 0:
                    prestamo.cuotas = cuotas
                    prestamo.cuota = prestamo.monto / prestamo.cuotas
                    print(
                        f"✅ Cuotas actualizadas. Nueva cuota: ${prestamo.cuota:.2f}")
                else:
                    print("❌ Cuotas deben ser positivas")
                    return
            except ValueError:
                print("❌ Número entero requerido")
                return

        nueva_fecha = input(f"Nueva fecha ({prestamo.fecha}): ").strip()
        if nueva_fecha:
            # Validar formato de fecha
            from datetime import datetime
            try:
                datetime.strptime(nueva_fecha, "%Y-%m-%d")
                prestamo.fecha = nueva_fecha
                print("✅ Fecha actualizada")
            except ValueError:
                print("❌ Formato de fecha inválido. Use YYYY-MM-DD")

        self._save_data()
        self.log(f"Préstamo {loan_id} actualizado")
        print(f"✅ Préstamo actualizado: {prestamo.mostrar()}")

    # ✅ MÉTODO ELIMINAR PRÉSTAMO
    def eliminar_prestamo(self, loan_id):
        """Eliminar préstamo (solo si no tiene pagos)"""
        prestamo = self.buscar_por_id(self.prestamos, loan_id)

        if not prestamo:
            print("❌ Préstamo no encontrado")
            return

        # Verificar si tiene pagos (esto se verifica mejor desde payment_controller)
        confirm = input(
            f"⚠️ ¿Eliminar préstamo {loan_id}? Esto eliminará TODOS sus pagos asociados (s/n): ").lower()
        if confirm == "s":
            self.prestamos = [p for p in self.prestamos if p.id != loan_id]
            self._save_data()
            self.log(f"Préstamo {loan_id} eliminado")
            print("🗑 Préstamo eliminado")
        else:
            print("❌ Eliminación cancelada")

    def get_prestamos_list(self):
        return self.prestamos
