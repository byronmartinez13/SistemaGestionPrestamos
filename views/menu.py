from core import (
    clear_screen, gotoxy, Colors, print_colored,
    draw_title, draw_menu_option, print_header
)
from controllers import (
    EmployeeController, LoanController,
    PaymentController, StatsController
)


class Menu:
    def __init__(self):
        self.employee_controller = EmployeeController()
        self.loan_controller = LoanController(self.employee_controller)
        self.payment_controller = PaymentController(self.loan_controller)

    def main_menu(self):
        while True:
            clear_screen()

            # Título principal
            print_colored("=" * 55, Colors.BRIGHT_CYAN)
            print_colored("    🏦 SISTEMA DE GESTIÓN DE PRÉSTAMOS",
                          Colors.BRIGHT_YELLOW + Colors.BOLD)
            print_colored("=" * 55, Colors.BRIGHT_CYAN)
            print()

            # Menú principal
            print_colored("   📋 MENÚ PRINCIPAL",
                          Colors.BRIGHT_GREEN + Colors.BOLD)
            print()
            print_colored("   1. 👥 Gestión de Empleados", Colors.WHITE)
            print_colored("   2. 📋 Gestión de Préstamos", Colors.WHITE)
            print_colored("   3. 💰 Gestión de Pagos", Colors.WHITE)
            print_colored("   4. 🔍 Consultar / Reportes", Colors.WHITE)
            print_colored("   5. 📊 Estadísticas", Colors.WHITE)
            print()
            print_colored("   0. 🚪 Salir", Colors.BRIGHT_RED)
            print()
            print_colored("-" * 55, Colors.BRIGHT_CYAN)
            print()

            opcion = input("   Opción: ")

            if opcion == "1":
                self._menu_empleados()
            elif opcion == "2":
                self._menu_prestamos()
            elif opcion == "3":
                self._menu_pagos()
            elif opcion == "4":
                self._menu_consultar()
            elif opcion == "5":
                StatsController(
                    self.employee_controller,
                    self.loan_controller,
                    self.payment_controller
                ).estadisticas()
                input("\n   Presione Enter para continuar...")
            elif opcion == "0":
                clear_screen()
                print_colored("\n   👋 ¡Gracias por usar el sistema!",
                              Colors.BRIGHT_GREEN + Colors.BOLD)
                print_colored("   Hasta luego!\n", Colors.BRIGHT_CYAN)
                break
            else:
                print_colored("   ❌ Opción inválida", Colors.BRIGHT_RED)
                input("   Presione Enter para continuar...")

    def _menu_empleados(self):
        while True:
            clear_screen()
            print_header("GESTIÓN DE EMPLEADOS")

            print_colored("\n   📋 OPCIONES:",
                          Colors.BRIGHT_GREEN + Colors.BOLD)
            print()
            print_colored("   1. ➕ Crear empleado", Colors.WHITE)
            print_colored("   2. 📖 Listar empleados", Colors.WHITE)
            print_colored("   3. ✏️ Actualizar empleado", Colors.WHITE)
            print_colored("   4. 🗑 Eliminar empleado", Colors.WHITE)
            print()
            print_colored("   0. 🔙 Volver", Colors.BRIGHT_CYAN)
            print()
            print_colored("-" * 40, Colors.BRIGHT_CYAN)
            print()

            op = input("   Opción: ")

            if op == "1":
                self.employee_controller.form_empleado()
                input("\n   Presione Enter para continuar...")
            elif op == "2":
                self.employee_controller.listar_empleados()
                input("\n   Presione Enter para continuar...")
            elif op == "3":
                emp_id = self.employee_controller.input_id(
                    "   ID empleado a actualizar: ", "EMP")
                self.employee_controller.actualizar_empleado(emp_id)
                input("\n   Presione Enter para continuar...")
            elif op == "4":
                self.employee_controller.listar_empleados()
                emp_id = self.employee_controller.input_id(
                    "\n   ID empleado a eliminar: ", "EMP")
                self.employee_controller.eliminar_empleado(emp_id)
                input("\n   Presione Enter para continuar...")
            elif op == "0":
                break
            else:
                print_colored("   ❌ Opción inválida", Colors.BRIGHT_RED)
                input("   Presione Enter para continuar...")

    def _menu_prestamos(self):
        while True:
            clear_screen()
            print_header("GESTIÓN DE PRÉSTAMOS")

            print_colored("\n   📋 OPCIONES:",
                          Colors.BRIGHT_GREEN + Colors.BOLD)
            print()
            print_colored("   1. ➕ Crear préstamo", Colors.WHITE)
            print_colored("   2. 📖 Listar préstamos", Colors.WHITE)
            print_colored("   3. ✏️ Actualizar préstamo", Colors.WHITE)
            print_colored("   4. 🗑 Eliminar préstamo", Colors.WHITE)
            print()
            print_colored("   0. 🔙 Volver", Colors.BRIGHT_CYAN)
            print()
            print_colored("-" * 40, Colors.BRIGHT_CYAN)
            print()

            op = input("   Opción: ")

            if op == "1":
                self.loan_controller.crear_prestamo()
                input("\n   Presione Enter para continuar...")
            elif op == "2":
                self.loan_controller.listar_prestamos()
                input("\n   Presione Enter para continuar...")
            elif op == "3":
                loan_id = self.employee_controller.input_id(
                    "   ID préstamo a actualizar: ", "PRE")
                self.loan_controller.actualizar_prestamo(loan_id)
                input("\n   Presione Enter para continuar...")
            elif op == "4":
                self.loan_controller.listar_prestamos()
                loan_id = self.employee_controller.input_id(
                    "\n   ID préstamo a eliminar: ", "PRE")
                self.loan_controller.eliminar_prestamo(loan_id)
                input("\n   Presione Enter para continuar...")
            elif op == "0":
                break
            else:
                print_colored("   ❌ Opción inválida", Colors.BRIGHT_RED)
                input("   Presione Enter para continuar...")

    def _menu_pagos(self):
        while True:
            clear_screen()
            print_header("GESTIÓN DE PAGOS")

            print_colored("\n   💰 OPCIONES:",
                          Colors.BRIGHT_GREEN + Colors.BOLD)
            print()
            print_colored("   1. ➕ Registrar pago", Colors.WHITE)
            print_colored("   2. 📖 Listar pagos", Colors.WHITE)
            print_colored("   3. ✏️ Actualizar pago", Colors.WHITE)
            print_colored("   4. 🗑 Eliminar pago", Colors.WHITE)
            print()
            print_colored("   0. 🔙 Volver", Colors.BRIGHT_CYAN)
            print()
            print_colored("-" * 40, Colors.BRIGHT_CYAN)
            print()

            op = input("   Opción: ")

            if op == "1":
                self.payment_controller.registrar_pago()
                input("\n   Presione Enter para continuar...")
            elif op == "2":
                self.payment_controller.listar_pagos()
                input("\n   Presione Enter para continuar...")
            elif op == "3":
                pag_id = self.employee_controller.input_id(
                    "   ID pago a actualizar: ", "PAG")
                self.payment_controller.actualizar_pago(pag_id)
                input("\n   Presione Enter para continuar...")
            elif op == "4":
                self.payment_controller.listar_pagos()
                pag_id = self.employee_controller.input_id(
                    "\n   ID pago a eliminar: ", "PAG")
                self.payment_controller.eliminar_pago(pag_id)
                input("\n   Presione Enter para continuar...")
            elif op == "0":
                break
            else:
                print_colored("   ❌ Opción inválida", Colors.BRIGHT_RED)
                input("   Presione Enter para continuar...")

    def _menu_consultar(self):
        while True:
            clear_screen()
            print_header("CONSULTAS")

            print_colored("\n   🔍 OPCIONES:",
                          Colors.BRIGHT_GREEN + Colors.BOLD)
            print()
            print_colored("   1. Ver todos los empleados", Colors.WHITE)
            print_colored("   2. Ver todos los préstamos", Colors.WHITE)
            print_colored("   3. Ver todos los pagos", Colors.WHITE)
            print_colored("   4. Buscar empleado por ID", Colors.WHITE)
            print_colored("   5. Buscar préstamo por ID", Colors.WHITE)
            print()
            print_colored("   0. 🔙 Volver", Colors.BRIGHT_CYAN)
            print()
            print_colored("-" * 40, Colors.BRIGHT_CYAN)
            print()

            op = input("   Opción: ")

            if op == "1":
                clear_screen()
                self.employee_controller.listar_empleados()
                input("\n   Presione Enter para continuar...")
            elif op == "2":
                clear_screen()
                self.loan_controller.listar_prestamos()
                input("\n   Presione Enter para continuar...")
            elif op == "3":
                clear_screen()
                self.payment_controller.listar_pagos()
                input("\n   Presione Enter para continuar...")
            elif op == "4":
                emp_id = self.employee_controller.input_id(
                    "   ID empleado: ", "EMP")
                emp = self.employee_controller.buscar_por_id(
                    self.employee_controller.empleados, emp_id
                )
                clear_screen()
                if emp:
                    self.payment_controller.consultar_empleado_detalle(emp)
                else:
                    print_colored("   ❌ No encontrado", Colors.BRIGHT_RED)
                input("\n   Presione Enter para continuar...")
            elif op == "5":
                loan_id = self.employee_controller.input_id(
                    "   ID préstamo: ", "PRE")
                prestamo = self.loan_controller.buscar_por_id(
                    self.loan_controller.prestamos, loan_id
                )
                clear_screen()
                if prestamo:
                    print_colored(
                        f"\n   📋 {prestamo.mostrar()}", Colors.BRIGHT_CYAN)
                    pagos = [
                        p for p in self.payment_controller.pagos if p.prestamo.id == loan_id]
                    if pagos:
                        print_colored("\n   Pagos realizados:",
                                      Colors.BRIGHT_GREEN)
                        for p in pagos:
                            print(f"     {p.mostrar()}")
                    else:
                        print_colored(
                            "\n   Sin pagos registrados", Colors.YELLOW)
                else:
                    print_colored("   ❌ No encontrado", Colors.BRIGHT_RED)
                input("\n   Presione Enter para continuar...")
            elif op == "0":
                break
            else:
                print_colored("   ❌ Opción inválida", Colors.BRIGHT_RED)
                input("   Presione Enter para continuar...")
