"""Modelo de Lotka–Volterra integrado mediante el método de Euler explícito."""

from __future__ import annotations
import warnings
from typing import Tuple, Dict, Any
import numpy as np

# Parámetros base estándar del modelo
DEFAULT_PARAMS: Dict[str, float] = {
    "a": 1.0,   # Tasa de crecimiento de presas
    "b": 0.1,   # Tasa de depredación
    "d": 0.1,   # Eficiencia de conversión / reproducción de depredadores
    "g": 1.0,   # Tasa de mortalidad de depredadores
}


def calcular_invariante(
    x: np.ndarray | float,
    y: np.ndarray | float,
    a: float = 1.0,
    b: float = 0.1,
    d: float = 0.1,
    g: float = 1.0,
) -> np.ndarray | float:
    """Calcula la cantidad conservada V(x, y) = d*x - g*ln(x) + b*y - a*ln(y)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        val = d * x - g * np.log(x) + b * y - a * np.log(y)
    return val


def resolver_lotka_volterra(
    x0: float,
    y0: float,
    t_max: float,
    dt: float,
    a: float = 1.0,
    b: float = 0.1,
    d: float = 0.1,
    g: float = 1.0,
    dt_max_warn: float = 0.2,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integra el sistema Lotka–Volterra usando el método de Euler explícito.

    Ecuaciones:
        dx/dt = a*x - b*x*y
        dy/dt = d*x*y - g*y

    Discretización (Euler explícito):
        x[n+1] = x[n] + dt * (a*x[n] - b*x[n]*y[n])
        y[n+1] = y[n] + dt * (d*x[n]*y[n] - g*y[n])

    Retorna:
        t: array de tiempos [0, dt, 2*dt, ..., t_max]
        x: array con la población de presas en cada tiempo
        y: array con la población de depredadores en cada tiempo
    """
    if x0 < 0 or y0 < 0:
        raise ValueError(f"Las condiciones iniciales deben ser no negativas: x0={x0}, y0={y0}")
    if dt <= 0:
        raise ValueError(f"El paso temporal dt debe ser estrictamente positivo: dt={dt}")
    if t_max <= 0:
        raise ValueError(f"t_max debe ser mayor que 0: t_max={t_max}")
    if any(p <= 0 for p in (a, b, d, g)):
        raise ValueError(f"Los parámetros (a, b, d, g) deben ser estrictamente positivos: a={a}, b={b}, d={d}, g={g}")

    # Advertencia si dt es excesivamente grande respecto a la escala de estabilidad
    if dt >= dt_max_warn:
        warnings.warn(
            f"El paso dt={dt} es excesivamente grande (>= {dt_max_warn}). "
            "Euler explícito puede volverse numéricamente inestable o violar positividad.",
            UserWarning,
            stacklevel=2,
        )

    # Número de pasos discretos (el tiempo final simulado será n_pasos * dt)
    n_pasos = int(np.round(t_max / dt))
    t = np.linspace(0.0, n_pasos * dt, n_pasos + 1)

    x = np.empty(n_pasos + 1, dtype=float)
    y = np.empty(n_pasos + 1, dtype=float)

    x[0] = float(x0)
    y[0] = float(y0)

    for n in range(n_pasos):
        xn = x[n]
        yn = y[n]

        # Derivadas instantáneas
        dxdt = a * xn - b * xn * yn
        dydt = d * xn * yn - g * yn

        # Actualización de Euler explícito
        x_sig = xn + dt * dxdt
        y_sig = yn + dt * dydt

        if x_sig < 0.0 or y_sig < 0.0:
            warnings.warn(
                f"Violación de positividad numérica en paso n={n+1} (t={t[n+1]:.4f}): "
                f"x={x_sig:.4f}, y={y_sig:.4f}. Euler explícito se ha vuelto inestable.",
                RuntimeWarning,
                stacklevel=2,
            )

        x[n + 1] = x_sig
        y[n + 1] = y_sig

    return t, x, y
