# TECHNICAL_REVIEW — MiniWaze-GUI-App

Fecha de revisión: 2026-07-16
Método: análisis estático + ejecución de la suite (`pytest tests/test_logic.py` → 1/1 pasa). Enunciado: `docs/Proyecto Programado 2 - SI 2023 - MiniWaze.md`.

## 1. Comprensión del proyecto

Navegador de rutas estilo Waze en **Python + Tkinter** (~870 LOC): carga un mapa desde CSV, construye un grafo, calcula rutas con **Dijkstra sobre heap binario** (`heapq`) y las dibuja en un canvas; incluye login básico de usuarios desde archivo.

## 2. Cumplimiento y calidad

| Aspecto | Estado | Evidencia |
|---|---|---|
| Grafo + ruta óptima | ✅ ejecutado | `models/pathfinder.py` — Dijkstra con priority queue; test `tests/test_logic.py` pasa |
| Carga de mapa CSV | 🟦 | `models/map_loader.py`, `data/mapa.csv` |
| Usuarios | 🟦 | `models/user_manager.py`, `data/Usuarios.txt` |
| UI Tkinter (login, ventana principal, canvas) | 🟦 | `ui/` (3 módulos) |
| CI **ejecuta pytest** | ✅ | `.github/workflows/ci.yml` — uno de los pocos repos del portafolio con tests corriendo en CI |

## 3. Fortalezas

1. Dijkstra idiomático con `heapq` (O((V+E) log V)) — contrasta con la versión C++ del portafolio y demuestra el algoritmo en dos lenguajes.
2. Separación models/ui/data real: la lógica se testea sin Tkinter.
3. CI que instala pytest y ejecuta la suite — patrón a replicar en los demás repos.

## 4. Debilidades y riesgos

| Hallazgo | Severidad | Nota |
|---|---|---|
| Contraseñas en texto plano en `data/Usuarios.txt` (datos seed: `ccampos;123`) | Baja-Media | Aceptable como fixture académico; hashear sería 10 líneas y elimina la mala señal |
| Suite mínima (1 test) | Media | El pathfinder amerita casos: sin ruta, mismo origen/destino, pesos |
| `tests/reproduce_issue.py` — script de depuración residual | Baja | Eliminar o convertir en test |
| Typos en README ("gestióna") | Baja | |

## 5. Evaluación profesional

- Nivel demostrado: **Junior+**. Correcto, testeable, con el algoritmo bien implementado; alcance pequeño.
- Rol en el portafolio: refuerza Python y grafos; su valor único es mostrar **Dijkstra en un segundo lenguaje** y el patrón CI-con-tests.

## 6. Recomendaciones

Ver `IMPROVEMENT_ROADMAP.md`. P1: ampliar la suite del pathfinder (esfuerzo mínimo, alto retorno).
