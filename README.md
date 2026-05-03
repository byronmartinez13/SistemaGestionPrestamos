# 🏦 Sistema de Gestión de Préstamos para Empleados

Sistema de consola en Python para gestionar empleados, préstamos y pagos, con persistencia en archivos JSON. Desarrollado como práctica de Programación Orientada a Objetos aplicando herencia, mixins, interfaces abstractas, decoradores y separación por capas (MVC).

---

## 📋 Requisitos cumplidos

| Requisito                                         | Estado |
| ------------------------------------------------- | ------ |
| Programación Orientada a Objetos                  | ✅     |
| CRUD completo (Crear, Leer, Actualizar, Eliminar) | ✅     |
| Clases abstractas (ABC)                           | ✅     |
| Mixins reutilizables                              | ✅     |
| Decoradores personalizados                        | ✅     |
| Funciones de orden superior (map, filter, reduce) | ✅     |
| Persistencia en JSON                              | ✅     |
| Validación de cédula ecuatoriana                  | ✅     |
| Menú interactivo                                  | ✅     |

---

## 📁 Estructura del proyecto (MVC)

POO Sistema de gestión de prestamos/
├── main.py # Punto de entrada
├── README.md
│
├── models/ # M — Entidades de dominio
│ ├── init.py
│ ├── base.py # Clase base abstracta
│ ├── employee.py # Empleado
│ ├── loan.py # Préstamo
│ └── payment.py # Pago
│
├── views/ # V — Capa de presentación
│ ├── init.py
│ └── menu.py # Menús interactivos
│
├── controllers/ # C — Lógica de negocio
│ ├── init.py
│ ├── employee_controller.py # CRUD empleados
│ ├── loan_controller.py # CRUD préstamos
│ ├── payment_controller.py # CRUD pagos
│ └── stats_controller.py # Estadísticas
│
├── core/ # Infraestructura transversal
│ ├── init.py
│ ├── decorators.py # Decoradores personalizados
│ ├── interfaces.py # CrudInterface (ABC)
│ ├── json_manager.py # Persistencia JSON
│ └── mixins.py # Mixins reutilizables
│
└── data/ # Datos persistidos
├── employees.json
├── loans.json
└── payments.json

---

## 🏗️ Arquitectura por capas

┌─────────────────────────────────────────────────────┐
│ main.py → views/Menu (V — Presentación) │
└────────────────────────┬────────────────────────────┘
│ delega operaciones
▼
┌─────────────────────────────────────────────────────┐
│ controllers/ (C — Lógica negocio) │
│ - EmployeeController │
│ - LoanController │
│ - PaymentController │
│ - StatsController │
└────────────────────────┬────────────────────────────┘
│ opera sobre
▼
┌─────────────────────────────────────────────────────┐
│ models/ (M — Dominio) │
│ - Empleado / Prestamo / Pago │
└────────────────────────┬────────────────────────────┘
│ persiste mediante
▼
┌─────────────────────────────────────────────────────┐
│ core/JsonManager (Persistencia) │
└────────────────────────┬────────────────────────────┘
│ lee/escribe
▼
data/employees.json
data/loans.json
data/payments.json

---

## 🚀 Funcionalidades

### 👥 Gestión de Empleados (CRUD)

- **Crear**: Registro con validación de cédula ecuatoriana y nombre
- **Listar**: Muestra todos los empleados registrados
- **Actualizar**: Modificar nombre, cédula o sueldo
- **Eliminar**: Remover empleado (si no tiene préstamos activos)

### 📋 Gestión de Préstamos (CRUD)

- **Crear**: Asociar a empleado, definir monto, cuotas y fecha
- **Listar**: Ver todos los préstamos (activos/pagados)
- **Actualizar**: Modificar monto, cuotas o fecha
- **Eliminar**: Remover préstamo (si no tiene pagos asociados)

### 💰 Gestión de Pagos (CRUD)

- **Registrar**: Pagos que reducen el saldo del préstamo
- **Listar**: Historial de pagos realizados
- **Actualizar**: Modificar valor o fecha del pago
- **Eliminar**: Eliminar pago y revertir el saldo

### 🔍 Consultas

- Ver todos los empleados
- Ver todos los préstamos
- Ver todos los pagos
- Buscar empleado por ID (con detalle de préstamos y pagos)
- Buscar préstamo por ID (con detalle de pagos)

### 📊 Estadísticas

- Totales de préstamos y pagos
- Monto total, promedio, máximo y mínimo
- Préstamos pendientes vs pagados
- Saldo total pendiente

---

## 📦 Modelo de datos

### `employees.json`

```json
[
  {
    "id": "EMP-0001",
    "cedula": "1710034065",
    "nombre": "Juan Pérez",
    "sueldo": 1500.0
  }
]
```

### `loans.json`

```json
[
  {
    "id": "PRE-0001",
    "empleado": {
      "id": "EMP-0001",
      "nombre": "Juan Pérez",
      "cedula": "1710034065",
      "sueldo": 1500.0
    },
    "fecha": "2024-01-15",
    "monto": 5000.0,
    "cuotas": 12,
    "cuota": 416.67,
    "saldo": 5000.0
  }
]
```

