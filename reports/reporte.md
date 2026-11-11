# Reporte Técnico: Simulación y Análisis del Modelo Lotka–Volterra

**Fecha:** 5 de noviembre de 2026  
**Autor:** Agente Graficador  
**Modelo:** Ecuaciones Depredador-Presa de Lotka–Volterra integradas mediante el método de Euler explícito  

---

## 1. Resumen de Cambios: Archivos y Funciones Creados o Modificados

Conforme a las directrices de diseño y a las restricciones de aislamiento del proyecto:
- **`src/` y `tests/` permanecieron intactos** por parte de este agente (respetando la separación de responsabilidades con `revisor_numerico` y `tester_fisico`).
- **Archivos creados en `scripts/`**:
  - [`scripts/barrido.py`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/scripts/barrido.py): Script de automatización que realiza los barridos paramétricos y de condiciones iniciales, configurando estilos vectoriales y exportando las figuras.
    - `configurar_estilo()`: Configura fuentes serif, rejillas, anchos de línea y tamaños legibles para publicación.
    - `graficar_barrido_a(output_dir)`: Genera la comparativa para $a \in \{0.8, 1.0, 1.2\}$.
    - `graficar_barrido_b(output_dir)`: Genera la comparativa para $b \in \{0.05, 0.1, 0.2\}$.
    - `graficar_barrido_ci(output_dir)`: Genera la comparativa para condiciones iniciales $(8,8)$, $(10,10)$ y $(12,12)$.
    - `main()`: Orquestador de generación de gráficos.
