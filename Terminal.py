#!/usr/bin/env python3
# imprime_wasd.py
from typing import Optional

ANSI_COLORS = {
    "black": "\033[30m", "red": "\033[31m", "green": "\033[32m",
    "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
    "cyan": "\033[36m", "white": "\033[37m",
    "bright_black": "\033[90m", "bright_red": "\033[91m",
    "bright_green": "\033[92m", "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m", "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m", "bright_white": "\033[97m",
}
ANSI_RESET = "\033[0m"


def print_wasd(text: str = "usa las teclas wasd",
               color: Optional[str] = "bright_green",
               use_unicode: bool = True):
    """
    Imprime la frase y las teclas W A S D con forma de tecla (W arriba, A S D abajo).
    Args:
        text: texto que aparecerá encima del dibujo.
        color: nombre de color ANSI o None.
        use_unicode: si False usa caracteres ASCII en vez de box-drawing.
    """
    color_pref = ANSI_COLORS.get(color, "") if color else ""
    color_suf = ANSI_RESET if color_pref else ""

    # Dos variantes: unicode con box-drawing, y fallback ASCII
    if use_unicode:
        # cajas con bordes Unicode. Mantener espacios para alinear bien.
        lines = [
            f"      ┌───┐      ",
            f"      │ W │      ",
            f"  ┌───┐┌───┐┌───┐ ",
            f"  │ A ││ S ││ D │ ",
            f"  └───┘└───┘└───┘ "
        ]
    else:
        # fallback ASCII (menos elegante)
        lines = [
            "      +---+      ",
            "      | W |      ",
            "  +---++---++---+ ",
            "  | A || S || D | ",
            "  +---++---++---+ "
        ]

    # Imprimir texto centrado respecto al ancho del dibujo
    width = len(lines[0])
    for i, line in enumerate([text] + [""] + lines):
        if i == 0:
            # centrar el texto simple
            print(color_pref + text.center(width) + color_suf)
            # imprimir una línea vacía entre texto y teclas
            print()
            # ahora las teclas
            for l in lines:
                print(color_pref + l + color_suf)
            break


#!/usr/bin/env python3
"""
banner_terminal.py

Función para imprimir un letrero bonito en la terminal que acepta texto multilínea.
"""

from typing import Optional

# Mapita simple de colores ANSI (puedes ampliarlo)
ANSI_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m",
}
ANSI_RESET = "\033[0m"


def print_banner(
    text: str,
    width: Optional[int] = None,
    padding: int = 1,
    border_char: str = "*",
    corner_char: Optional[str] = None,
    title: Optional[str] = None,
    align: str = "center",
    color: Optional[str] = None,
):
    """
    Imprime un letrero decorativo en la terminal.

    Args:
        text: Texto multilínea (usa '\n' para saltos)
        width: Ancho total del banner (incluye bordes). Si None, se calcula automáticamente.
        padding: Espacio en blanco (en caracteres) entre texto y borde.
        border_char: Carácter a usar para el borde horizontal y laterales.
        corner_char: Carácter para las esquinas (si None, usa border_char)
        title: Texto corto que aparecerá en la línea superior del borde (opcional).
        align: 'left', 'center' o 'right' — alineación del texto dentro del banner.
        color: nombre de color ANSI (p. ej. 'cyan' o 'bright_yellow') o None.
    """
    if corner_char is None:
        corner_char = border_char

    lines = text.splitlines() or [""]
    # calcular el ancho del contenido (el más largo de las líneas)
    content_width = max(len(line) for line in lines)

    inner_width = content_width + 2 * padding

    # si el usuario dio un width, asegúrate de que sea suficiente
    min_total_width = inner_width + 2  # +2 por los bordes verticales
    if width is not None:
        if width < min_total_width:
            # forzamos el ancho si es demasiado pequeño
            width = min_total_width
    else:
        width = min_total_width

    # ancho interior real para centrar/alinear el texto
    real_inner = width - 2

    # top border con posible título
    top_border = corner_char + border_char * (width - 2) + corner_char

    if title:
        # incrustar título en la parte superior si cabe
        t = f" {title} "
        if len(t) <= width - 2:
            left = (width - 2 - len(t)) // 2
            top_border = (
                corner_char
                + border_char * left
                + t
                + border_char * (width - 2 - left - len(t))
                + corner_char
            )

    # aplicar color si se pidió
    color_prefix = ANSI_COLORS.get(color, "") if color else ""
    color_suffix = ANSI_RESET if color_prefix else ""

    print(color_prefix + top_border + color_suffix)

    # líneas de contenido
    for line in lines:
        # recortar si la línea es más larga que el espacio permitido
        if len(line) > real_inner - 2 * padding:
            line = line[: real_inner - 2 * padding]

        if align == "left":
            padded = " " * padding + line.ljust(real_inner - 2 * padding) + " " * padding
        elif align == "right":
            padded = " " * padding + line.rjust(real_inner - 2 * padding) + " " * padding
        else:  # center
            padded = " " * padding + line.center(real_inner - 2 * padding) + " " * padding

        print(color_prefix + border_char + padded + border_char + color_suffix)

    # bottom border (simétrica)
    bottom_border = corner_char + border_char * (width - 2) + corner_char
    print(color_prefix + bottom_border + color_suffix)


# Ejemplos de uso
if __name__ == "__main__":
    texto = """Bienvenido al simulador
        Configuración por defecto:
        - Integrador: Verlet
        - Caja: rebotes
        ¡Disfruta!"""

    print_banner(texto, padding=2, border_char="═", corner_char="╔", title=" SIMULADOR ", align="center", color="bright_cyan")
