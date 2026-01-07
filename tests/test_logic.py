import sys
import os

# Add program to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'programa'))

from models.map_loader import MapLoader
from models.pathfinder import Pathfinder

def test_backend():
    print("Testing Backend Logic...")
    
    # 1. Load Map
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'programa')
    map_path = os.path.join(base_dir, 'data', 'mapa.csv')
    
    # Debug Raw File
    with open(map_path, 'rb') as f:
        print(f"Raw first 50 bytes: {f.read(50)}")
        
    loader = MapLoader(map_path)
    graph = loader.load_graph(is_peak_hour=False)
    
    if not graph:
        print("FAIL: Graph not loaded")
        return

    # Check Node at (1,4)
    target_node = graph.get_node(1, 4)
    if target_node:
        print(f"Node(1,4) Value: '{target_node.value}' (Len: {len(target_node.value)})")
        print(f"Node(1,4) Edges: {len(target_node.edges)}")
        for e in target_node.edges:
             print(f" -> {e[0].id}")
    else:
        print("Node(1,4) is None")

    start_node = graph.get_node(1, 4)
    end_node = graph.get_node(3, 4)

    if not start_node or not end_node:
        print("FAIL: Start or End node missing")
        return

    path, cost = Pathfinder.find_path(graph, start_node.id, end_node.id)
    
    if path:
        print(f"Path found: {len(path)} nodes. Cost: {cost}")
        print("Route:", [str(n) for n in path])
        print("PASS: Pathfinding logic works.")
    else:
        print("FAIL: No path found.")

if __name__ == "__main__":
    test_backend()