- **Archivos generados en `figs/`**:
  - [`figs/barrido_parametro_a.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_parametro_a.pdf) y `barrido_parametro_a.png`
  - [`figs/barrido_parametro_b.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_parametro_b.pdf) y `barrido_parametro_b.png`
  - [`figs/barrido_condiciones_iniciales.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_condiciones_iniciales.pdf) y `barrido_condiciones_iniciales.png`
- **Archivos creados en `reports/`**:
  - [`reports/reporte.md`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/reports/reporte.md): El presente informe técnico detallado.

---

## 2. Tabla de Errores y Orden de Convergencia

Se ejecutó el protocolo de análisis numérico implementado en [`tests/test_precision.py`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/tests/test_precision.py), comparando la aproximación numérica de Euler explícito frente a la solución analítica exacta en ausencia de depredadores ($y_0 = 0 \implies x(t) = x_0 e^{a t}$), con $x_0 = 10.0$, $a = 1.0$ en el intervalo $t \in [0, 2.0]$.

El error global se midió bajo la norma infinito $L_\infty = \max_{n} |x_n - x(t_n)|$:

| Paso Temporal $\Delta t$ | $N_{\text{pasos}}$ | Error $L_\infty$ | Factor de Reducción $\frac{E(\Delta t)}{E(\Delta t / 2)}$ | Orden Local Estimado $p$ |
| :---: | :---: | :---: | :---: | :---: |
| **0.10000** | 20 | 6.615561 | — | — |
| **0.05000** | 40 | 3.490674 | 1.8952 | 0.9224 |
| **0.02500** | 80 | 1.794883 | 1.9448 | 0.9596 |
| **0.01250** | 160 | 0.910352 | 1.9716 | 0.9794 |
| **0.00625** | 320 | 0.458472 | 1.9856 | 0.9896 |

### Análisis de Convergencia
- **Ajuste lineal en escala log-log** ($\log(E) = p \log(\Delta t) + C$):
  $$\mathbf{p = 0.9641 \approx 1.0}$$
- **Conclusión numérica**: A medida que $\Delta t \to 0$, el factor de reducción converge asintóticamente a $2.0$ y el orden estimado tiende a $1.00$. Esto confirma rigurosamente que el algoritmo de Euler explícito implementado en [`src/lv.py`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/src/lv.py) exhibe consistencia global de primer orden $\mathcal{O}(\Delta t)$.

---

## 3. Resultado de los Tests Físicos y Numéricos

Se ejecutó la suite completa de pruebas unitarias mediante `pytest -v tests/`, tras la auditoría científica y resolución de hallazgos, arrojando un resultado de **8 pruebas superadas de 8 (100% éxito)**:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\itapi\Desktop\CryoSoft\Taller Antigravity
collected 8 items

tests/test_fisica.py::test_positividad PASSED                            [ 12%]
tests/test_fisica.py::test_equilibrio PASSED                             [ 25%]
tests/test_fisica.py::test_cantidad_conservada PASSED                    [ 37%]
tests/test_fisica.py::test_sin_depredadores PASSED                       [ 50%]
tests/test_fisica.py::test_sin_presas PASSED                             [ 62%]
tests/test_fisica.py::test_dt_grande PASSED                              [ 75%]
tests/test_precision.py::test_orden_convergencia_euler PASSED            [ 87%]
tests/test_precision.py::test_orden_convergencia_sistema_acoplado PASSED [100%]

============================== 8 passed in 0.04s ==============================
```

- **Autoconvergencia del sistema acoplado no lineal**: Además de la solución escalar exacta, se verificó la convergencia del sistema completo 2D acoplado mediante error de Cauchy/Richardson ($p_x \approx 1.04, p_y \approx 1.01$).

### Resumen Detallado de Pruebas Físicas:
1. **`test_positividad`**: Superado. Para condiciones iniciales biológicamente válidas ($x_0>0, y_0>0$) y $\Delta t = 0.01$, las trayectorias no cruzan el cero ni generan poblaciones negativas espurias.
2. **`test_equilibrio`**: Superado. Al iniciar exactamente en el punto fijo co-existente $(x^*, y^*) = (g/d, a/b) = (10, 10)$, las derivadas instantáneas se anulan y las poblaciones permanecen invariantes con tolerancia relativa estricta ($< 10^{-10}$).
3. **`test_cantidad_conservada`**: Superado. Se evalúa el invariante analítico $V(x, y) = d x - g \ln x + b y - a \ln y$. Como Euler explícito no es simpléctico, existe una deriva artificial no nula ($\Delta V > 0$), pero se demostró que dicha deriva decrece estrictamente al refinar el paso temporal ($\Delta V(\Delta t/2) < \Delta V(\Delta t)$).
4. **`test_sin_depredadores`**: Superado. Al anular $y_0 = 0$, los depredadores permanecen en cero y las presas crecen exponencialmente según la ley malthusiana analítica $x(t) = x_0 e^{at}$.
5. **`test_sin_presas`**: Superado. Al fijar $x_0 = 0$, las presas permanecen extintas y los depredadores decaen exponencialmente por mortalidad natural $y(t) = y_0 e^{-gt}$, reduciéndose el error numérico al disminuir $\Delta t$.
6. **`test_dt_grande`**: Superado. Al fijar un paso temporal excesivamente grande ($\Delta t = 0.5 \ge 0.2$), el integrador emite una advertencia preventiva explícita (`UserWarning`) informando sobre la inestabilidad potencial.
7. **`test_orden_convergencia_euler`**: Superado. Comprueba que el orden de convergencia experimental $p \in [0.95, 1.05]$.

---

## 4. Interpretación de Figuras

### Figura 1: Barrido del Parámetro $a$ (Tasa de Crecimiento de Presas)
*Archivo:* [`figs/barrido_parametro_a.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_parametro_a.pdf)  
*(Parámetros base: $b=0.1, d=0.1, g=1.0$, con $a \in \{0.8, 1.0, 1.2\}$, condición inicial $(x_0, y_0) = (12, 10)$, $\Delta t = 0.01$)*

- **Efecto biológico:** El parámetro $a$ modula la velocidad de reproducción de las presas. Al incrementarse de 0.8 a 1.2, se incrementa la disponibilidad de biomasa para los depredadores, desplazando verticalmente el equilibrio hacia arriba ($y^* = a/b \in \{8.0, 10.0, 12.0\}$), mientras el equilibrio de presas permanece estático en $x^* = g/d = 10.0$. Asimismo, la frecuencia de oscilación angular aumenta ($\omega \approx \sqrt{a g}$), acortando el período de las oscilaciones.
- **Efecto numérico (Euler explícito):** En el retrato de fase, las trayectorias no se cierran perfectamente sobre sí mismas, sino que forman una espiral abierta hacia afuera. Este ensanchamiento no es una propiedad ecológica del sistema depredador-presa clásico, sino un artefacto numérico intrínseco del método de Euler explícito, el cual inyecta energía artificialmente al sistema en cada paso.

### Figura 2: Barrido del Parámetro $b$ (Tasa de Depredación)
*Archivo:* [`figs/barrido_parametro_b.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_parametro_b.pdf)  
*(Parámetros base: $a=1.0, d=0.1, g=1.0$, con $b \in \{0.05, 0.1, 0.2\}$, condición inicial $(x_0, y_0) = (12, 10)$, $\Delta t = 0.01$)*

- **Efecto biológico:** El parámetro $b$ cuantifica la eficiencia con la que un depredador captura presas. A valores bajos ($b=0.05$), la ineficiencia de captura exige una población masiva de depredadores en equilibrio ($y^* = 20.0$) para contener a las presas, desencadenando ciclos de gran amplitud con picos de depredadores cercanos a 38 individuos. Para $b=0.2$, la alta presión depredadora deprime tanto la abundancia de presas que el equilibrio de carnívoros cae a $y^* = 5.0$, forzando a la población de presas a valles críticos cercanos a $3.5$ individuos.
- **Efecto numérico (Euler explícito):** En las trayectorias con mayores excursiones dinámicas ($b=0.05$), la no linealidad del término de interacción ($x \cdot y$) intensifica el error de truncamiento local, provocando una deriva de la energía y una espiral numérica hacia afuera más pronunciada que en los regímenes de baja amplitud.

### Figura 3: Barrido de Condiciones Iniciales en Torno al Equilibrio
*Archivo:* [`figs/barrido_condiciones_iniciales.pdf`](file:///c:/Users/itapi/Desktop/CryoSoft/Taller%20Antigravity/figs/barrido_condiciones_iniciales.pdf)  
*(Parámetros base: $a=1.0, b=0.1, d=0.1, g=1.0$, Equilibrio $(10.0, 10.0)$, CIs: $(8,8), (10,10), (12,12)$, $\Delta t = 0.01$)*

- **Efecto biológico:** Cuando el sistema parte exactamente en el punto de equilibrio $(10, 10)$, las tasas de natalidad igualan exactamente a las de mortalidad/depredación, por lo que el sistema permanece estrictamente constante en el tiempo (derivadas nulas). Las perturbaciones $(8, 8)$ y $(12, 12)$ demuestran el comportamiento de centro neutralmente estable del modelo continuo, donde cada condición inicial da origen a una órbita cerrada de amplitud característica.
- **Efecto numérico (Euler explícito):** Mientras que la órbita de equilibrio $(10, 10)$ permanece inmune a la deriva debido a que $\dot{x}=\dot{y}=0$, las trayectorias oscilatorias $(8, 8)$ y $(12, 12)$ revelan claramente la espiral divergente progresiva producida por Euler hacia el exterior. Esto ilustra nítidamente la violación de la ley de conservación del invariante analítico $V(x, y)$ generada por la discretización temporal hacia adelante.

---

## 5. Limitaciones del Método Numérico y Próximos Pasos

### Limitaciones de Euler Explícito en Modelos Lotka–Volterra
1. **Falta de conservación geométrica / simpléctica:** El sistema Lotka–Volterra posee una estructura Poisson no lineal y admite una primera integral invariante $V(x, y)$. Euler explícito sistemáticamente añade energía numérica ($\Delta V > 0$), convirtiendo centros neutrales cerrados en focos inestables con espirales divergentes artificiales.
2. **Primer orden de convergencia $\mathcal{O}(\Delta t)$:** La tasa de reducción del error es lineal, exigiendo tamaños de paso extremadamente pequeños ($\Delta t \ll 0.001$) y alto costo computacional para simulaciones prolongadas si se requiere precisión cuantitativa en los picos de población.
3. **Condicionalmente estable y pérdida de positividad:** Para perturbaciones severas o pasos temporales moderados ($\Delta t \ge 0.2$), el método puede violar la positividad biológica intrínseca ($x < 0$ o $y < 0$) o divergencias numéricas catastróficas.

### Próximos Pasos Recomendados
1. **Implementación de Métodos de Mayor Orden:** Incorporar Runge–Kutta de 4to orden (RK4) para abatir drásticamente el error de truncamiento local a $\mathcal{O}(\Delta t^4)$, reduciendo la tasa de dispersión espiral para un mismo costo computacional.
2. **Integradores Simplécticos o Preservadores de Invariantes:** Implementar esquemas no convencionales adaptados a sistemas conservativos (por ejemplo, el método del punto medio implícito, Euler simpléctico en coordenadas logarítmicas o algoritmos con proyección sobre la variedad $V(x,y)=\text{cte}$), garantizando ciclos cerrados sin deriva energética artificial a lo largo de tiempos arbitrariamente largos.
3. **Generalización Ecológica:** Incorporar capacidad de carga ambiental mediante un término logístico en las presas ($a x (1 - x/K)$), transformando el sistema de conservativo a disipativo con la aparición de ciclos límite estables o equilibrios asintóticamente estables más robustos frente a aproximaciones numéricas.
