"""
Utilidades de consola: gotoxy, colores, limpieza de pantalla.
Portable para Windows, Linux y Mac.
"""

import os
import platform

# =========================
# LIMPIAR PANTALLA
# =========================


def clear_screen():
    """Limpia la pantalla de la consola"""
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:  # Linux, Mac
        os.system("clear")


# =========================
# GOTOXY (posicionar cursor)
# =========================

def gotoxy(x, y):
    """
    Mueve el cursor a la posición (x, y) en la consola.
    x = columna, y = fila (empieza en 1)
    """
    print(f"\033[{y};{x}H", end="")


# =========================
# COLORES ANSI
# =========================

class Colors:
    """Códigos ANSI para colores en consola"""
    # Reset
    RESET = "\033[0m"

    # Estilos
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"

    # Colores de texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Colores de fondo
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Colores brillantes
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def color_text(text, color):
    """Aplica color a un texto"""
    return f"{color}{text}{Colors.RESET}"


def print_colored(text, color, end="\n"):
    """Imprime texto coloreado"""
    print(f"{color}{text}{Colors.RESET}", end=end)


# =========================
# BORDES Y RECUADROS
# =========================

def draw_box(x1, y1, x2, y2, color=Colors.CYAN):
    """
    Dibuja un recuadro desde (x1,y1) hasta (x2,y2)
    """
    gotoxy(x1, y1)
    print_colored("┌" + "─" * (x2 - x1 - 1) + "┐", color)

    for y in range(y1 + 1, y2):
        gotoxy(x1, y)
        print_colored("│", color)
        gotoxy(x2, y)
        print_colored("│", color)

    gotoxy(x1, y2)
    print_colored("└" + "─" * (x2 - x1 - 1) + "┘", color)


def draw_title(x, y, title, color=Colors.BRIGHT_CYAN):
    """Dibuja un título centrado en un recuadro"""
    gotoxy(x, y)
    print_colored("╔" + "═" * (len(title) + 4) + "╗", color)
    gotoxy(x, y + 1)
    print_colored(f"║  {title}  ║", color)
    gotoxy(x, y + 2)
    print_colored("╚" + "═" * (len(title) + 4) + "╝", color)


def draw_menu_option(x, y, number, text, color=Colors.YELLOW):
    """Dibuja una opción de menú"""
    gotoxy(x, y)
    print_colored(f"[{number}]", Colors.BRIGHT_GREEN, end="")
    print(f" {text}")


def print_header(title):
    """Imprime un encabezado bonito"""
    clear_screen()
    print_colored("═" * 50, Colors.BRIGHT_CYAN)
    print_colored(f"   {title}", Colors.BRIGHT_YELLOW + Colors.BOLD)
    print_colored("═" * 50, Colors.BRIGHT_CYAN)
    print()
