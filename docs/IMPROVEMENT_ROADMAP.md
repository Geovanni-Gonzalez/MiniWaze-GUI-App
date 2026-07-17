# IMPROVEMENT_ROADMAP — MiniWaze-GUI-App

Backlog priorizado. Impacto/Esfuerzo: Alto/Medio/Bajo.

## Quick Wins

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 1 | Ampliar `tests/test_logic.py`: sin ruta, origen=destino, empates de peso, grafo desconexo (CI ya los ejecutaría) | Alto | Bajo | P1 |
| 2 | Eliminar `tests/reproduce_issue.py` o convertirlo en test formal | Medio | Bajo | P1 |
| 3 | Hashear las contraseñas de `Usuarios.txt` (`hashlib.sha256`) — elimina la mala señal de texto plano | Medio | Bajo | P1 |
| 4 | GitHub Topics: `python`, `tkinter`, `dijkstra`, `graphs`, `pathfinding` + descripción; corregir typos del README | Medio | Bajo | P1 |

## Mejoras técnicas

| # | Mejora | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| 5 | A* como alternativa seleccionable (heurística euclidiana — las coordenadas ya existen para el canvas) | Medio | Medio | P2 |
| 6 | Captura del canvas con una ruta resaltada en el README | Medio | Bajo | P2 |

## Mejoras arquitectónicas

Ninguna prioritaria: el alcance actual es coherente.

## Mejoras de GitHub

Ya presentes: badge CI (con pytest ejecutándose — mejor que la mayoría del portafolio), LICENSE, enunciado en docs. Faltan: Topics (item 4).
