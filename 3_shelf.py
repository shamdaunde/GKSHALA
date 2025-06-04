import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class Simple3DModelingTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple 3D Modeling Tool")
        self.geometry("800x600")
        
        # Initialize 3D view state
        self.objects = []
        
        # Create UI components
        self.create_menu()
        self.create_main_panels()
        self.setup_3d_viewport()
        
    def create_menu(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Scene", command=self.new_scene)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        create_menu = tk.Menu(menubar, tearoff=0)
        create_menu.add_command(label="Cube", command=lambda: self.create_shape('cube'))
        create_menu.add_command(label="Sphere", command=lambda: self.create_shape('sphere'))
        menubar.add_cascade(label="Create", menu=create_menu)
        
        self.config(menu=menubar)
    
    def create_main_panels(self):
        """Create the main application panels"""
        self.main_panel = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for tools
        self.left_panel = ttk.Frame(self.main_panel, width=200)
        self.main_panel.add(self.left_panel)
        
        # Center panel for 3D viewport
        self.viewport_panel = ttk.Frame(self.main_panel)
        self.main_panel.add(self.viewport_panel, weight=1)
    
    def setup_3d_viewport(self):
        """Set up the 3D viewport using matplotlib"""
        self.viewport_figure = Figure(figsize=(5, 5), dpi=100)
        self.viewport_ax = self.viewport_figure.add_subplot(111, projection='3d')
        self.viewport_canvas = FigureCanvasTkAgg(self.viewport_figure, master=self.viewport_panel)
        self.viewport_canvas.draw()
        self.viewport_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_shape(self, shape_type):
        """Create a 3D shape in the viewport"""
        if shape_type == 'cube':
            self.create_cube()
        elif shape_type == 'sphere':
            self.create_sphere()
        self.redraw_viewport()
    
    def create_cube(self):
        """Create a cube in the 3D viewport"""
        r = 1  # Cube size
        vertices = np.array([[r, r, r], [-r, r, r], [-r, -r, r], [r, -r, r],
                             [r, r, -r], [-r, r, -r], [-r, -r, -r], [r, -r, -r]])
        faces = [[vertices[j] for j in [0, 1, 2, 3]],
                 [vertices[j] for j in [4, 5, 6, 7]],
                 [vertices[j] for j in [0, 1, 5, 4]],
                 [vertices[j] for j in [2, 3, 7, 6]],
                 [vertices[j] for j in [1, 2, 6, 5]],
                 [vertices[j] for j in [0, 3, 7, 4]]]
        
        for face in faces:
            self.viewport_ax.add_collection3d(plt.Polygon(face, color='cyan', alpha=0.5))
    
    def create_sphere(self):
        """Create a sphere in the 3D viewport"""
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        self.viewport_ax.plot_surface(x, y, z, color='magenta', alpha=0.5)
    
    def redraw_viewport(self):
        """Redraw all objects in the viewport"""
        self.viewport_ax.cla()  # Clear the axes
        self.setup_3d_viewport()  # Reset the viewport
        for obj in self.objects:
            if obj['type'] == 'cube':
                self.create_cube()
            elif obj['type'] == 'sphere':
                self.create_sphere()
        self.viewport_canvas.draw()
    
    def new_scene(self):
        """Create a new empty scene"""
        self.objects = []
        self.redraw_viewport()

if __name__ == "__main__":
    app = Simple3DModelingTool()
    app.mainloop()
