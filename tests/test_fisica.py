"""Tests de coherencia física y biológica para el modelo de Lotka–Volterra."""

import sys
from pathlib import Path
import numpy as np
import pytest

# Asegurar que src esté en el sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lv import resolver_lotka_volterra, calcular_invariante


def test_positividad():
    """1. test_positividad: con x0 > 0, y0 > 0 y delta t razonable, x e y nunca son negativos."""
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    x0 = 10.0
    y0 = 5.0
    dt = 0.01
    t_max = 15.0

    t, x, y = resolver_lotka_volterra(
        x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g
    )

    assert np.all(x >= 0.0), f"Existen presas con valores negativos: min(x) = {np.min(x)}"
    assert np.all(y >= 0.0), f"Existen depredadores con valores negativos: min(y) = {np.min(y)}"
    assert np.all(x > 0.0), f"Las presas no deberían extinguirse completamente con estas condiciones: min(x) = {np.min(x)}"
    assert np.all(y > 0.0), f"Los depredadores no deberían extinguirse completamente: min(y) = {np.min(y)}"


def test_equilibrio():
    """2. test_equilibrio: con x0 = g/d e y0 = a/b, las poblaciones se mantienen constantes (tolerancia relativa 1e-10)."""
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    x0 = g / d  # 10.0
    y0 = a / b  # 10.0
    dt = 0.01
    t_max = 10.0

    t, x, y = resolver_lotka_volterra(
        x0=x0, y0=y0, t_max=t_max, dt=dt, a=a, b=b, d=d, g=g
    )

    # Las poblaciones deben ser constantes con tolerancia relativa 1e-10
    assert np.allclose(x, x0, rtol=1e-10, atol=1e-10), (
        f"La población de presas no se mantuvo en equilibrio: max diff = {np.max(np.abs(x - x0))}"
    )
    assert np.allclose(y, y0, rtol=1e-10, atol=1e-10), (
        f"La población de depredadores no se mantuvo en equilibrio: max diff = {np.max(np.abs(y - y0))}"
    )


def test_cantidad_conservada():
    """3. test_cantidad_conservada: V = d*x - g ln x + by - a ln y deriva con Euler, pero la deriva disminuye al reducir delta t."""
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    x0 = 15.0
    y0 = 8.0
    t_max = 5.0
    dt1 = 0.02
    dt2 = dt1 / 2.0  # 0.01

    _, x1, y1 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt1, a=a, b=b, d=d, g=g)
    _, x2, y2 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt2, a=a, b=b, d=d, g=g)

    v1 = calcular_invariante(x1, y1, a=a, b=b, d=d, g=g)
    v2 = calcular_invariante(x2, y2, a=a, b=b, d=d, g=g)

    # Deriva numérica máxima con respecto al valor inicial
    deriva1 = np.max(np.abs(v1 - v1[0]))
    deriva2 = np.max(np.abs(v2 - v2[0]))

    # Euler explícito no conserva la cantidad exactamente, por lo que debe haber deriva
    assert deriva1 > 0.0, "Se esperaba deriva numérica no nula con Euler explícito"
    # La deriva debe disminuir al reducir delta t (dt2 < dt1)
    assert deriva2 < deriva1, (
        f"La deriva no disminuyó al reducir dt a la mitad: deriva(dt1)={deriva1:.6e}, deriva(dt2)={deriva2:.6e}"
    )


def test_sin_depredadores():
    """4. test_sin_depredadores: con y0 = 0, x(t) se acerca a x0 * e^(at) y el error disminuye al reducir delta t."""
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    x0 = 10.0
    y0 = 0.0
    t_max = 2.0
    dt1 = 0.02
    dt2 = dt1 / 2.0  # 0.01

    t1, x1, y1 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt1, a=a, b=b, d=d, g=g)
    t2, x2, y2 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt2, a=a, b=b, d=d, g=g)

    # Sin depredadores, y(t) debe permanecer idénticamente en 0
    assert np.allclose(y1, 0.0), f"Los depredadores deberían ser 0: max(y1) = {np.max(y1)}"
    assert np.allclose(y2, 0.0), f"Los depredadores deberían ser 0: max(y2) = {np.max(y2)}"

    # Solución analítica para x(t): x0 * exp(a * t)
    x_exacta1 = x0 * np.exp(a * t1)
    x_exacta2 = x0 * np.exp(a * t2)

    error1 = np.max(np.abs(x1 - x_exacta1))
    error2 = np.max(np.abs(x2 - x_exacta2))

    # Cota superior de error y verificación de reducción coherente con orden 1
    assert error1 < 1.5, f"Error numérico excesivo para dt1: {error1}"
    assert error2 < error1, (
        f"El error analítico no disminuyó al reducir dt: error(dt1)={error1:.6e}, error(dt2)={error2:.6e}"
    )
    ratio = error1 / error2
    assert 1.7 <= ratio <= 2.3, f"El factor de reducción ({ratio:.2f}) no es consistente con orden 1"


def test_sin_presas():
    """5. test_sin_presas: con x0 = 0, y(t) se acerca a y0 * e^(-gt)."""
    a = 1.0
    b = 0.1
    d = 0.1
    g = 1.0
    x0 = 0.0
    y0 = 10.0
    t_max = 2.0
    dt1 = 0.02
    dt2 = dt1 / 2.0  # 0.01

    t1, x1, y1 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt1, a=a, b=b, d=d, g=g)
    t2, x2, y2 = resolver_lotka_volterra(x0=x0, y0=y0, t_max=t_max, dt=dt2, a=a, b=b, d=d, g=g)

    # Sin presas, x(t) debe permanecer idénticamente en 0
    assert np.allclose(x1, 0.0), f"Las presas deberían ser 0: max(x1) = {np.max(x1)}"
    assert np.allclose(x2, 0.0), f"Las presas deberían ser 0: max(x2) = {np.max(x2)}"

    # Solución analítica para y(t): y0 * exp(-g * t)
    y_exacta1 = y0 * np.exp(-g * t1)
    y_exacta2 = y0 * np.exp(-g * t2)

    error1 = np.max(np.abs(y1 - y_exacta1))
    error2 = np.max(np.abs(y2 - y_exacta2))

    # El error respecto a la solución analítica debe ser razonablemente pequeño y decrecer con dt
    assert error1 < 0.2, f"Error numérico excesivo para dt1: {error1}"
    assert error2 < error1, (
        f"El error analítico no disminuyó al reducir dt: error(dt1)={error1:.6e}, error(dt2)={error2:.6e}"
    )


def test_dt_grande():
    """6. test_dt_grande: con un delta t demasiado grande (p. ej. 0.5), el código advierte de forma explícita."""
    dt_grande = 0.5
    with pytest.warns(UserWarning, match="excesivamente grande"):
        resolver_lotka_volterra(
            x0=10.0, y0=5.0, t_max=2.0, dt=dt_grande, a=1.0, b=0.1, d=0.1, g=1.0
        )
