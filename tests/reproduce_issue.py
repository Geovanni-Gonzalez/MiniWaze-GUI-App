import sys
import os

# Add program to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'programa'))

from models.map_loader import MapLoader
from models.pathfinder import Pathfinder

def test_directionality():
    print("Testing Path Directionality...")
    
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'programa')
    map_path = os.path.join(base_dir, 'data', 'mapa.csv')
    
    loader = MapLoader(map_path)
    graph = loader.load_graph(is_peak_hour=False)
    
    # User Scenario: (1,1) to (8,1)
    # (1,1) is L (Left Only). (8,1) is to the Right.
    # Expected: FAIL
    
    print("\n--- Test 1: (1,1) -> (8,1) [Expecting Fail] ---")
    path1, _ = Pathfinder.find_path(graph, "1,1", "8,1")
    if path1:
        print("UNEXPECTED: Path found against traffic!")
    else:
        print("SUCCESS: correctly blocked movement against traffic.")

    # Inverse Scenario: (8,1) to (1,1)
    # Traffic flows Left. So 8 (Right) -> 1 (Left) should work?
    # 8,1 is C (Cruce). 7,1 is L.
    # 8->7 (Left) allowed?
    # C allows moving L if neighbor is L. Yes.
    
    print("\n--- Test 2: (8,1) -> (1,1) [Expecting Pass] ---")
    path2, cost2 = Pathfinder.find_path(graph, "8,1", "1,1")
    if path2:
        print(f"SUCCESS: Path found! Cost: {cost2}")
        print("Route:", [n.id for n in path2])
    else:
        print("FAIL: Valid path not found.")
        
    # Test 3: Path with turns
    # (1,4) is R (Row 4). Ends at (8,4) C.
    # Can we go (1,4) -> (8,4)?
    print("\n--- Test 3: (1,4) -> (8,4) [Row 4 is Right/East] ---")
    path3, cost3 = Pathfinder.find_path(graph, "1,4", "8,4")
    if path3:
        print(f"SUCCESS: Path found! Cost: {cost3}")
    else:
        print("FAIL: Path (1,4)->(8,4) not found.")

if __name__ == "__main__":
    test_directionality()
