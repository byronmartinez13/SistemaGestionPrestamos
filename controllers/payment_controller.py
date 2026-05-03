from datetime import datetime
from core import JsonManager, LogMixin, InputMixin, MostrarMixin, BuscarPorIdMixin
from models import Pago


class PaymentController(InputMixin, MostrarMixin, BuscarPorIdMixin, LogMixin):
    DATA_FILE = "data/pagos.json"  # Cambiado a pagos.json para coincidir

    def __init__(self, loan_controller):
        self.loan_controller = loan_controller
        self.db = JsonManager(PaymentController.DATA_FILE)
        self.pagos = []
        self._load_data()

    def _load_data(self):
        """Cargar pagos desde JSON"""
        data = self.db.load()
        prestamos_dict = {p.id: p for p in self.loan_controller.prestamos}
        self.pagos = [Pago.from_dict(item, prestamos_dict) for item in data]

    def _save_data(self):
        """Guardar pagos a JSON"""
        data = [pg.to_dict() for pg in self.pagos]
        self.db.save(data)

    def registrar_pago(self):
        """Registrar un pago con todas las validaciones"""
        print("\n--- PRÉSTAMOS DISPONIBLES ---")
        self.loan_controller.listar_prestamos(solo_activos=True)

        if not self.loan_controller.prestamos:
            print("❌ No hay préstamos registrados")
            return

        prestamo_id = self.input_id("ID préstamo: ", "PRE")

        # ✅ USAR EL MÉTODO CORRECTO
        prestamo = self.loan_controller.get_prestamo_by_id(prestamo_id)

        if prestamo is None:
            print("❌ ID no encontrado")
            return

        if prestamo.saldo <= 0:
            print("❌ Este préstamo ya está pagado")
            return

        print(f"\n💰 Saldo actual: ${prestamo.saldo:.2f}")
        valor = self.input_float("Monto a pagar: ")

        if valor > prestamo.saldo:
            print(
                f"❌ El pago (${valor:.2f}) excede el saldo pendiente (${prestamo.saldo:.2f})")
            return

        fecha = self.input_fecha("Fecha pago (YYYY-MM-DD): ")

        # Validar fecha
        fecha_pago_dt = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_prestamo_dt = datetime.strptime(prestamo.fecha, "%Y-%m-%d")
        hoy = datetime.now()

        if fecha_pago_dt < fecha_prestamo_dt:
            print("❌ La fecha de pago no puede ser anterior al préstamo")
            return

        if fecha_pago_dt > hoy:
            print("❌ No se puede registrar un pago en una fecha futura")
            return

        nuevo_saldo = prestamo.saldo - valor

        confirm = input(
            f"Saldo actual: {prestamo.saldo:.2f} → Nuevo: {nuevo_saldo:.2f} ¿Confirmar? (s/n): ")

        if confirm.lower() == "s":
            prestamo.saldo = nuevo_saldo
            pago = Pago(prestamo, valor, fecha)
            self.pagos.append(pago)
            self._save_data()
            self.loan_controller._save_data()  # Actualizar saldo del préstamo

            self.log(f"Pago registrado | ID: {pago.id}")
            print(f"✅ Pago registrado | ID: {pago.id}")

            if nuevo_saldo == 0:
                print("🎉 ¡Préstamo completamente pagado!")

    def listar_pagos(self):
        """Listar todos los pagos"""
        print("\n--- PAGOS ---")
        if not self.pagos:
            print("No hay pagos registrados")
            return
        self.mostrar_lista(self.pagos)

    # ✅ MÉTODO ACTUALIZAR PAGO
    def actualizar_pago(self, pag_id):
        """Actualizar un pago existente"""
        pago = self.buscar_por_id(self.pagos, pag_id)

        if not pago:
            print("❌ Pago no encontrado")
            return

        print(f"\n--- ACTUALIZANDO: {pago.mostrar()} ---")
        print("(Deje en blanco para mantener el valor actual)")

        nuevo_valor = input(f"Nuevo valor ({pago.valor}): ").strip()
        if nuevo_valor:
            try:
                valor = float(nuevo_valor)
                prestamo = pago.prestamo

                # Recalcular saldo
                diferencia = valor - pago.valor
                if valor > prestamo.saldo + pago.valor:
                    print(
                        f"❌ El nuevo valor (${valor:.2f}) excede lo permitido")
                    return

                prestamo.saldo -= diferencia
                pago.valor = valor
                self.loan_controller._save_data()
                print(
                    f"✅ Valor actualizado. Nuevo saldo del préstamo: ${prestamo.saldo:.2f}")
            except ValueError:
                print("❌ Valor numérico requerido")
                return

        nueva_fecha = input(f"Nueva fecha ({pago.fecha}): ").strip()
        if nueva_fecha:
            try:
                datetime.strptime(nueva_fecha, "%Y-%m-%d")
                pago.fecha = nueva_fecha
                print("✅ Fecha actualizada")
            except ValueError:
                print("❌ Formato inválido. Use YYYY-MM-DD")

        self._save_data()
        self.log(f"Pago {pag_id} actualizado")
        print(f"✅ Pago actualizado: {pago.mostrar()}")

    # ✅ MÉTODO ELIMINAR PAGO (mejorado)
    def eliminar_pago(self, pag_id):
        """Eliminar un pago y revertir el saldo"""
        pago = self.buscar_por_id(self.pagos, pag_id)

        if not pago:
            print("❌ Pago no encontrado")
            return

        print(f"\n⚠️ Pago a eliminar: {pago.mostrar()}")
        print(f"   Saldo actual del préstamo: ${pago.prestamo.saldo:.2f}")
        print(
            f"   Al eliminar, el saldo volverá a: ${pago.prestamo.saldo + pago.valor:.2f}")

        confirm = input("\n¿Confirmar eliminación? (s/n): ").lower()
        if confirm == "s":
            # Revertir efecto del pago
            pago.prestamo.saldo += pago.valor
            # Eliminar pago
            self.pagos = [p for p in self.pagos if p.id != pag_id]
            self._save_data()
            self.loan_controller._save_data()
            self.log(f"Pago {pag_id} eliminado")
            print(
                f"🗑 Pago eliminado. Nuevo saldo del préstamo: ${pago.prestamo.saldo:.2f}")
        else:
            print("❌ Eliminación cancelada")

    def consultar_empleado_detalle(self, empleado):
        """Mostrar detalle completo de un empleado con sus préstamos y pagos"""
        print(f"\n📋 DETALLE: {empleado.mostrar()}")

        prestamos_emp = [
            p for p in self.loan_controller.prestamos if p.empleado.id == empleado.id]

        if not prestamos_emp:
            print("  No tiene préstamos registrados")
            return

        for p in prestamos_emp:
            print(f"\n  📌 {p.mostrar()}")
            pagos_prestamo = [
                pg for pg in self.pagos if pg.prestamo.id == p.id]
            if pagos_prestamo:
                print("     Pagos realizados:")
                for pg in pagos_prestamo:
                    print(f"       {pg.mostrar()}")
            else:
                print("     Sin pagos registrados")
