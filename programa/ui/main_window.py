import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from ui.map_canvas import MapCanvas
from models.map_loader import MapLoader
from models.pathfinder import Pathfinder
import os

class MainWindow:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title(f"MiniWaze - Usuario: {current_user}")
        self.root.geometry("1000x700")

        self.graph = None
        self.map_loader = None
        self.start_point = None
        self.end_point = None
        self.destinations = {} # Name -> NodeID
        self.current_hour = 12 # Default normal
        
        # UI Components
        self._build_ui()

    def _build_ui(self):
        # Toolbar / Sidebar
        toolbar = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10, width=250)
        toolbar.pack(side="left", fill="y")
        
        # Map Area
        self.canvas_frame = tk.Frame(self.root, bg="#333", relief=tk.SUNKEN, borderwidth=2)
        self.canvas_frame.pack(side="right", expand=True, fill="both")
        
        # --- Sidebar Controls ---
        
        # Group 1: Mapa
        frame_map = tk.LabelFrame(toolbar, text="Mapa", bg="#f0f0f0", font=("Arial", 10, "bold"), padx=5, pady=5)
        frame_map.pack(fill="x", pady=5)
        tk.Button(frame_map, text="📂 Cargar Mapa (CSV)", command=self._load_map_dialog, bg="#e0e0e0").pack(fill="x")
        self.btn_theme = tk.Button(frame_map, text="🌗 Tema Oscuro/Claro", command=self._toggle_theme, bg="#e0e0e0")
        self.btn_theme.pack(fill="x", pady=2)
        
        # Group 2: Navegación
        frame_nav = tk.LabelFrame(toolbar, text="Navegación", bg="#f0f0f0", font=("Arial", 10, "bold"), padx=5, pady=5)
        frame_nav.pack(fill="x", pady=5)
        
        self.lbl_start = tk.Label(frame_nav, text="Inicio: --", bg="#f0f0f0", fg="blue", font=("Consolas", 9))
        self.lbl_start.pack(anchor="w")
        self.lbl_end = tk.Label(frame_nav, text="Fin:    --", bg="#f0f0f0", fg="red", font=("Consolas", 9))
        self.lbl_end.pack(anchor="w")
        
        tk.Button(frame_nav, text="🧹 Limpiar Puntos", command=self._clear_points).pack(fill="x", pady=5)
        
        tk.Label(frame_nav, text="Hora (0-23):", bg="#f0f0f0").pack(anchor="w")
        self.spin_hour = tk.Spinbox(frame_nav, from_=0, to=23, width=5, command=self._on_hour_change)
        self.spin_hour.delete(0, "end")
        self.spin_hour.insert(0, 12)
        self.spin_hour.pack(fill="x")

        tk.Button(frame_nav, text="🚀 Calcular Ruta", command=self._calculate_route, bg="#4CAF50", fg="white", font=("Arial", 9, "bold")).pack(fill="x", pady=10)
        
        # Group 3: Destinos
        frame_dest = tk.LabelFrame(toolbar, text="Destinos", bg="#f0f0f0", font=("Arial", 10, "bold"), padx=5, pady=5)
        frame_dest.pack(fill="x", pady=5)
        
        self.listbox_dest = tk.Listbox(frame_dest, height=4)
        self.listbox_dest.pack(fill="x")
        
        btn_frame_dest = tk.Frame(frame_dest, bg="#f0f0f0")
        btn_frame_dest.pack(fill="x", pady=2)
        tk.Button(btn_frame_dest, text="💾 Guardar", command=self._save_destination, width=8).pack(side="left")
        tk.Button(btn_frame_dest, text="🗑️ Borrar", command=self._delete_destination, width=8).pack(side="right")
        tk.Button(frame_dest, text="📍 Ir a Destino", command=self._load_destination_to_end).pack(fill="x", pady=2)

        # Exit Button
        tk.Button(toolbar, text="❌ Salir", command=self.root.quit, bg="#FFCDD2", fg="red").pack(fill="x", pady=20, side="bottom")

        # Legend
        frame_legend = tk.LabelFrame(toolbar, text="Leyenda", bg="#f0f0f0", font=("Arial", 9), padx=5, pady=5)
        frame_legend.pack(fill="x", pady=5, side="bottom")
        tk.Label(frame_legend, text="⬜ Calle (2)", bg="#f0f0f0").pack(anchor="w")
        tk.Label(frame_legend, text="🟨 Avenida (1/4)", bg="#f0f0f0", fg="#D4AC0D").pack(anchor="w")
        tk.Label(frame_legend, text="🟥 Cruce (2/3)", bg="#f0f0f0", fg="red").pack(anchor="w")

        
        # Placeholder Canvas
        self.map_canvas = MapCanvas(self.canvas_frame, None, [], on_click_callback=self._on_map_click)
        self.map_canvas.pack(expand=True, fill="both", padx=10, pady=10)

    def _load_map_dialog(self):
        filepath = filedialog.askopenfilename(
            initialdir=".", 
            title="Seleccionar Mapa CSV",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if filepath:
            self._load_map(filepath)

    def _load_map(self, filepath):
        """
        Loads the map from the CSV file and initializes the graph.
        Inputs: filepath (str)
        Outputs: None (Updates internal state)
        Restrictions: File must be a valid CSV.
        """
        self.map_loader = MapLoader(filepath)
        self._refresh_graph()
        self.map_canvas.set_map(self.graph, self.map_loader.raw_matrix)
        messagebox.showinfo("Mapa Cargado", "El mapa ha sido cargado exitosamente.")

    def _refresh_graph(self):
        """
        Rebuilds the graph with weights based on the current hour.
        Inputs: None (Reads from spin_hour)
        Outputs: None
        """
        # Reload graph based on current hour
        if not self.map_loader: return
        
        h = int(self.spin_hour.get())
        is_peak = (6 <= h <= 9) or (12 <= h <= 13) or (17 <= h <= 20)
        
        # Rebuild graph
        self.graph = self.map_loader.load_graph(is_peak_hour=is_peak)
        if self.map_canvas:
            self.map_canvas.graph = self.graph

    def _on_hour_change(self):
        # When hour changes, we might need to update graph weights?
        # Only strict requirement is calculation time, but let's update graph to be safe
        self._refresh_graph()

    def _on_map_click(self, x, y):
        """
        Handler for map clicks. Sets start or end points.
        Inputs: x, y (grid coordinates)
        Outputs: None
        Restrictions: Cannot select blocked cells.
        """
        # Select interactively
        if not self.start_point:
            self.start_point = (x, y)
            self.lbl_start.config(text=f"Inicio: ({x},{y})")
            # Visual feedback
            self.map_canvas.create_oval(
                x*40+10, y*40+10, x*40+30, y*40+30, 
                fill="blue", outline="white", width=2, tags="marker_start"
            )
        elif not self.end_point:
            self.end_point = (x, y)
            self.lbl_end.config(text=f"Fin: ({x},{y})")
            self.map_canvas.create_oval(
                x*40+10, y*40+10, x*40+30, y*40+30, 
                fill="red", outline="white", width=2, tags="marker_end"
            )
        else:
            # Maybe reset if clicked again? or ignore
            pass

    def _clear_points(self):
        self.start_point = None
        self.end_point = None
        self.lbl_start.config(text="Inicio: N/A")
        self.lbl_end.config(text="Fin: N/A")
        self.map_canvas.delete("marker_start")
        self.map_canvas.delete("marker_end")
        self.map_canvas.delete("path")

    def _calculate_route(self):
        """
        Calculates and visualizes the shortest path.
        Inputs: None (Uses internal start/end points)
        Outputs: None (Visualizes on canvas)
        Restrictions: Start and End must be set.
        """
        if not self.graph: 
            messagebox.showerror("Error", "No hay mapa cargado")
            return
        if not self.start_point or not self.end_point:
            messagebox.showerror("Error", "Seleccione Inicio y Fin")
            return

        self._refresh_graph() # Ensure weights are correct for current hour

        start_id = f"{self.start_point[0]},{self.start_point[1]}"
        end_id = f"{self.end_point[0]},{self.end_point[1]}"

        path, cost = Pathfinder.find_path(self.graph, start_id, end_id)

        self.map_canvas.delete("path")
        if path:
            self.map_canvas.highlight_path(path)
            messagebox.showinfo("Ruta Calculada", f"Costo estimado: {cost}\nNodos: {len(path)}\n\n(Cierre esta ventana para ver la animación)")
            self.map_canvas.animate_vehicle(path)
        else:
            messagebox.showwarning("Ruta", "No se encontró un camino válido.")

    def _save_destination(self):
        if not self.end_point:
            messagebox.showwarning("Destinos", "Seleccione un punto de fin primero.")
            return
            
        name = simpledialog.askstring("Guardar Destino", "Nombre del destino:")
        if name:
            self.destinations[name] = self.end_point
            self.listbox_dest.insert("end", name)

    def _delete_destination(self):
        sel = self.listbox_dest.curselection()
        if not sel: return
        name = self.listbox_dest.get(sel[0])
        del self.destinations[name]
        self.listbox_dest.delete(sel[0])

    def _load_destination_to_end(self):
        sel = self.listbox_dest.curselection()
        if not sel: return
        name = self.listbox_dest.get(sel[0])
        self.end_point = self.destinations[name]
        
        x, y = self.end_point
        self.lbl_end.config(text=f"Fin: ({x},{y})")
        self.map_canvas.delete("marker_end")
        self.map_canvas.create_oval(
            x*40+10, y*40+10, x*40+30, y*40+30, 
            fill="red", outline="white", width=2, tags="marker_end"
        )
        
    def _plan_trip(self):
        # Simple simulation: Ask for dept time, set spinbox, calculate
        h = simpledialog.askinteger("Planificar", "Hora de salida (0-23):", minvalue=0, maxvalue=23)
        if h is not None:
            self.spin_hour.delete(0, "end")
            self.spin_hour.insert(0, h)
            self._calculate_route()

    def _modify_map_mode(self):
        messagebox.showinfo("Modificar Mapa", "Funcionalidad Extra: Haga click derecho en el mapa para agregar un POI (Punto de Interés). (No implementado visualmente en este demo rápido)")

    def _toggle_theme(self):
        current = self.map_canvas.theme
        new_theme = "light" if current == "dark" else "dark"
        self.map_canvas.set_theme(new_theme)
        
        # Note: Sidebar colors are hardcoded to #f0f0f0, updating them dynamically would require tracking all widgets.
        # For this prototype, we just update the map which is the main visual element.

