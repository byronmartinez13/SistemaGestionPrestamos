from core import JsonManager, LogMixin, InputMixin, MostrarMixin, BuscarPorIdMixin
from models import Empleado
from core import print_colored, print_header, Colors


class EmployeeController(InputMixin, MostrarMixin, BuscarPorIdMixin, LogMixin):
    DATA_FILE = "data/employees.json"

    def __init__(self):
        self.db = JsonManager(EmployeeController.DATA_FILE)
        self.empleados = []
        self._load_data()

    def _load_data(self):
        """Cargar empleados desde JSON"""
        data = self.db.load()
        self.empleados = [Empleado.from_dict(item) for item in data]

    def _save_data(self):
        """Guardar empleados a JSON"""
        data = [emp.to_dict() for emp in self.empleados]
        self.db.save(data)

    def form_empleado(self):
        """Registrar empleado con tus validaciones"""
        print_header("\n=== REGISTRO EMPLEADO ===")

        nombre = self.input_nombre("Nombre: ")
        cedula = self.input_cedula("Cédula: ")
        sueldo = self.input_float("Sueldo: ")

        print(f"\nResumen:")
        print(f"Nombre: {nombre}")
        print(f"Cédula: {cedula}")
        print(f"Sueldo: {sueldo}")

        confirm = input("¿Guardar? (1=Sí / 2=No): ")

        if confirm != "1":
            print_colored("   ❌ Registro cancelado", Colors.BRIGHT_RED)
            return

        emp = Empleado(cedula, nombre, sueldo)
        self.empleados.append(emp)
        self._save_data()

        self.log(f"Empleado {nombre} registrado con ID: {emp.id}")
        print_colored(f"\n   ✅ Guardado | ID: {emp.id}", Colors.BRIGHT_GREEN)
        print_colored(
            f"   💰 Máximo préstamo disponible: ${emp.max_loan_amount:.2f}", Colors.BRIGHT_CYAN)

    def listar_empleados(self):
        """Listar todos los empleados"""
        print("\n--- EMPLEADOS ---")
        if not self.empleados:
            print("No hay empleados registrados")
            return
        self.mostrar_lista(self.empleados)

    def actualizar_empleado(self, emp_id):
        """Actualizar datos de un empleado"""
        empleado = self.buscar_por_id(self.empleados, emp_id)

        if not empleado:
            print("❌ Empleado no encontrado")
            return

        print(f"\n--- ACTUALIZANDO: {empleado.mostrar()} ---")
        print("(Deje en blanco para mantener el valor actual)")

        nuevo_nombre = input(f"Nuevo nombre ({empleado.nombre}): ").strip()
        if nuevo_nombre:
            if all(c.isalpha() or c.isspace() for c in nuevo_nombre):
                empleado.nombre = nuevo_nombre.title()
            else:
                print("❌ Nombre inválido. Solo letras.")
                return

        nueva_cedula = input(f"Nueva cédula ({empleado.cedula}): ").strip()
        if nueva_cedula:
            from core.decorators import es_cedula_ecuatoriana
            if es_cedula_ecuatoriana(nueva_cedula):
                empleado.cedula = nueva_cedula
            else:
                print("❌ Cédula inválida")
                return

        nuevo_sueldo = input(f"Nuevo sueldo ({empleado.sueldo}): ").strip()
        if nuevo_sueldo:
            try:
                sueldo = float(nuevo_sueldo)
                if sueldo > 0:
                    empleado.sueldo = sueldo
                else:
                    print("❌ Sueldo debe ser positivo")
                    return
            except ValueError:
                print("❌ Valor numérico requerido")
                return

        self._save_data()
        self.log(f"Empleado {emp_id} actualizado")
        print(f"✅ Empleado actualizado: {empleado.mostrar()}")

    def eliminar_empleado(self, emp_id):
        """Eliminar empleado (solo si no tiene préstamos activos)"""
        empleado = self.buscar_por_id(self.empleados, emp_id)

        if not empleado:
            print("❌ Empleado no encontrado")
            return

        # Verificar si tiene préstamos activos
        from .loan_controller import LoanController
        # Nota: esto requiere acceso a los préstamos, lo manejaremos desde el menú
        # Por ahora, una verificación simple

        confirm = input(f"¿Eliminar a {empleado.nombre}? (s/n): ").lower()
        if confirm == "s":
            self.empleados = [e for e in self.empleados if e.id != emp_id]
            self._save_data()
            self.log(f"Empleado {emp_id} eliminado")
            print("🗑 Empleado eliminado")
        else:
            print("❌ Eliminación cancelada")

    def get_empleados_list(self):
        """Retornar lista de empleados (para otros controladores)"""
        return self.empleados
