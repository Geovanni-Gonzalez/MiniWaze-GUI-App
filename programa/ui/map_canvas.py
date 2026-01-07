import tkinter as tk

class MapCanvas(tk.Canvas):
    def __init__(self, parent, graph, matrix, cell_size=40, on_click_callback=None):
        super().__init__(parent, bg="#1E1E1E", highlightthickness=0)
        self.graph = graph
        self.matrix = matrix
        self.cell_size = cell_size
        self.on_click_callback = on_click_callback
        self.theme = "dark" # dark or light
        
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

    def set_theme(self, mode):
        self.theme = mode
        bg = "#1E1E1E" if mode == "dark" else "#FFFFFF"
        self.config(bg=bg)
        self.draw_map()

    def draw_map(self):
        self.delete("all")
        if not self.matrix: return

        rows = len(self.matrix)
        cols = len(self.matrix[0])

        # Colors
        if self.theme == "dark":
            COLOR_BLOCK = "#333333"
            COLOR_CALLE = "#FFFFFF" # Directions on Dark
            COLOR_BG_CALLE = "#1E1E1E" # Actually transparent? No, grid.
            # Let's keep logic simple: 
            # 0 = Block
            # L/R/N/S = Streets/Aves
        else:
            COLOR_BLOCK = "#E0E0E0"
        
        # Unified Palette
        # Key: (DarkColor, LightColor)
        PALETTE = {
            'BLOCK': ("#333333", "#E0E0E0"),
            'CALLE': ("#FFFFFF", "#CCCCCC"),
            'AVENIDA': ("#FFEB3B", "#FBC02D"),
            'CRUCE': ("#F44336", "#D32F2F"),
            'SF': ("#4CAF50", "#388E3C"),
            'TEXT': ("#000000", "#000000"), # Arrows always black on colored cells?
            'TEXT_DARK_BG': ("#FFFFFF", "#000000") # Text on block?
        }
        
        p_idx = 0 if self.theme == "dark" else 1

        for y in range(rows):
            for x in range(cols):
                val = self.matrix[y][x]
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = PALETTE['BLOCK'][p_idx]
                text = ""

                if val == '0': color = PALETTE['BLOCK'][p_idx]
                elif val == 'L': 
                    color = PALETTE['CALLE'][p_idx] 
                    text = "←" 
                elif val == 'R': 
                    color = PALETTE['CALLE'][p_idx] 
                    text = "→" 
                elif val == 'N': 
                    color = PALETTE['AVENIDA'][p_idx]
                    text = "↑" 
                elif val == 'S': 
                    color = PALETTE['AVENIDA'][p_idx]
                    text = "↓" 
                elif val == 'C': 
                    color = PALETTE['CRUCE'][p_idx]
                    text = "C"
                elif val == 'SF': 
                    color = PALETTE['SF'][p_idx]
                    text = "🏁"
                elif val == 'ND':
                    color = PALETTE['CALLE'][p_idx]
                    text = "↔"
                
                # Draw Cell
                tag = f"cell_{x}_{y}"
                # Border color
                border = "#222" if self.theme == "dark" else "#999"
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline=border, tags=("cell", tag))

                # Draw Text (Direction)
                if text:
                    # Determine text color contrast
                    textcolor = "black" 
                    if self.theme == "dark" and color == PALETTE['BLOCK'][0]: textcolor = "white"
                    
                    font_size = 14 if text in ["C", "SF"] else 18
                    self.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=text, fill=textcolor, font=("Arial", font_size, "bold"), tags=("text", tag))

        # Bind hover
        self.bind("<Motion>", self._on_hover)

    def _on_hover(self, event):
        x = int(event.x // self.cell_size)
        y = int(event.y // self.cell_size)
        
        # Reset previous highlight (optional, or just redraw on move? Canvas is efficient enough)
        # Actually, simpler to just delete a specific 'highlight' tag
        self.delete("highlight")
        
        if 0 <= y < len(self.matrix) and 0 <= x < len(self.matrix[0]):
             x1 = x * self.cell_size
             y1 = y * self.cell_size
             x2 = x1 + self.cell_size
             y2 = y1 + self.cell_size
             self.create_rectangle(x1, y1, x2, y2, outline="#00FF00", width=3, tags="highlight")


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

    def animate_vehicle(self, path_nodes, callback=None):
        if not path_nodes or len(path_nodes) < 2: return
        
        # Draw vehicle
        start_node = path_nodes[0]
        sx = start_node.x * self.cell_size + self.cell_size/2
        sy = start_node.y * self.cell_size + self.cell_size/2
        
        vehicle = self.create_oval(sx-8, sy-8, sx+8, sy+8, fill="#FF00FF", outline="white", width=2, tags="vehicle")
        
        self._animate_step(vehicle, path_nodes, 1, callback)

    def _animate_step(self, vehicle, nodes, target_idx, callback):
        if target_idx >= len(nodes):
            self.delete(vehicle)
            if callback: callback()
            return
            
        target_node = nodes[target_idx]
        tx = target_node.x * self.cell_size + self.cell_size/2
        ty = target_node.y * self.cell_size + self.cell_size/2
        
        coords = self.coords(vehicle)
        cx = (coords[0] + coords[2]) / 2
        cy = (coords[1] + coords[3]) / 2
        
        dx = tx - cx
        dy = ty - cy
        dist = (dx**2 + dy**2)**0.5
        
        if dist < 5:
            # Reached node
            self._animate_step(vehicle, nodes, target_idx + 1, callback)
        else:
            # Move towards target
            step = 5 # Speed
            nx = dx / dist * step
            ny = dy / dist * step
            self.move(vehicle, nx, ny)
            self.after(20, lambda: self._animate_step(vehicle, nodes, target_idx, callback))

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
