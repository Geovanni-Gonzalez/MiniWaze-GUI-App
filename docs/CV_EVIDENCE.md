# CV_EVIDENCE — MiniWaze-GUI-App

Mostly **reinforces** Python and graph skills (Dijkstra also evidenced in C++ in VisualizadorDeGrafos). Suite verified by execution (pytest, CI runs it too).

## Unique evidence

| Item | Evidence |
|---|---|
| Dijkstra with binary-heap priority queue in Python | `programa/models/pathfinder.py` (`heapq`) |
| CSV → graph data pipeline + canvas rendering | `models/map_loader.py`, `ui/map_canvas.py` |
| Logic/UI separation enabling GUI-free tests, run in CI | `tests/test_logic.py` + `ci.yml` with pytest |

## Optional resume bullet

- Built a route-finding desktop app (Python/Tkinter) that loads CSV map data into a graph and computes optimal routes with heap-based Dijkstra, with GUI-independent logic tested via pytest in CI.

## ATS keywords (incremental)

Python, Tkinter, Dijkstra, priority queue, heapq, pytest, CSV parsing, pathfinding.
