class StatsController:
    def __init__(self, employee_controller, loan_controller, payment_controller):
        self.employee_controller = employee_controller
        self.loan_controller = loan_controller
        self.payment_controller = payment_controller

    def estadisticas(self):
        print("\n" + "=" * 50)
        print("   📊 ESTADÍSTICAS DEL SISTEMA")
        print("=" * 50)

        empleados = self.employee_controller.empleados
        prestamos = self.loan_controller.prestamos
        pagos = self.payment_controller.pagos

        print(f"\n👥 EMPLEADOS:")
        print(f"   Total empleados: {len(empleados)}")
        if empleados:
            sueldos = [e.sueldo for e in empleados]
            print(f"   Promedio sueldo: ${sum(sueldos)/len(sueldos):.2f}")
            print(f"   Sueldo máximo: ${max(sueldos):.2f}")
            print(f"   Sueldo mínimo: ${min(sueldos):.2f}")

        print(f"\n📋 PRÉSTAMOS:")
        print(f"   Total préstamos: {len(prestamos)}")
        if prestamos:
            montos = [p.monto for p in prestamos]
            print(f"   Monto total prestado: ${sum(montos):.2f}")
            print(f"   Promedio préstamo: ${sum(montos)/len(montos):.2f}")
            print(f"   Préstamo máximo: ${max(montos):.2f}")
            print(f"   Préstamo mínimo: ${min(montos):.2f}")

            activos = [p for p in prestamos if p.saldo > 0]
            pagados = [p for p in prestamos if p.saldo == 0]
            print(f"   Préstamos activos: {len(activos)}")
            print(f"   Préstamos pagados: {len(pagados)}")
            print(
                f"   Saldo pendiente total: ${sum(p.saldo for p in activos):.2f}")

        print(f"\n💰 PAGOS:")
        print(f"   Total pagos: {len(pagos)}")
        if pagos:
            valores = [pg.valor for pg in pagos]
            print(f"   Monto total pagado: ${sum(valores):.2f}")
            print(f"   Promedio pago: ${sum(valores)/len(valores):.2f}")
            print(f"   Pago máximo: ${max(valores):.2f}")
            print(f"   Pago mínimo: ${min(valores):.2f}")

        print("\n" + "=" * 50)