### `payments.json`

```json
[
  {
    "id": "PAG-0001",
    "prestamo_id": "PRE-0001",
    "fecha": "2024-02-15",
    "valor": 416.67
  }
]
```

## 🛠️ Validaciones implementadas

|Validación | Descripción |
|✅ Cédula ecuatoriana | 10 dígitos, provincia válida, dígito verificador |
|✅ Nombre | Solo letras y espacios, no vacío |
|✅ Sueldo | Número positivo |
|✅ Monto | Número positivo |
|✅ Cuotas | Número entero positivo |
|✅ Fechas | Formato YYYY-MM-DD, no futura, no anterior al préstamo |
|✅ Pago | No mayor al saldo pendiente |
|✅ Valores negativos| No permitidos en ningún campo |

## 🔧 Conceptos POO aplicados

|Concepto | Dónde se aplica |
|Encapsulamiento | Modelos con propiedades privadas y métodos públicos |
|Herencia | Empleado(Base), Prestamo(Base), Pago(Base) |
|Clases abstractas | Base con @abstractmethod |
|Mixins | InputMixin, BuscarMixin, MostrarMixin, LogMixin|
|Decoradores | @validar_no_negativo, @validar_formato_id, @validar_existencia |
|Funciones de orden superior | map, filter, reduce, comprehensions en estadísticas |
|Separación por capas| MVC claro: models/views/controllers/core |

## 🖥️ Menú principal

=======================================================
🏦 SISTEMA DE GESTIÓN DE PRÉSTAMOS
=======================================================

1. 👥 Gestión de Empleados (CRUD)
2. 📋 Gestión de Préstamos (CRUD)
3. 💰 Gestión de Pagos (CRUD)
4. 🔍 Consultar / Reportes
5. 📊 Estadísticas
6. 🚪 Salir

### Submenú de Empleados

---

## 📋 GESTIÓN DE EMPLEADOS

1. ➕ Crear empleado
2. 📖 Listar empleados
3. ✏️ Actualizar empleado
4. 🗑 Eliminar empleado
5. 🔙 Volver

### Submenú de Préstamos

---

## 📋 GESTIÓN DE PRÉSTAMOS

1. ➕ Crear préstamo
2. 📖 Listar préstamos
3. ✏️ Actualizar préstamo
4. 🗑 Eliminar préstamo
5. 🔙 Volver

### Submenú de Pagos

---

## 💰 GESTIÓN DE PAGOS

1. ➕ Registrar pago
2. 📖 Listar pagos
3. ✏️ Actualizar pago
4. 🗑 Eliminar pago
5. 🔙 Volver

## ⚙️ Instalación y ejecución

### Requisitos

Python 3.8 o superior
No requiere dependencias externas (solo librería estándar)

### Pasos

Clonar o descargar el proyecto
Abrir terminal en la carpeta del proyecto

Ejecutar:
bash
python main.py
Primera ejecución
Los archivos JSON se crearán automáticamente en la carpeta data/ al registrar los primeros datos.

### 📝 Ejemplo de uso

1. Crear empleado: Ingresar nombre, cédula y sueldo
   → ID generado automáticamente: EMP-0001

2. Crear préstamo: Seleccionar empleado, ingresar monto y cuotas
   → ID generado: PRE-0001
   → Cuota mensual calculada automáticamente

3. Registrar pago: Seleccionar préstamo, ingresar valor
   → Saldo se reduce automáticamente

4. Consultar: Ver detalle completo de empleado con préstamos y pagos

5. Estadísticas: Ver resumen de todo el sistema

### 📊 Ejemplo de salida de estadísticas

==================================================
📊 ESTADÍSTICAS DEL SISTEMA
==================================================

👥 EMPLEADOS:
Total empleados: 3
Promedio sueldo: $1833.33
Sueldo máximo: $2500.00
Sueldo mínimo: $1200.00

📋 PRÉSTAMOS:
Total préstamos: 5
Monto total prestado: $25000.00
Promedio préstamo: $5000.00
Préstamo máximo: $10000.00
Préstamo mínimo: $2000.00
Préstamos activos: 3
Préstamos pagados: 2
Saldo pendiente total: $12500.00

💰 PAGOS:
Total pagos: 8
Monto total pagado: $12500.00
Promedio pago: $1562.50
Pago máximo: $2500.00
Pago mínimo: $500.00

## 🧪 Validación de cédula ecuatoriana

El sistema incluye validación completa de cédulas ecuatorianas:
10 dígitos numéricos
Provincia válida (01-24)
Tercer dígito < 6 (persona natural)
Algoritmo de dígito verificador
Cédulas de prueba válidas:
1710034065
0914192182
1724306740

## 👨‍💻 Autor

Desarrollado como proyecto de Programación Orientada a Objetos.

## 📄 Licencia

Proyecto educativo - Libre de uso y modificación.
