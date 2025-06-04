import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu

class GKSHALA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - 3D Animation Suite")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Remove window decorations (title bar)
        self.overrideredirect(True)
        
        # Variables
        self.current_file = None
        self.is_maximized = False
        
        # Custom title bar
        self.create_title_bar()
        
        # Main menu bar
        self.create_main_menu()
        
        # Ribbon menu
        self.create_ribbon_menu()
        
        # Status line/toolbar
        self.create_status_line()
        
        # Main workspace
        self.create_workspace()
        
        # Channel box
        self.create_channel_box()
        
        # Attribute editor
        self.create_attribute_editor()
        
        # Time slider
        self.create_time_slider()
        
        # Status bar
        self.create_status_bar()
        
        # Bindings for window dragging
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)
        
    def create_title_bar(self):
        """Create custom title bar with window controls"""
        self.title_bar = tk.Frame(self, bg='#2d2d2d', height=32)
        self.title_bar.pack(fill=tk.X)
        
        # Title label
        self.title_label = tk.Label(
            self.title_bar, 
            text="GKSHALA", 
            bg='#2d2d2d', 
            fg='white',
            font=('Arial', 10, 'bold')
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Window controls
        controls_frame = tk.Frame(self.title_bar, bg='#2d2d2d')
        controls_frame.pack(side=tk.RIGHT, padx=5)
        
        # Minimize button
        self.minimize_btn = tk.Button(
            controls_frame, 
            text="—", 
            command=self.show_minimized,
            borderwidth=0,
            bg='#2d2d2d',
            fg='white',
            activebackground='#4d4d4d',
            font=('Arial', 12)
        )
        self.minimize_btn.pack(side=tk.LEFT, padx=2)
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(
            controls_frame, 
            text="□", 
            command=self.toggle_maximize,
            borderwidth=0,
            bg='#2d2d2d',
            fg='white',
            activebackground='#4d4d4d',
            font=('Arial', 10)
        )
        self.maximize_btn.pack(side=tk.LEFT, padx=2)
        
        # Close button
        self.close_btn = tk.Button(
            controls_frame, 
            text="×", 
            command=self.quit,
            borderwidth=0,
            bg='#2d2d2d',
            fg='white',
            activebackground='#ff4444',
            font=('Arial', 12)
        )
        self.close_btn.pack(side=tk.LEFT, padx=2)
        
    def create_main_menu(self):
        """Create the main menu bar"""
        menubar = Menu(self)
        
        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Scene", command=lambda: self.new_scene())
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit Menu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Workspace Menu
        workspace_menu = Menu(menubar, tearoff=0)
        workspace_menu.add_command(label="Modeling")
        workspace_menu.add_command(label="Animation")
        workspace_menu.add_command(label="Rendering")
        menubar.add_cascade(label="Workspace", menu=workspace_menu)
        
        # Polygons Menu
        polygons_menu = Menu(menubar, tearoff=0)
        polygons_menu.add_command(label="Create Cube")
        polygons_menu.add_command(label="Create Sphere")
        polygons_menu.add_command(label="Create Cylinder")
        menubar.add_cascade(label="Polygons", menu=polygons_menu)
        
        self.config(menu=menubar)
    
    def create_ribbon_menu(self):
        """Create ribbon-style menu with tabs"""
        self.ribbon_menu = ttk.Notebook(self)
        self.ribbon_menu.pack(fill=tk.X)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TNotebook', background='#2d2d2d')
        style.configure('TNotebook.Tab', background='#2d2d2d', foreground='white')
        style.map('TNotebook.Tab', 
                 background=[('selected', '#4d4d4d')])
        
        # File Tab
        file_tab = tk.Frame(self.ribbon_menu, bg='#2d2d2d')
        self.create_file_tab(file_tab)
        self.ribbon_menu.add(file_tab, text="File")
        
        # Insert Tab
        insert_tab = tk.Frame(self.ribbon_menu, bg='#2d2d2d')
        self.create_insert_tab(insert_tab)
        self.ribbon_menu.add(insert_tab, text="Insert")
        
        # Animation Tab
        animation_tab = tk.Frame(self.ribbon_menu, bg='#2d2d2d')
        self.create_animation_tab(animation_tab)
        self.ribbon_menu.add(animation_tab, text="Animation")
        
        # View Tab
        view_tab = tk.Frame(self.ribbon_menu, bg='#2d2d2d')
        self.create_view_tab(view_tab)
        self.ribbon_menu.add(view_tab, text="View")
        
        # Help Tab
        help_tab = tk.Frame(self.ribbon_menu, bg='#2d2d2d')
        self.create_help_tab(help_tab)
        self.ribbon_menu.add(help_tab, text="Help")
    
    def create_file_tab(self, parent):
        """Create content for File tab"""
        file_group = tk.LabelFrame(
            parent, 
            text="File", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        file_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Save button
        save_btn = tk.Button(
            file_group, 
            text="Save", 
            command=self.save_file,
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            activeforeground='white',
            bd=0
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save As button
        save_as_btn = tk.Button(
            file_group, 
            text="Save As", 
            command=self.save_file_as,
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            activeforeground='white',
            bd=0
        )
        save_as_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Recent button with dropdown
        recent_btn = tk.Menubutton(
            file_group, 
            text="Recent", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            activeforeground='white',
            bd=0,
            relief=tk.RAISED
        )
        recent_btn.menu = tk.Menu(recent_btn, tearoff=0)
        recent_btn["menu"] = recent_btn.menu
        recent_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add some dummy recent items
        for i in range(1, 6):
            recent_btn.menu.add_command(label=f"Recent Project {i}")
    
    def create_insert_tab(self, parent):
        """Create content for Insert tab"""
        code_group = tk.LabelFrame(
            parent, 
            text="Code", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        code_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Code insertion buttons
        code_buttons = [
            ("Code Block",),
            ("Function",),
            ("Class",),
            ("Loop",)
        ]
        
        for text in code_buttons:
            btn = tk.Button(
                code_group, 
                text=text[0], 
                bg='#3d3d3d',
                fg='white',
                activebackground='#4d4d4d',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_animation_tab(self, parent):
        """Create content for Animation tab"""
        # Entrance animations
        entrance_group = tk.LabelFrame(
            parent, 
            text="Entrance", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        entrance_group.pack(fill=tk.X, padx=5, pady=5)
        
        for anim in ["Fade", "Fly In", "Bounce"]:
            btn = tk.Button(
                entrance_group, 
                text=anim, 
                bg='#3d3d3d',
                fg='white',
                activebackground='#4d4d4d',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Exit animations
        exit_group = tk.LabelFrame(
            parent, 
            text="Exit", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        exit_group.pack(fill=tk.X, padx=5, pady=5)
        
        for anim in ["Fade Out", "Fly Out", "Shrink"]:
            btn = tk.Button(
                exit_group, 
                text=anim, 
                bg='#3d3d3d',
                fg='white',
                activebackground='#4d4d4d',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_view_tab(self, parent):
        """Create content for View tab"""
        # Presentation views
        pres_group = tk.LabelFrame(
            parent, 
            text="Presentation Views", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        pres_group.pack(fill=tk.X, padx=5, pady=5)
        
        view_buttons = ["Normal", "Slide Sorter", "Reading"]
        
        for view in view_buttons:
            btn = tk.Button(
                pres_group, 
                text=view, 
                bg='#3d3d3d',
                fg='white',
                activebackground='#4d4d4d',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Show/hide options
        show_group = tk.LabelFrame(
            parent, 
            text="Show", 
            bg='#2d2d2d', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        show_group.pack(fill=tk.X, padx=5, pady=5)
        
        show_options = ["Ruler", "Gridlines", "Guides", "Navigation Pane"]
        
        for option in show_options:
            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(
                show_group, 
                text=option, 
                variable=var,
                bg='#2d2d2d',
                fg='white',
                activebackground='#2d2d2d',
                activeforeground='white',
                selectcolor='#2d2d2d'
            )
            cb.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_help_tab(self, parent):
        """Create content for Help tab"""
        help_buttons = ["Help", "About", "Check for Updates"]
        
        for text in help_buttons:
            btn = tk.Button(
                parent, 
                text=text, 
                bg='#3d3d3d',
                fg='white',
                activebackground='#4d4d4d',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_status_line(self):
        """Create status line/toolbar"""
        self.status_line = tk.Frame(self, bd=1, relief=tk.RAISED, padx=5, pady=2, bg='#3d3d3d')
        self.status_line.pack(fill=tk.X)
        
        # Buttons
        new_file_btn = tk.Button(
            self.status_line, 
            text="New File", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        new_file_btn.pack(side=tk.LEFT, padx=2)
        
        open_btn = tk.Button(
            self.status_line, 
            text="Open", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        open_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        separator = tk.Label(self.status_line, text="|", fg="gray", bg='#3d3d3d')
        separator.pack(side=tk.LEFT, padx=5)
        
        grid_snap_btn = tk.Button(
            self.status_line, 
            text="Grid Snap", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        grid_snap_btn.pack(side=tk.LEFT, padx=2)
        
        vertex_snap_btn = tk.Button(
            self.status_line, 
            text="Vertex Snap", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        vertex_snap_btn.pack(side=tk.LEFT, padx=2)
    
    def create_workspace(self):
        """Create the main workspace with viewports"""
        self.workspace = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.workspace.pack(fill=tk.BOTH, expand=True)
        
        # Left toolbox
        self.toolbox = tk.Frame(self.workspace, width=200, bg='#2d2d2d', bd=1, relief=tk.SUNKEN)
        self.create_toolbox()
        self.workspace.add(self.toolbox)
        
        # Main viewport area
        self.viewport_area = tk.PanedWindow(self.workspace, orient=tk.VERTICAL)
        self.workspace.add(self.viewport_area)
        
        # Viewport tabs
        self.viewport_tabs = ttk.Notebook(self.viewport_area)
        self.viewport_area.add(self.viewport_tabs)
        
        # Create viewports
        self.create_viewports()
        
        # Right channel box area
        self.channel_area = tk.Frame(self.workspace, width=300, bg='#2d2d2d')
        self.workspace.add(self.channel_area)
    
    def create_toolbox(self):
        """Create the toolbox on the left side"""
        # Transform Tools
        move_btn = tk.Button(
            self.toolbox, 
            text="Move Tool", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        move_btn.pack(fill=tk.X, pady=2)
        
        rotate_btn = tk.Button(
            self.toolbox, 
            text="Rotate Tool", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        rotate_btn.pack(fill=tk.X, pady=2)
        
        scale_btn = tk.Button(
            self.toolbox, 
            text="Scale Tool", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        scale_btn.pack(fill=tk.X, pady=2)
        
        # Separator
        separator = tk.Frame(self.toolbox, height=2, bg='#4d4d4d')
        separator.pack(fill=tk.X, pady=5)
        
        # Viewport Layouts
        single_pane_btn = tk.Button(
            self.toolbox, 
            text="Single Pane", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        single_pane_btn.pack(fill=tk.X, pady=2)
        
        four_view_btn = tk.Button(
            self.toolbox, 
            text="Four View", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        four_view_btn.pack(fill=tk.X, pady=2)
    
    def create_viewports(self):
        """Create viewports with gridlines"""
        # Perspective view
        perspective = tk.Frame(self.viewport_tabs)
        self.perspective_canvas = tk.Canvas(perspective, bg='#1d1d1d')
        self.perspective_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(self.perspective_canvas)
        self.viewport_tabs.add(perspective, text="Perspective")
        
        # Front view
        front = tk.Frame(self.viewport_tabs)
        front_canvas = tk.Canvas(front, bg='#1d1d1d')
        front_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(front_canvas)
        self.viewport_tabs.add(front, text="Front")
        
        # Side view
        side = tk.Frame(self.viewport_tabs)
        side_canvas = tk.Canvas(side, bg='#1d1d1d')
        side_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(side_canvas)
        self.viewport_tabs.add(side, text="Side")
        
        # Top view
        top = tk.Frame(self.viewport_tabs)
        top_canvas = tk.Canvas(top, bg='#1d1d1d')
        top_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(top_canvas)
        self.viewport_tabs.add(top, text="Top")
    
    def draw_grid(self, canvas):
        """Draw gridlines on the viewport canvas"""
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Clear existing grid
        canvas.delete("grid_line")
        
        # Draw vertical lines
        for i in range(0, width, 20):
            canvas.create_line(i, 0, i, height, fill='#333333', tags="grid_line")
        
        # Draw horizontal lines
        for i in range(0, height, 20):
            canvas.create_line(0, i, width, i, fill='#333333', tags="grid_line")
        
        # Draw center lines
        canvas.create_line(width//2, 0, width//2, height, fill='#555555', width=1, tags="grid_line")
        canvas.create_line(0, height//2, width, height//2, fill='#555555', width=1, tags="grid_line")
        
        # Bind resize event to redraw grid
        canvas.bind("<Configure>", lambda e: self.draw_grid(canvas))
    
    def create_channel_box(self):
        """Create the channel box on the right side"""
        self.channel_box = tk.Frame(self.channel_area, bd=2, relief=tk.GROOVE, bg='#2d2d2d')
        self.channel_box.pack(fill=tk.BOTH, expand=True)
        
        # Title Label
        title = tk.Label(
            self.channel_box, 
            text="Channel Box", 
            bg='#3d3d3d', 
            fg='white',
            font=("Arial", 10, "bold")
        )
        title.pack(fill=tk.X)
        
        # Listbox for attributes
        self.attribute_list = tk.Listbox(
            self.channel_box, 
            bg='#2d2d2d', 
            fg='white',
            selectbackground='#4d4d4d',
            selectforeground='white',
            bd=0
        )
        self.attribute_list.pack(fill=tk.BOTH, expand=True)
        
        # Add sample attributes
        attributes = ["Translate X", "Translate Y", "Translate Z",
                     "Rotate X", "Rotate Y", "Rotate Z",
                     "Scale X", "Scale Y", "Scale Z",
                     "Visibility"]
        
        for attr in attributes:
            self.attribute_list.insert(tk.END, attr)
    
    def create_attribute_editor(self):
        """Create the attribute editor below the viewports"""
        self.attribute_editor = ttk.Notebook(self.viewport_area)
        self.viewport_area.add(self.attribute_editor)
        
        # Node Attributes Tab
        node_tab = tk.Text(
            self.attribute_editor, 
            bg='#2d2d2d', 
            fg='white',
            insertbackground='white'
        )
        node_tab.insert("1.0", "Transform Node Attributes...")
        node_tab.pack(expand=True, fill="both")
        self.attribute_editor.add(node_tab, text="pCube1")
        
        # Material Tab
        material_tab = tk.Text(
            self.attribute_editor, 
            bg='#2d2d2d', 
            fg='white',
            insertbackground='white'
        )
        material_tab.insert("1.0", "Lambert1 Shader Attributes...")
        material_tab.pack(expand=True, fill="both")
        self.attribute_editor.add(material_tab, text="lambert1")
    
    def create_time_slider(self):
        """Create the time slider at the bottom"""
        self.time_slider_frame = tk.Frame(self, bg='#2d2d2d')
        self.time_slider_frame.pack(fill=tk.X)
        
        # Playback controls
        controls_frame = tk.Frame(self.time_slider_frame, bg='#2d2d2d')
        controls_frame.pack(side=tk.LEFT, padx=5)
        
        rewind_btn = tk.Button(
            controls_frame, 
            text="⏮", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        rewind_btn.pack(side=tk.LEFT, padx=2)
        
        play_btn = tk.Button(
            controls_frame, 
            text="▶", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        play_btn.pack(side=tk.LEFT, padx=2)
        
        stop_btn = tk.Button(
            controls_frame, 
            text="⏹", 
            bg='#3d3d3d',
            fg='white',
            activebackground='#4d4d4d',
            bd=0
        )
        stop_btn.pack(side=tk.LEFT, padx=2)
        
        # Time slider
        self.time_slider = tk.Scale(
            self.time_slider_frame, 
            from_=1, 
            to=100, 
            orient=tk.HORIZONTAL,
            bg="#d83131",
            fg='white',
            troughcolor="#45b1db",
            highlightbackground="#9c7171",
            bd=0
        )
        self.time_slider.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Current frame indicator
        frame_label = tk.Label(
            self.time_slider_frame, 
            text="Frame: 1", 
            bg='#2d2d2d',
            fg='white'
        )
        frame_label.pack(side=tk.RIGHT, padx=5)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#d14444",
            fg='white'
        )
        self.status_bar.pack(fill=tk.X)
    
    def show_minimized(self):
        """Minimize the window"""
        self.iconify()
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            self.geometry(self.normal_geometry)
            self.maximize_btn.config(text="□")
            self.is_maximized = False
        else:
            self.normal_geometry = self.geometry()
            self.state('zoomed')
            self.maximize_btn.config(text="❐")
            self.is_maximized = True
    
    def new_scene(self):
        """Create a new scene"""
        self.current_file = None
        self.status_bar.config(text="New scene created")
        self.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def save_file(self):
        """Handle save file action"""
        if self.current_file:
            # In a real app, you would save the file here
            self.status_bar.config(text=f"Saved {self.current_file}")
            self.after(3000, lambda: self.status_bar.config(text="Ready"))
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Handle save as file action"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gks",
            filetypes=[("GKSHALA Files", "*.gks"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            # In a real app, you would save the file here
            self.status_bar.config(text=f"Saved as {file_path}")
            self.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def open_file(self):
        """Handle open file action"""
        file_path = filedialog.askopenfilename(
            filetypes=[("GKSHALA Files", "*.gks"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            # In a real app, you would open the file here
            self.status_bar.config(text=f"Opened {file_path}")
            self.after(3000, lambda: self.status_bar.config(text="Ready"))
    
    def start_move(self, event):
        """Start window move on title bar drag"""
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        """Handle window movement"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = GKSHALA()
    app.mainloop()