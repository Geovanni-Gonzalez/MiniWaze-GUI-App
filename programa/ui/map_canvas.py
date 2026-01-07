import tkinter as tk

class MapCanvas(tk.Canvas):
    def __init__(self, parent, graph, matrix, cell_size=40, on_click_callback=None):
        super().__init__(parent, bg="#1E1E1E", highlightthickness=0)
        self.graph = graph
        self.matrix = matrix
        self.cell_size = cell_size
        self.on_click_callback = on_click_callback
        
        self.width = len(matrix[0]) * cell_size if matrix else 600
        self.height = len(matrix) * cell_size if matrix else 400
        self.config(width=self.width, height=self.height)

        self.start_node = None
        self.end_node = None
        
        self.bind("<Button-1>", self._on_click)
        self.draw_map()

    def set_map(self, graph, matrix):
        self.graph = graph
        self.matrix = matrix
        self.width = len(matrix[0]) * self.cell_size if matrix else 600
        self.height = len(matrix) * self.cell_size if matrix else 400
        self.config(width=self.width, height=self.height)
        self.draw_map()

    def draw_map(self):
        self.delete("all")
        if not self.matrix: return

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # Colors
        COLOR_BLOCK = "#333333" # 0
        COLOR_CALLE = "#FFFFFF" # L, R
        COLOR_AVENIDA = "#FFEB3B" # N, S (Yellow)
        COLOR_CRUCE = "#F44336" # C (Red)
        COLOR_SF = "#4CAF50" # SF (Green)
        
        for y in range(rows):
            for x in range(cols):
                val = self.matrix[y][x]
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = COLOR_BLOCK
                text = ""

                if val == '0': color = COLOR_BLOCK
                elif val in ['L', 'R']: 
                    color = COLOR_CALLE 
                    text = val
                elif val in ['N', 'S']: 
                    color = COLOR_AVENIDA
                    text = val
                elif val == 'C': 
                    color = COLOR_CRUCE
                    text = "C"
                elif val == 'SF': 
                    color = COLOR_SF
                    text = "SF"
                
                # Draw Cell
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline="#222")

                # Draw Text (Direction)
                if text:
                    textcolor = "black" if color in [COLOR_AVENIDA, COLOR_CALLE, COLOR_SF] else "white"
                    self.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=text, fill=textcolor)

    def highlight_path(self, path_nodes):
        # path_nodes: List of Node objects
        if not path_nodes: return
        
        points = []
        for node in path_nodes:
            center_x = node.x * self.cell_size + self.cell_size/2
            center_y = node.y * self.cell_size + self.cell_size/2
            points.append(center_x)
            points.append(center_y)
        
        if len(points) >= 4:
            self.create_line(points, fill="#00E5FF", width=4, capstyle=tk.ROUND, joinstyle=tk.ROUND, tags="path")

    def _on_click(self, event):
        x = int(event.x // self.cell_size)
        y = int(event.y // self.cell_size)
        
        # Validate connection
        if not self.graph: return
        node = self.graph.get_node(x, y)
        
        if node and node.value != '0':
            if self.on_click_callback:
                self.on_click_callback(x, y)
            
            # Simple visual marker
            # self.create_oval(...) - Handled by Main Window refreshing map or markers
