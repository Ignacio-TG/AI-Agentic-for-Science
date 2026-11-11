"""Test de precisión numérica y orden de convergencia para el modelo Lotka–Volterra."""

import sys
from pathlib import Path
import numpy as np
import pytest

# Asegurar que src esté en el sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lv import resolver_lotka_volterra


def test_orden_convergencia_euler():
    """Verifica que el método de Euler explícito tenga orden de convergencia ≈ 1.

    Para y0 = 0, el sistema se reduce a:
        dx/dt = a * x
        x(t) = x0 * exp(a * t)
    """
    x0 = 10.0
    y0 = 0.0
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    t_max = 2.0

    # Lista de pasos temporales decrecientes
    dt_list = [0.1, 0.05, 0.025, 0.0125, 0.00625]
    errores = []

    for dt in dt_list:
        t, x, _ = resolver_lotka_volterra(
            x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g, dt_max_warn=1.0
        )
        x_exacta = x0 * np.exp(a * t)
        # Error en norma infinito a lo largo de toda la trayectoria
        error_inf = np.max(np.abs(x - x_exacta))
        errores.append(error_inf)

    errores = np.array(errores)
    dt_arr = np.array(dt_list)

    # Estimación del orden mediante regresión lineal en log-log: log(error) = p * log(dt) + C
    p, _ = np.polyfit(np.log(dt_arr), np.log(errores), 1)

    # Verificación de monotonía decreciente del error
    assert np.all(np.diff(errores) < 0), "El error debe disminuir monótonamente al reducir dt"

    # Verificación de que el orden de convergencia es aproximadamente 1 (Euler explícito)
    # Tolerancia razonable: 0.95 <= p <= 1.05
    assert 0.95 <= p <= 1.05, f"El orden observado ({p:.4f}) difiere del orden teórico 1.0"


def test_orden_convergencia_sistema_acoplado():
    """Verifica el orden de convergencia ≈ 1 en el sistema no lineal acoplado completo.

    Usa condiciones iniciales no triviales x0 > 0, y0 > 0 y autoconvergencia
    (Richardson / Cauchy error) con refinamiento sucesivo por factor 2:
        ||u_{dt} - u_{dt/2}||_inf / ||u_{dt/2} - u_{dt/4}||_inf ≈ 2^p
    """
    x0, y0 = 12.0, 8.0
    a, b, d_param, g = 1.0, 0.1, 0.1, 1.0
    t_max = 2.0

    dt_base = 0.08
    sols = []
    dts = [dt_base / (2**i) for i in range(4)]  # [0.08, 0.04, 0.02, 0.01]

    for dt_val in dts:
        _, x, y = resolver_lotka_volterra(
            x0=x0, y0=y0, t_max=t_max, dt=dt_val, a=a, b=b, d=d_param, g=g, dt_max_warn=1.0
        )
        sols.append((x, y))

    # Diferencias en la malla de paso más grueso correspondiente al refinar por factor 2
    diff1_x = np.max(np.abs(sols[0][0] - sols[1][0][::2]))
    diff2_x = np.max(np.abs(sols[1][0] - sols[2][0][::2]))
    diff3_x = np.max(np.abs(sols[2][0] - sols[3][0][::2]))

    diff1_y = np.max(np.abs(sols[0][1] - sols[1][1][::2]))
    diff2_y = np.max(np.abs(sols[1][1] - sols[2][1][::2]))
    diff3_y = np.max(np.abs(sols[2][1] - sols[3][1][::2]))

    # Verificación de monotonía decreciente del error
    assert diff2_x < diff1_x and diff3_x < diff2_x, "El error de presas debe decrecer al refinar dt"
    assert diff2_y < diff1_y and diff3_y < diff2_y, "El error de depredadores debe decrecer al refinar dt"

    # Órdenes de convergencia observados
    px = np.log2(diff2_x / diff3_x)
    py = np.log2(diff2_y / diff3_y)

    # Tolerancia: orden en [0.95, 1.10] consistente con Euler explícito (p=1.0)
    assert 0.95 <= px <= 1.10, f"Orden observado en presas acopladas ({px:.4f}) difiere de 1.0"
    assert 0.95 <= py <= 1.10, f"Orden observado en depredadores acoplados ({py:.4f}) difiere de 1.0"
