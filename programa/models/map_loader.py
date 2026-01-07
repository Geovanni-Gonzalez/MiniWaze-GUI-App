import csv
from models.graph import Graph

class MapLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.raw_matrix = []

    def load_graph(self, is_peak_hour=False):
        """
        Parses the CSV and builds a weighted graph.
        Weights depend on is_peak_hour.
        """
        graph = Graph()
        self.raw_matrix = []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                for y, row in enumerate(reader):
                    self.raw_matrix.append(row)
                    for x, cell_value in enumerate(row):
                        graph.add_node(x, y, cell_value.strip())
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return None

        # Build edges based on direction and weights
        rows = len(self.raw_matrix)
        cols = len(self.raw_matrix[0]) if rows > 0 else 0

        # Define Costs
        # is_peak_hour: 
        #   Calles (L/R) = 2
        #   Avenidas (N/S) = 4
        #   Cruces (C) = 3
        # Normal Cost:
        #   Calles (L/R) = 2
        #   Avenidas (N/S) = 1
        #   Cruces (C) = 2
        
        cost_calle = 2      # Always 2
        cost_avenida = 4 if is_peak_hour else 1
        cost_cruce = 3 if is_peak_hour else 2
        
        # Valid moves from current cell type
        # N: North -> (x, y-1)
        # S: South -> (x, y+1)
        # L: Left -> (x-1, y)
        # R: Right -> (x+1, y)
        # C: Intersection -> Can go N, S, L, R (depending on neighbors)
        # ND: No Dir -> All neighbors (not in spec but good for fallback)

        for y in range(rows):
            for x in range(cols):
                current_node = graph.get_node(x, y)
                val = current_node.value

                if val == '0': continue # Block/Cuadra
                if val in ['SF', 'ND']: pass # Handle endpoints or generic

                # Check Neighbors
                neighbors = [
                    (x, y-1, 'N'), # Up
                    (x, y+1, 'S'), # Down
                    (x-1, y, 'L'), # Left
                    (x+1, y, 'R')  # Right
                ]

                for nx, ny, direction in neighbors:
                    if 0 <= nx < cols and 0 <= ny < rows:
                        neighbor_node = graph.get_node(nx, ny)
                        n_val = neighbor_node.value
                        
                        if n_val == '0': continue

                        # Logic to determine if connection exists
                        can_move = False
                        
                        # Apply rules based on 'val' (Current Source)
                        # If current is Arrow, must follow arrow
                        if val == 'N' and direction == 'N': can_move = True
                        elif val == 'S' and direction == 'S': can_move = True
                        elif val == 'L' and direction == 'L': can_move = True
                        elif val == 'R' and direction == 'R': can_move = True
                        
                        # If current is Cruce, can go anywhere valid
                        # But wait, Cruce allows exit to any connected path?
                        # Usually yes, but destination must accept it.
                        elif val == 'C':
                            # Can go N if neighbor is N or C
                            if direction == 'N' and n_val in ['N', 'C', 'SF']: can_move = True
                            if direction == 'S' and n_val in ['S', 'C', 'SF']: can_move = True
                            if direction == 'L' and n_val in ['L', 'C', 'SF']: can_move = True
                            if direction == 'R' and n_val in ['R', 'C', 'SF']: can_move = True

                        # Handle SF (Start/Finish or Endpoint) as permissive?
                        # Spec says SF is just a location. Assume it behaves like C or 0? 
                        # Figure 2 shows SF at ends of streets.
                        
                        if can_move:
                            # Calculate weight based on TARGET type
                            weight = 1 # Default
                            if n_val in ['L', 'R']: weight = cost_calle
                            elif n_val in ['N', 'S']: weight = cost_avenida
                            elif n_val == 'C': weight = cost_cruce
                            
                            current_node.add_edge(neighbor_node, weight)

        return graph
