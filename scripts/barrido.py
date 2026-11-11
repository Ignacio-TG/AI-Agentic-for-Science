"""Script de barrido de parámetros y condiciones iniciales para Lotka–Volterra.

Genera figuras en formato PDF vectorial (y PNG auxiliar) en la carpeta figs/:
1. figs/barrido_parametro_a.pdf: barrido de a = [0.8, 1.0, 1.2]
2. figs/barrido_parametro_b.pdf: barrido de b = [0.05, 0.1, 0.2]
3. figs/barrido_condiciones_iniciales.pdf: condiciones iniciales (8,8), (10,10), (12,12)
"""

from __future__ import annotations
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Configurar ruta a src
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from lv import resolver_lotka_volterra, calcular_invariante, DEFAULT_PARAMS


def configurar_estilo() -> None:
    """Configura el estilo visual de matplotlib para publicaciones e informes."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9.5,
        "figure.titlesize": 14,
        "lines.linewidth": 1.8,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
    })


def graficar_barrido_a(output_dir: Path) -> None:
    """Barrido de parámetro a = [0.8, 1.0, 1.2] con b=0.1, d=0.1, g=1.0."""
    a_vals = [0.8, 1.0, 1.2]
    b = 0.1
    d = 0.1
    g = 1.0
    x0, y0 = 12.0, 10.0
    t_max = 25.0
    dt = 0.01

    colores = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    fig, (ax_t, ax_phase) = plt.subplots(1, 2, figsize=(13, 5.2), constrained_layout=True)

    for a, col in zip(a_vals, colores):
        t, x, y = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g)
        x_eq = g / d
        y_eq = a / b

        # Series temporales
        ax_t.plot(t, x, color=col, linestyle="-", label=f"Presas $x(t)$ ($a={a}$)")
        ax_t.plot(t, y, color=col, linestyle="--", label=f"Depredadores $y(t)$ ($a={a}$)")

        # Retrato de fase
        ax_phase.plot(x, y, color=col, linestyle="-", label=f"Órbita ($a={a}$)")
        ax_phase.scatter(
            [x_eq], [y_eq], color=col, marker="*", s=140, zorder=5,
            edgecolors="black", linewidths=0.8, label=f"Eq. ({x_eq:.1f}, {y_eq:.1f})"
        )

    # Punto inicial común
    ax_phase.scatter([x0], [y0], color="black", marker="o", s=45, zorder=6, label=f"Inicio ({x0:.0f}, {y0:.0f})")

    ax_t.set_title("Series Temporales $x(t)$ e $y(t)$")
    ax_t.set_xlabel("Tiempo $t$ [unidades de tiempo]")
    ax_t.set_ylabel("Población [individuos]")
    ax_t.grid(True)
    ax_t.legend(loc="upper right", framealpha=0.9, ncol=1)

    ax_phase.set_title("Retrato de Fase ($x$ vs $y$)")
    ax_phase.set_xlabel("Presas $x$ [individuos]")
    ax_phase.set_ylabel("Depredadores $y$ [individuos]")
    ax_phase.grid(True)
    ax_phase.legend(loc="upper right", framealpha=0.9)

    fig.suptitle(
        f"Barrido de Parámetro $a$ (Tasa de Crecimiento de Presas) — $(x_0, y_0)=({x0:.0f}, {y0:.0f})$, $dt={dt}$",
        fontsize=13, weight="bold"
    )

    pdf_path = output_dir / "barrido_parametro_a.pdf"
    png_path = output_dir / "barrido_parametro_a.png"
    fig.savefig(pdf_path, dpi=300)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"[OK] Generado: {pdf_path}")


def graficar_barrido_b(output_dir: Path) -> None:
    """Barrido de parámetro b = [0.05, 0.1, 0.2] con a=1.0, d=0.1, g=1.0."""
    b_vals = [0.05, 0.1, 0.2]
    a = 1.0
    d = 0.1
    g = 1.0
    x0, y0 = 12.0, 10.0
    t_max = 25.0
    dt = 0.01

    colores = ["#9467bd", "#e377c2", "#17becf"]
    fig, (ax_t, ax_phase) = plt.subplots(1, 2, figsize=(13, 5.2), constrained_layout=True)

    for b, col in zip(b_vals, colores):
        t, x, y = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g)
        x_eq = g / d
        y_eq = a / b

        # Series temporales
        ax_t.plot(t, x, color=col, linestyle="-", label=f"Presas $x(t)$ ($b={b}$)")
        ax_t.plot(t, y, color=col, linestyle="--", label=f"Depredadores $y(t)$ ($b={b}$)")

        # Retrato de fase
        ax_phase.plot(x, y, color=col, linestyle="-", label=f"Órbita ($b={b}$)")
        ax_phase.scatter(
            [x_eq], [y_eq], color=col, marker="*", s=140, zorder=5,
            edgecolors="black", linewidths=0.8, label=f"Eq. ({x_eq:.1f}, {y_eq:.1f})"
        )

    # Punto inicial común
    ax_phase.scatter([x0], [y0], color="black", marker="o", s=45, zorder=6, label=f"Inicio ({x0:.0f}, {y0:.0f})")

    ax_t.set_title("Series Temporales $x(t)$ e $y(t)$")
    ax_t.set_xlabel("Tiempo $t$ [unidades de tiempo]")
    ax_t.set_ylabel("Población [individuos]")
    ax_t.grid(True)
    ax_t.legend(loc="upper right", framealpha=0.9)

    ax_phase.set_title("Retrato de Fase ($x$ vs $y$)")
    ax_phase.set_xlabel("Presas $x$ [individuos]")
    ax_phase.set_ylabel("Depredadores $y$ [individuos]")
    ax_phase.grid(True)
    ax_phase.legend(loc="upper right", framealpha=0.9)

    fig.suptitle(
        f"Barrido de Parámetro $b$ (Tasa de Depredación) — $(x_0, y_0)=({x0:.0f}, {y0:.0f})$, $dt={dt}$",
        fontsize=13, weight="bold"
    )

    pdf_path = output_dir / "barrido_parametro_b.pdf"
    png_path = output_dir / "barrido_parametro_b.png"
    fig.savefig(pdf_path, dpi=300)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"[OK] Generado: {pdf_path}")


def graficar_barrido_ci(output_dir: Path) -> None:
    """Barrido de 3 condiciones iniciales alrededor del equilibrio (10, 10): (8,8), (10,10), (12,12)."""
    cis = [(8.0, 8.0), (10.0, 10.0), (12.0, 12.0)]
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    t_max = 25.0
    dt = 0.01

    colores = ["#d62728", "#2ca02c", "#1f77b4"]
    fig, (ax_t, ax_phase) = plt.subplots(1, 2, figsize=(13, 5.2), constrained_layout=True)

    x_eq = g / d
    y_eq = a / b

    for (x0, y0), col in zip(cis, colores):
        t, x, y = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g)

        etiqueta_ci = f"CI ({x0:.0f}, {y0:.0f})"
        # Series temporales
        ax_t.plot(t, x, color=col, linestyle="-", label=f"Presas $x(t)$ [{etiqueta_ci}]")
        ax_t.plot(t, y, color=col, linestyle="--", label=f"Depredadores $y(t)$ [{etiqueta_ci}]")

        # Retrato de fase
        ax_phase.plot(x, y, color=col, linestyle="-", label=f"Órbita {etiqueta_ci}")
        ax_phase.scatter([x0], [y0], color=col, marker="o", s=40, zorder=4)

    # Marcar el punto de equilibrio en el retrato de fase
    ax_phase.scatter(
        [x_eq], [y_eq], color="black", marker="*", s=180, zorder=6,
        edgecolors="gold", linewidths=1.2, label=f"Equilibrio ({x_eq:.1f}, {y_eq:.1f})"
    )

    ax_t.set_title("Series Temporales $x(t)$ e $y(t)$")
    ax_t.set_xlabel("Tiempo $t$ [unidades de tiempo]")
    ax_t.set_ylabel("Población [individuos]")
    ax_t.grid(True)
    ax_t.legend(loc="upper right", framealpha=0.9)

    ax_phase.set_title("Retrato de Fase ($x$ vs $y$)")
    ax_phase.set_xlabel("Presas $x$ [individuos]")
    ax_phase.set_ylabel("Depredadores $y$ [individuos]")
    ax_phase.grid(True)
    ax_phase.legend(loc="upper right", framealpha=0.9)

    fig.suptitle(
        f"Barrido de Condiciones Iniciales en Torno al Equilibrio — $a=1.0, b=0.1, d=0.1, g=1.0$, $dt={dt}$",
        fontsize=13, weight="bold"
    )

    pdf_path = output_dir / "barrido_condiciones_iniciales.pdf"
    png_path = output_dir / "barrido_condiciones_iniciales.png"
    fig.savefig(pdf_path, dpi=300)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)
    print(f"[OK] Generado: {pdf_path}")


def main() -> None:
    configurar_estilo()
    output_dir = BASE_DIR / "figs"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generando gráficos de barrido en figs/...")
    graficar_barrido_a(output_dir)
    graficar_barrido_b(output_dir)
    graficar_barrido_ci(output_dir)
    print("Barrido completado exitosamente.")


if __name__ == "__main__":
    main()
