import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu
from tkinter import font as tkfont

class GKSHALA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - 3D Animation Suite")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Custom color scheme
        self.bg_dark = "#1e1e1e"
        self.bg_darker = "#171717"
        self.bg_light = "#2d2d2d"
        self.accent_color = "#45aaf2"
        self.highlight_color = "#4d7cff"
        self.text_color = "#ffffff"
        self.highlight_text = "#f1c40f"
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_style()
        
        # Remove window decorations (title bar)
        self.overrideredirect(True)
        self.configure(bg=self.bg_dark)
        
        # Variables
        self.current_file = None
        self.is_maximized = False
        self.current_frame = 1
        self.playback_active = False
        
        # Custom title bar
        self.create_title_bar()
        
        # Main menu bar
        self.create_main_menu()
        
        # Ribbon menu
        self.create_ribbon_menu()
        
        # Toolbar
        self.create_toolbar()
        
        # Status line
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
        
        # Bind escape key to close
        self.bind("<Escape>", lambda e: self.quit())
        
    def configure_style(self):
        """Configure ttk styles for the application"""
        # Frame styles
        self.style.configure('TFrame', background=self.bg_dark)
        
        # Notebook styles
        self.style.configure('TNotebook', background=self.bg_darker)
        self.style.configure('TNotebook.Tab', 
                           background=self.bg_darker, 
                           foreground=self.text_color,
                           padding=[10, 2],
                           font=('Segoe UI', 9))
        self.style.map('TNotebook.Tab', 
                     background=[('selected', self.bg_light)],
                     foreground=[('selected', self.highlight_text)])
        
        # Button styles
        self.style.configure('TButton', 
                           background=self.bg_light,
                           foreground=self.text_color,
                           borderwidth=0,
                           font=('Segoe UI', 9))
        self.style.map('TButton',
                      background=[('active', self.highlight_color)],
                      foreground=[('active', self.text_color)])
        
        # Scrollbar styles
        self.style.configure('Vertical.TScrollbar', 
                           background=self.bg_light,
                           troughcolor=self.bg_darker,
                           bordercolor=self.bg_dark,
                           arrowcolor=self.text_color,
                           gripcount=0)
        
        # Entry styles
        self.style.configure('TEntry',
                           fieldbackground=self.bg_light,
                           foreground=self.text_color,
                           insertcolor=self.text_color)
        
    def create_title_bar(self):
        """Create custom title bar with window controls"""
        self.title_bar = tk.Frame(self, bg=self.bg_darker, height=32)
        self.title_bar.pack(fill=tk.X)
        
        # Title label with icon
        title_frame = tk.Frame(self.title_bar, bg=self.bg_darker)
        title_frame.pack(side=tk.LEFT)
        
        # App icon (placeholder)
        self.app_icon = tk.Label(title_frame, text="G", bg=self.bg_darker, 
                               fg=self.accent_color, font=('Arial', 12, 'bold'))
        self.app_icon.pack(side=tk.LEFT, padx=(10, 5))
        
        self.title_label = tk.Label(
            title_frame, 
            text="GKSHALA", 
            bg=self.bg_darker, 
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Document name
        self.doc_label = tk.Label(
            self.title_bar, 
            text="Untitled.gks", 
            bg=self.bg_darker, 
            fg="#aaaaaa",
            font=('Segoe UI', 9)
        )
        self.doc_label.pack(side=tk.LEFT, padx=10)
        
        # Window controls
        controls_frame = tk.Frame(self.title_bar, bg=self.bg_darker)
        controls_frame.pack(side=tk.RIGHT, padx=5)
        
        # Minimize button
        self.minimize_btn = tk.Button(
            controls_frame, 
            text="─", 
            command=self.show_minimized,
            borderwidth=0,
            bg=self.bg_darker,
            fg=self.text_color,
            activebackground='#4d4d4d',
            font=('Segoe UI', 12),
            padx=8
        )
        self.minimize_btn.pack(side=tk.LEFT)
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(
            controls_frame, 
            text="□", 
            command=self.toggle_maximize,
            borderwidth=0,
            bg=self.bg_darker,
            fg=self.text_color,
            activebackground='#4d4d4d',
            font=('Segoe UI', 10),
            padx=8
        )
        self.maximize_btn.pack(side=tk.LEFT)
        
        # Close button
        self.close_btn = tk.Button(
            controls_frame, 
            text="×", 
            command=self.quit,
            borderwidth=0,
            bg=self.bg_darker,
            fg=self.text_color,
            activebackground='#ff4444',
            font=('Segoe UI', 12),
            padx=8
        )
        self.close_btn.pack(side=tk.LEFT)
        
    def create_main_menu(self):
        """Create the main menu bar"""
        menubar = Menu(self, bg=self.bg_darker, fg=self.text_color, 
                      activebackground=self.highlight_color,
                      activeforeground=self.text_color,
                      bd=0)
        
        # File Menu
        file_menu = Menu(menubar, tearoff=0, bg=self.bg_darker, fg=self.text_color,
                        activebackground=self.highlight_color,
                        activeforeground=self.text_color)
        file_menu.add_command(label="New Scene", command=lambda: self.new_scene(), accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Import", command=lambda: None)
        file_menu.add_command(label="Export", command=lambda: None)
        file_menu.add_separator()
        file_menu.add_command(label="Preferences", command=lambda: None)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Alt+F4")
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit Menu
        edit_menu = Menu(menubar, tearoff=0, bg=self.bg_darker, fg=self.text_color,
                        activebackground=self.highlight_color,
                        activeforeground=self.text_color)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Duplicate", accelerator="Ctrl+D")
        edit_menu.add_command(label="Delete", accelerator="Del")
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Create Menu
        create_menu = Menu(menubar, tearoff=0, bg=self.bg_darker, fg=self.text_color,
                          activebackground=self.highlight_color,
                          activeforeground=self.text_color)
        create_menu.add_command(label="Polygon Primitive", command=lambda: None)
        create_menu.add_command(label="NURBS Primitive", command=lambda: None)
        create_menu.add_command(label="Lights", command=lambda: None)
        create_menu.add_command(label="Cameras", command=lambda: None)
        create_menu.add_separator()
        create_menu.add_command(label="Text", command=lambda: None)
        create_menu.add_command(label="Curves", command=lambda: None)
        menubar.add_cascade(label="Create", menu=create_menu)
        
        # Workspace Menu
        workspace_menu = Menu(menubar, tearoff=0, bg=self.bg_darker, fg=self.text_color,
                             activebackground=self.highlight_color,
                             activeforeground=self.text_color)
        workspace_menu.add_command(label="Modeling")
        workspace_menu.add_command(label="Animation")
        workspace_menu.add_command(label("Rendering"))
        workspace_menu.add_command(label("Dynamics"))
        workspace_menu.add_command(label("FX"))
        menubar.add_cascade(label="Workspace", menu=workspace_menu)
        
        # Help Menu
        help_menu = Menu(menubar, tearoff=0, bg=self.bg_darker, fg=self.text_color,
                        activebackground=self.highlight_color,
                        activeforeground=self.text_color)
        help_menu.add_command(label="Documentation", command=lambda: None)
        help_menu.add_command(label="Tutorials", command=lambda: None)
        help_menu.add_separator()
        help_menu.add_command(label="About GKSHALA", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.config(menu=menubar)
    
    def create_ribbon_menu(self):
        """Create ribbon-style menu with tabs"""
        self.ribbon_frame = tk.Frame(self, bg=self.bg_darker)
        self.ribbon_frame.pack(fill=tk.X)
        
        # Ribbon tabs
        self.ribbon_tabs = ttk.Notebook(self.ribbon_frame)
        self.ribbon_tabs.pack(fill=tk.X)
        
        # File Tab
        file_tab = ttk.Frame(self.ribbon_tabs)
        self.create_file_tab(file_tab)
        self.ribbon_tabs.add(file_tab, text="File")
        
        # Home Tab
        home_tab = ttk.Frame(self.ribbon_tabs)
        self.create_home_tab(home_tab)
        self.ribbon_tabs.add(home_tab, text="Home")
        
        # Modeling Tab
        modeling_tab = ttk.Frame(self.ribbon_tabs)
        self.create_modeling_tab(modeling_tab)
        self.ribbon_tabs.add(modeling_tab, text="Modeling")
        
        # Animation Tab
        animation_tab = ttk.Frame(self.ribbon_tabs)
        self.create_animation_tab(animation_tab)
        self.ribbon_tabs.add(animation_tab, text="Animation")
        
        # Render Tab
        render_tab = ttk.Frame(self.ribbon_tabs)
        self.create_render_tab(render_tab)
        self.ribbon_tabs.add(render_tab, text="Render")
        
        # View Tab
        view_tab = ttk.Frame(self.ribbon_tabs)
        self.create_view_tab(view_tab)
        self.ribbon_tabs.add(view_tab, text="View")
    
    def create_file_tab(self, parent):
        """Create content for File tab"""
        # File operations section
        file_group = ttk.LabelFrame(parent, text="File", padding=(5, 5, 5, 5))
        file_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Button icons would be added here in a real app
        ttk.Button(file_group, text="New", command=self.new_scene).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_group, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_group, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_group, text="Save As", command=self.save_file_as).pack(side=tk.LEFT, padx=2)
        
        # Import/Export section
        io_group = ttk.LabelFrame(parent, text="Import/Export", padding=(5, 5, 5, 5))
        io_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(io_group, text="Import").pack(side=tk.LEFT, padx=2)
        ttk.Button(io_group, text="Export").pack(side=tk.LEFT, padx=2)
        ttk.Button(io_group, text="Reference").pack(side=tk.LEFT, padx=2)
    
    def create_home_tab(self, parent):
        """Create content for Home tab"""
        # Selection section
        select_group = ttk.LabelFrame(parent, text="Selection", padding=(5, 5, 5, 5))
        select_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(select_group, text="Select").pack(side=tk.LEFT, padx=2)
        ttk.Button(select_group, text="Lasso Select").pack(side=tk.LEFT, padx=2)
        ttk.Button(select_group, text="Paint Select").pack(side=tk.LEFT, padx=2)
        
        # Transform section
        transform_group = ttk.LabelFrame(parent, text="Transform", padding=(5, 5, 5, 5))
        transform_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(transform_group, text="Move").pack(side=tk.LEFT, padx=2)
        ttk.Button(transform_group, text="Rotate").pack(side=tk.LEFT, padx=2)
        ttk.Button(transform_group, text="Scale").pack(side=tk.LEFT, padx=2)
        ttk.Button(transform_group, text="Universal Manipulator").pack(side=tk.LEFT, padx=2)
        
        # Display section
        display_group = ttk.LabelFrame(parent, text="Display", padding=(5, 5, 5, 5))
        display_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(display_group, text="Wireframe").pack(side=tk.LEFT, padx=2)
        ttk.Button(display_group, text="Shaded").pack(side=tk.LEFT, padx=2)
        ttk.Button(display_group, text="Textured").pack(side=tk.LEFT, padx=2)
        ttk.Button(display_group, text="Lighting").pack(side=tk.LEFT, padx=2)
    
    def create_modeling_tab(self, parent):
        """Create content for Modeling tab"""
        # Polygon section
        poly_group = ttk.LabelFrame(parent, text="Polygon", padding=(5, 5, 5, 5))
        poly_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(poly_group, text="Extrude").pack(side=tk.LEFT, padx=2)
        ttk.Button(poly_group, text="Bevel").pack(side=tk.LEFT, padx=2)
        ttk.Button(poly_group, text="Bridge").pack(side=tk.LEFT, padx=2)
        ttk.Button(poly_group, text="Multi-Cut").pack(side=tk.LEFT, padx=2)
        
        # NURBS section
        nurbs_group = ttk.LabelFrame(parent, text="NURBS", padding=(5, 5, 5, 5))
        nurbs_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(nurbs_group, text="Revolve").pack(side=tk.LEFT, padx=2)
        ttk.Button(nurbs_group, text="Loft").pack(side=tk.LEFT, padx=2)
        ttk.Button(nurbs_group, text="Extrude").pack(side=tk.LEFT, padx=2)
        ttk.Button(nurbs_group, text="Planar").pack(side=tk.LEFT, padx=2)
    
    def create_animation_tab(self, parent):
        """Create content for Animation tab"""
        # Keyframe section
        key_group = ttk.LabelFrame(parent, text="Keyframes", padding=(5, 5, 5, 5))
        key_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(key_group, text="Set Key").pack(side=tk.LEFT, padx=2)
        ttk.Button(key_group, text="Auto Key").pack(side=tk.LEFT, padx=2)
        ttk.Button(key_group, text="Graph Editor").pack(side=tk.LEFT, padx=2)
        ttk.Button(key_group, text="Dope Sheet").pack(side=tk.LEFT, padx=2)
        
        # Rigging section
        rig_group = ttk.LabelFrame(parent, text="Rigging", padding=(5, 5, 5, 5))
        rig_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(rig_group, text="Joint Tool").pack(side=tk.LEFT, padx=2)
        ttk.Button(rig_group, text="IK Handle").pack(side=tk.LEFT, padx=2)
        ttk.Button(rig_group, text="Skin").pack(side=tk.LEFT, padx=2)
        ttk.Button(rig_group, text="Blend Shape").pack(side=tk.LEFT, padx=2)
    
    def create_render_tab(self, parent):
        """Create content for Render tab"""
        # Render section
        render_group = ttk.LabelFrame(parent, text="Render", padding=(5, 5, 5, 5))
        render_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(render_group, text="Render Image").pack(side=tk.LEFT, padx=2)
        ttk.Button(render_group, text="Render Sequence").pack(side=tk.LEFT, padx=2)
        ttk.Button(render_group, text="IPR Render").pack(side=tk.LEFT, padx=2)
        ttk.Button(render_group, text="Render Settings").pack(side=tk.LEFT, padx=2)
        
        # Lighting section
        light_group = ttk.LabelFrame(parent, text="Lighting", padding=(5, 5, 5, 5))
        light_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(light_group, text="Directional Light").pack(side=tk.LEFT, padx=2)
        ttk.Button(light_group, text="Point Light").pack(side=tk.LEFT, padx=2)
        ttk.Button(light_group, text="Spot Light").pack(side=tk.LEFT, padx=2)
        ttk.Button(light_group, text="Area Light").pack(side=tk.LEFT, padx=2)
    
    def create_view_tab(self, parent):
        """Create content for View tab"""
        # Viewport section
        viewport_group = ttk.LabelFrame(parent, text="Viewport", padding=(5, 5, 5, 5))
        viewport_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(viewport_group, text="Perspective").pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_group, text="Orthographic").pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_group, text="Camera").pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_group, text="Look Through Selected").pack(side=tk.LEFT, padx=2)
        
        # Layout section
        layout_group = ttk.LabelFrame(parent, text="Layout", padding=(5, 5, 5, 5))
        layout_group.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(layout_group, text="Single Pane").pack(side=tk.LEFT, padx=2)
        ttk.Button(layout_group, text="Two Pane").pack(side=tk.LEFT, padx=2)
        ttk.Button(layout_group, text="Four Pane").pack(side=tk.LEFT, padx=2)
        ttk.Button(layout_group, text="Save Layout").pack(side=tk.LEFT, padx=2)
    
    def create_toolbar(self):
        """Create the main toolbar"""
        self.toolbar = tk.Frame(self, bg=self.bg_darker, height=40)
        self.toolbar.pack(fill=tk.X)
        
        # Tool buttons
        tools = [
            ("Select", "S"), ("Move", "W"), ("Rotate", "E"), 
            ("Scale", "R"), ("Universal", "T"), ("Soft Select", "B")
        ]
        
        for tool, hotkey in tools:
            btn = tk.Button(
                self.toolbar, 
                text=f"{tool} ({hotkey})", 
                bg=self.bg_light,
                fg=self.text_color,
                activebackground=self.highlight_color,
                bd=0,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        sep = tk.Frame(self.toolbar, bg="#444444", width=1, height=30)
        sep.pack(side=tk.LEFT, padx=5)
        
        # Snapping tools
        snap_tools = [
            ("Snap to Grid", "X"), ("Snap to Curve", "C"), 
            ("Snap to Point", "V")
        ]
        
        for tool, hotkey in snap_tools:
            btn = tk.Button(
                self.toolbar, 
                text=f"{tool} ({hotkey})", 
                bg=self.bg_light,
                fg=self.text_color,
                activebackground=self.highlight_color,
                bd=0,
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_status_line(self):
        """Create status line with coordinate display and selection info"""
        self.status_line = tk.Frame(self, bg=self.bg_darker, height=24)
        self.status_line.pack(fill=tk.X)
        
        # Coordinate display
        coord_frame = tk.Frame(self.status_line, bg=self.bg_darker)
        coord_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(coord_frame, text="X:", bg=self.bg_darker, fg=self.text_color).pack(side=tk.LEFT)
        self.x_coord = tk.Label(coord_frame, text="0.000", bg=self.bg_darker, fg=self.highlight_text, width=8)
        self.x_coord.pack(side=tk.LEFT)
        
        tk.Label(coord_frame, text="Y:", bg=self.bg_darker, fg=self.text_color).pack(side=tk.LEFT)
        self.y_coord = tk.Label(coord_frame, text="0.000", bg=self.bg_darker, fg=self.highlight_text, width=8)
        self.y_coord.pack(side=tk.LEFT)
        
        tk.Label(coord_frame, text="Z:", bg=self.bg_darker, fg=self.text_color).pack(side=tk.LEFT)
        self.z_coord = tk.Label(coord_frame, text="0.000", bg=self.bg_darker, fg=self.highlight_text, width=8)
        self.z_coord.pack(side=tk.LEFT)
        
        # Selection info
        self.selection_info = tk.Label(
            self.status_line, 
            text="Nothing selected", 
            bg=self.bg_darker, 
            fg=self.text_color
        )
        self.selection_info.pack(side=tk.LEFT, padx=20)
        
        # Render stats
        render_stats = tk.Label(
            self.status_line, 
            text="Polygons: 0 | Verts: 0 | Edges: 0 | FPS: 60", 
            bg=self.bg_darker, 
            fg=self.text_color
        )
        render_stats.pack(side=tk.RIGHT, padx=10)
    
    def create_workspace(self):
        """Create the main workspace with viewports"""
        self.workspace = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.bg_dark)
        self.workspace.pack(fill=tk.BOTH, expand=True)
        
        # Left toolbox
        self.toolbox = tk.Frame(self.workspace, width=220, bg=self.bg_darker, bd=0)
        self.create_toolbox()
        self.workspace.add(self.toolbox)
        
        # Main viewport area
        self.viewport_area = tk.PanedWindow(self.workspace, orient=tk.VERTICAL, bg=self.bg_dark)
        self.workspace.add(self.viewport_area, stretch="always")
        
        # Viewport tabs
        self.viewport_tabs = ttk.Notebook(self.viewport_area)
        self.viewport_area.add(self.viewport_tabs, height=400)
        
        # Create viewports
        self.create_viewports()
        
        # Right channel box area
        self.channel_area = tk.Frame(self.workspace, width=300, bg=self.bg_darker)
        self.workspace.add(self.channel_area)
    
    def create_toolbox(self):
        """Create the toolbox on the left side"""
        # Search box
        search_frame = tk.Frame(self.toolbox, bg=self.bg_darker)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(fill=tk.X, padx=2)
        search_entry.insert(0, "Search...")
        
        # Scene hierarchy
        scene_frame = tk.Frame(self.toolbox, bg=self.bg_darker)
        scene_frame.pack(fill=tk.BOTH, expand=True)
        
        scene_label = tk.Label(
            scene_frame, 
            text="Scene Hierarchy", 
            bg=self.bg_darker, 
            fg=self.text_color,
            font=('Segoe UI', 9, 'bold')
        )
        scene_label.pack(fill=tk.X, pady=(5, 0))
        
        # Treeview for scene hierarchy
        self.scene_tree = ttk.Treeview(
            scene_frame,
            columns=('type'),
            show='tree',
            selectmode='browse'
        )
        
        # Configure style for treeview
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.bg_darker,
                       fieldbackground=self.bg_darker,
                       foreground=self.text_color)
        style.map("Treeview", 
                background=[('selected', self.highlight_color)],
                foreground=[('selected', self.text_color)])
        
        self.scene_tree.heading('#0', text='Name', anchor=tk.W)
        self.scene_tree.heading('type', text='Type', anchor=tk.W)
        
        # Add sample items
        root_node = self.scene_tree.insert('', 'end', text='Scene', open=True)
        self.scene_tree.insert(root_node, 'end', text='pCube1', values=('Polygon'))
        self.scene_tree.insert(root_node, 'end', text='pSphere1', values=('Polygon'))
        self.scene_tree.insert(root_node, 'end', text='light1', values=('Light'))
        self.scene_tree.insert(root_node, 'end', text='camera1', values=('Camera'))
        
        self.scene_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_viewports(self):
        """Create viewports with gridlines"""
        # Perspective view
        perspective = tk.Frame(self.viewport_tabs)
        self.perspective_canvas = tk.Canvas(
            perspective, 
            bg=self.bg_dark,
            highlightthickness=0
        )
        self.perspective_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(self.perspective_canvas)
        
        # Add viewport controls
        viewport_controls = tk.Frame(perspective, bg=self.bg_darker)
        viewport_controls.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(viewport_controls, text="Persp", width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_controls, text="Shaded", width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_controls, text="Grid", width=4).pack(side=tk.LEFT, padx=2)
        ttk.Button(viewport_controls, text="Axis", width=4).pack(side=tk.LEFT, padx=2)
        
        self.viewport_tabs.add(perspective, text="Perspective")
        
        # Front view
        front = tk.Frame(self.viewport_tabs)
        front_canvas = tk.Canvas(front, bg=self.bg_dark, highlightthickness=0)
        front_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(front_canvas)
        
        # Front view controls
        front_controls = tk.Frame(front, bg=self.bg_darker)
        front_controls.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(front_controls, text="Front", width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(front_controls, text="Wireframe", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(front_controls, text="Grid", width=4).pack(side=tk.LEFT, padx=2)
        ttk.Button(front_controls, text="Axis", width=4).pack(side=tk.LEFT, padx=2)
        
        self.viewport_tabs.add(front, text="Front")
        
        # Side view
        side = tk.Frame(self.viewport_tabs)
        side_canvas = tk.Canvas(side, bg=self.bg_dark, highlightthickness=0)
        side_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(side_canvas)
        
        # Side view controls
        side_controls = tk.Frame(side, bg=self.bg_darker)
        side_controls.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(side_controls, text="Side", width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(side_controls, text="Wireframe", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(side_controls, text="Grid", width=4).pack(side=tk.LEFT, padx=2)
        ttk.Button(side_controls, text="Axis", width=4).pack(side=tk.LEFT, padx=2)
        
        self.viewport_tabs.add(side, text="Side")
        
        # Top view
        top = tk.Frame(self.viewport_tabs)
        top_canvas = tk.Canvas(top, bg=self.bg_dark, highlightthickness=0)
        top_canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_grid(top_canvas)
        
        # Top view controls
        top_controls = tk.Frame(top, bg=self.bg_darker)
        top_controls.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(top_controls, text="Top", width=6).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_controls, text="Wireframe", width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_controls, text="Grid", width=4).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_controls, text="Axis", width=4).pack(side=tk.LEFT, padx=2)
        
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
        self.channel_notebook = ttk.Notebook(self.channel_area)
        self.channel_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Channel Box Tab
        channel_tab = tk.Frame(self.channel_notebook, bg=self.bg_darker)
        self.channel_notebook.add(channel_tab, text="Channel Box")
        
        # Title Label
        title = tk.Label(
            channel_tab, 
            text="pCube1", 
            bg=self.bg_light, 
            fg=self.text_color,
            font=("Segoe UI", 10, "bold"),
            padx=5,
            anchor=tk.W
        )
        title.pack(fill=tk.X)
        
        # Scrollable frame for attributes
        scroll_frame = tk.Frame(channel_tab, bg=self.bg_darker)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=self.bg_darker, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_darker)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add sample attributes
        transform_attrs = [
            ("Translate X", "0.000"),
            ("Translate Y", "0.000"),
            ("Translate Z", "0.000"),
            ("Rotate X", "0.000"),
            ("Rotate Y", "0.000"),
            ("Rotate Z", "0.000"),
            ("Scale X", "1.000"),
            ("Scale Y", "1.000"),
            ("Scale Z", "1.000"),
            ("Visibility", "on")
        ]
        
        for attr, value in transform_attrs:
            attr_frame = tk.Frame(scrollable_frame, bg=self.bg_darker)
            attr_frame.pack(fill=tk.X, padx=5, pady=1)
            
            tk.Label(
                attr_frame, 
                text=attr, 
                bg=self.bg_darker, 
                fg=self.text_color,
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Entry(
                attr_frame, 
                bg=self.bg_light,
                fg=self.text_color,
                insertbackground=self.text_color,
                bd=0,
                width=10
            ).pack(side=tk.RIGHT)
            attr_frame.children['!entry'].insert(0, value)
        
        # Shape Node Tab
        shape_tab = tk.Frame(self.channel_notebook, bg=self.bg_darker)
        self.channel_notebook.add(shape_tab, text="Shape Node")
        
        # Layer Editor Tab
        layer_tab = tk.Frame(self.channel_notebook, bg=self.bg_darker)
        self.channel_notebook.add(layer_tab, text="Layer Editor")
    
    def create_attribute_editor(self):
        """Create the attribute editor below the viewports"""
        self.attribute_editor = ttk.Notebook(self.viewport_area)
        self.viewport_area.add(self.attribute_editor)
        
        # Node Attributes Tab
        node_tab = tk.Frame(self.attribute_editor, bg=self.bg_darker)
        
        # Scrollable area
        scroll_frame = tk.Frame(node_tab, bg=self.bg_darker)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(scroll_frame, bg=self.bg_darker, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_darker)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Transform attributes section
        transform_frame = tk.LabelFrame(
            scrollable_frame, 
            text="Transform Attributes", 
            bg=self.bg_darker,
            fg=self.text_color,
            padx=5,
            pady=5
        )
        transform_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add transform attributes
        transform_attrs = [
            ("Translate", ["X", "0.000"], ["Y", "0.000"], ["Z", "0.000"]),
            ("Rotate", ["X", "0.000"], ["Y", "0.000"], ["Z", "0.000"]),
            ("Scale", ["X", "1.000"], ["Y", "1.000"], ["Z", "1.000"]),
            ("Visibility", ["", "on"])
        ]
        
        for attr_group in transform_attrs:
            group_frame = tk.Frame(transform_frame, bg=self.bg_darker)
            group_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                group_frame, 
                text=attr_group[0], 
                bg=self.bg_darker, 
                fg=self.text_color,
                width=12,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            for attr in attr_group[1:]:
                if attr[0]:  # If there's an axis label
                    tk.Label(
                        group_frame, 
                        text=attr[0], 
                        bg=self.bg_darker, 
                        fg=self.text_color,
                        width=1
                    ).pack(side=tk.LEFT)
                
                tk.Entry(
                    group_frame, 
                    bg=self.bg_light,
                    fg=self.text_color,
                    insertbackground=self.text_color,
                    bd=0,
                    width=8
                ).pack(side=tk.LEFT, padx=2)
                group_frame.children['!entry'].insert(0, attr[1])
        
        # Add more attribute sections (Pivot, Limits, etc.)
        sections = ["Pivot", "Limits", "Display"]
        for section in sections:
            section_frame = tk.LabelFrame(
                scrollable_frame, 
                text=f"{section} Attributes", 
                bg=self.bg_darker,
                fg=self.text_color,
                padx=5,
                pady=5
            )
            section_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Add some dummy controls
            for i in range(3):
                tk.Checkbutton(
                    section_frame,
                    text=f"{section} Option {i+1}",
                    bg=self.bg_darker,
                    fg=self.text_color,
                    activebackground=self.bg_darker,
                    activeforeground=self.text_color,
                    selectcolor=self.bg_darker
                ).pack(anchor=tk.W)
        
        self.attribute_editor.add(node_tab, text="pCube1")
        
        # Material Tab
        material_tab = tk.Frame(self.attribute_editor, bg=self.bg_darker)
        self.attribute_editor.add(material_tab, text="lambert1")
        
        # Render Tab
        render_tab = tk.Frame(self.attribute_editor, bg=self.bg_darker)
        self.attribute_editor.add(render_tab, text="Render Stats")
    
    def create_time_slider(self):
        """Create the time slider at the bottom"""
        self.time_slider_frame = tk.Frame(self, bg=self.bg_darker)
        self.time_slider_frame.pack(fill=tk.X)
        
        # Playback controls
        controls_frame = tk.Frame(self.time_slider_frame, bg=self.bg_darker)
        controls_frame.pack(side=tk.LEFT, padx=5)
        
        # Transport controls
        transport_buttons = [
            ("⏮", self.rewind),
            ("⏪", self.step_back),
            ("▶", self.play),
            ("⏸", self.pause),
            ("⏩", self.step_forward),
            ("⏭", self.fast_forward),
            ("⏹", self.stop)
        ]
        
        for text, cmd in transport_buttons:
            btn = tk.Button(
                controls_frame, 
                text=text, 
                command=cmd,
                bg=self.bg_light,
                fg=self.text_color,
                activebackground=self.highlight_color,
                bd=0,
                padx=5
            )
            btn.pack(side=tk.LEFT, padx=1)
        
        # Time slider
        self.time_slider = tk.Scale(
            self.time_slider_frame, 
            from_=1, 
            to=100, 
            orient=tk.HORIZONTAL,
            bg=self.bg_light,
            fg=self.text_color,
            troughcolor=self.bg_dark,
            highlightthickness=0,
            bd=0,
            command=self.update_frame
        )
        self.time_slider.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Current frame indicator
        self.frame_var = tk.StringVar(value="Frame: 1")
        frame_label = tk.Label(
            self.time_slider_frame, 
            textvariable=self.frame_var, 
            bg=self.bg_darker,
            fg=self.text_color,
            padx=10
        )
        frame_label.pack(side=tk.RIGHT)
        
        # Range controls
        range_frame = tk.Frame(self.time_slider_frame, bg=self.bg_darker)
        range_frame.pack(side=tk.RIGHT)
        
        tk.Label(range_frame, text="Start:", bg=self.bg_darker, fg=self.text_color).pack(side=tk.LEFT)
        start_entry = ttk.Entry(range_frame, width=4)
        start_entry.pack(side=tk.LEFT)
        start_entry.insert(0, "1")
        
        tk.Label(range_frame, text="End:", bg=self.bg_darker, fg=self.text_color).pack(side=tk.LEFT)
        end_entry = ttk.Entry(range_frame, width=4)
        end_entry.pack(side=tk.LEFT)
        end_entry.insert(0, "100")
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Frame(self, bg=self.bg_darker, height=24)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Left side - status message
        self.status_message = tk.Label(
            self.status_bar, 
            text="Ready", 
            bg=self.bg_darker,
            fg=self.text_color,
            anchor=tk.W
        )
        self.status_message.pack(side=tk.LEFT, padx=10)
        
        # Right side - zoom level and other info
        zoom_label = tk.Label(
            self.status_bar, 
            text="Zoom: 100%", 
            bg=self.bg_darker,
            fg=self.text_color
        )
        zoom_label.pack(side=tk.RIGHT, padx=10)
        
        # Render resolution
        res_label = tk.Label(
            self.status_bar, 
            text="1920x1080", 
            bg=self.bg_darker,
            fg=self.text_color
        )
        res_label.pack(side=tk.RIGHT, padx=10)
        
        # Memory usage
        mem_label = tk.Label(
            self.status_bar, 
            text="Mem: 1.2GB", 
            bg=self.bg_darker,
            fg=self.text_color
        )
        mem_label.pack(side=tk.RIGHT, padx=10)
    
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
        self.doc_label.config(text="Untitled.gks")
        self.status_message.config(text="New scene created")
        self.after(3000, lambda: self.status_message.config(text="Ready"))
    
    def save_file(self):
        """Handle save file action"""
        if self.current_file:
            # In a real app, you would save the file here
            self.status_message.config(text=f"Saved {self.current_file}")
            self.after(3000, lambda: self.status_message.config(text="Ready"))
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
            self.doc_label.config(text=file_path.split("/")[-1])
            # In a real app, you would save the file here
            self.status_message.config(text=f"Saved as {file_path}")
            self.after(3000, lambda: self.status_message.config(text="Ready"))
    
    def open_file(self):
        """Handle open file action"""
        file_path = filedialog.askopenfilename(
            filetypes=[("GKSHALA Files", "*.gks"), ("All Files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            self.doc_label.config(text=file_path.split("/")[-1])
            # In a real app, you would open the file here
            self.status_message.config(text=f"Opened {file_path}")
            self.after(3000, lambda: self.status_message.config(text="Ready"))
    
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
    
    def show_about(self):
        """Show about dialog"""
        about = tk.Toplevel(self)
        about.title("About GKSHALA")
        about.geometry("400x300")
        about.resizable(False, False)
        
        # Center the window
        window_width = about.winfo_reqwidth()
        window_height = about.winfo_reqheight()
        position_right = int(about.winfo_screenwidth()/2 - window_width/2)
        position_down = int(about.winfo_screenheight()/2 - window_height/2)
        about.geometry(f"+{position_right}+{position_down}")
        
        # Content
        logo = tk.Label(about, text="GKSHALA", font=("Arial", 24, "bold"), fg=self.accent_color)
        logo.pack(pady=20)
        
        version = tk.Label(about, text="Version 1.0.0", font=("Arial", 10))
        version.pack()
        
        desc = tk.Label(about, text="Professional 3D Animation and Modeling Suite", font=("Arial", 12))
        desc.pack(pady=10)
        
        copyright = tk.Label(about, text="© 2023 GKSHALA Team. All rights reserved.", font=("Arial", 8))
        copyright.pack(side=tk.BOTTOM, pady=10)
    
    def play(self):
        """Start animation playback"""
        if not self.playback_active:
            self.playback_active = True
            self.animate()
    
    def pause(self):
        """Pause animation playback"""
        self.playback_active = False
    
    def stop(self):
        """Stop animation and reset to frame 1"""
        self.playback_active = False
        self.current_frame = 1
        self.time_slider.set(1)
        self.update_frame(1)
    
    def rewind(self):
        """Go to first frame"""
        self.current_frame = 1
        self.time_slider.set(1)
        self.update_frame(1)
    
    def fast_forward(self):
        """Go to last frame"""
        self.current_frame = 100
        self.time_slider.set(100)
        self.update_frame(100)
    
    def step_back(self):
        """Go to previous frame"""
        if self.current_frame > 1:
            self.current_frame -= 1
            self.time_slider.set(self.current_frame)
            self.update_frame(self.current_frame)
    
    def step_forward(self):
        """Go to next frame"""
        if self.current_frame < 100:
            self.current_frame += 1
            self.time_slider.set(self.current_frame)
            self.update_frame(self.current_frame)
    
    def animate(self):
        """Animate the timeline"""
        if self.playback_active and self.current_frame < 100:
            self.current_frame += 1
            self.time_slider.set(self.current_frame)
            self.update_frame(self.current_frame)
            self.after(50, self.animate)
        else:
            self.playback_active = False
    
    def update_frame(self, frame):
        """Update current frame display"""
        self.current_frame = int(frame)
        self.frame_var.set(f"Frame: {self.current_frame}")

if __name__ == "__main__":
    app = GKSHALA()
    app.mainloop()