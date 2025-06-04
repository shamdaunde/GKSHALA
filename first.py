import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class GKSHALA(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA")
        self.geometry("1000x700")
        self.minsize(1000, 700)
        
        # Remove window decorations (title bar)
        self.overrideredirect(True)
        
        # Variables
        self.current_file = None
        self.is_maximized = False
        
        # Custom title bar
        self.create_title_bar()
        
        # Ribbon menu
        self.create_ribbon_menu()
        
        # Central area
        self.create_central_area()
        
        # Status bar
        self.create_status_bar()
        
        # Bindings for window dragging
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_move)
        
    def create_title_bar(self):
        """Create custom title bar with window controls"""
        self.title_bar = tk.Frame(self, bg='white', height=32)
        self.title_bar.pack(fill=tk.X)
        
        # Title label
        self.title_label = tk.Label(
            self.title_bar, 
            text="GKSHALA", 
            bg='white', 
            fg='black',
            font=('Arial', 14)
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Window controls
        controls_frame = tk.Frame(self.title_bar, bg='white')
        controls_frame.pack(side=tk.RIGHT, padx=5)
        
        # Minimize button
        self.minimize_btn = tk.Button(
            controls_frame, 
            text="🗕", 
            command=self.show_minimized,
            borderwidth=0,
            bg='white',
            activebackground='#e0e0e0'
        )
        self.minimize_btn.pack(side=tk.LEFT, padx=2)
        
        # Maximize/Restore button
        self.maximize_btn = tk.Button(
            controls_frame, 
            text="🗖", 
            command=self.toggle_maximize,
            borderwidth=0,
            bg='white',
            activebackground='#e0e0e0'
        )
        self.maximize_btn.pack(side=tk.LEFT, padx=2)
        
        # Close button
        self.close_btn = tk.Button(
            controls_frame, 
            text="✕", 
            command=self.quit,
            borderwidth=0,
            bg='white',
            activebackground='#e0e0e0'
        )
        self.close_btn.pack(side=tk.LEFT, padx=2)
        
    def create_ribbon_menu(self):
        """Create ribbon-style menu with tabs"""
        self.ribbon_menu = ttk.Notebook(self)
        self.ribbon_menu.pack(fill=tk.X)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TNotebook', background='#0078D7')
        style.configure('TNotebook.Tab', background='#0078D7', foreground='white')
        style.map('TNotebook.Tab', 
                 background=[('selected', '#005499')])
        
        # File Tab
        file_tab = tk.Frame(self.ribbon_menu, bg='#0078D7')
        self.create_file_tab(file_tab)
        self.ribbon_menu.add(file_tab, text="File")
        
        # Insert Tab
        insert_tab = tk.Frame(self.ribbon_menu, bg='#0078D7')
        self.create_insert_tab(insert_tab)
        self.ribbon_menu.add(insert_tab, text="Insert")
        
        # Animation Tab
        animation_tab = tk.Frame(self.ribbon_menu, bg='#0078D7')
        self.create_animation_tab(animation_tab)
        self.ribbon_menu.add(animation_tab, text="Animation")
        
        # View Tab
        view_tab = tk.Frame(self.ribbon_menu, bg='#0078D7')
        self.create_view_tab(view_tab)
        self.ribbon_menu.add(view_tab, text="View")
        
        # Help Tab
        help_tab = tk.Frame(self.ribbon_menu, bg='#0078D7')
        self.create_help_tab(help_tab)
        self.ribbon_menu.add(help_tab, text="Help")
    
    def create_file_tab(self, parent):
        """Create content for File tab"""
        file_group = tk.LabelFrame(
            parent, 
            text="File", 
            bg='#0078D7', 
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
            bg='#0078D7',
            fg='white',
            activebackground='#005499',
            activeforeground='white',
            bd=0
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save As button
        save_as_btn = tk.Button(
            file_group, 
            text="Save As", 
            command=self.save_file_as,
            bg='#0078D7',
            fg='white',
            activebackground='#005499',
            activeforeground='white',
            bd=0
        )
        save_as_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Recent button with dropdown
        recent_btn = tk.Menubutton(
            file_group, 
            text="Recent", 
            bg='#0078D7',
            fg='white',
            activebackground='#005499',
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
            bg='#0078D7', 
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
                bg='#0078D7',
                fg='white',
                activebackground='#005499',
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
            bg='#0078D7', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        entrance_group.pack(fill=tk.X, padx=5, pady=5)
        
        for anim in ["Fade", "Fly In", "Bounce"]:
            btn = tk.Button(
                entrance_group, 
                text=anim, 
                bg='#0078D7',
                fg='white',
                activebackground='#005499',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Exit animations
        exit_group = tk.LabelFrame(
            parent, 
            text="Exit", 
            bg='#0078D7', 
            fg='white',
            bd=1,
            relief=tk.SOLID
        )
        exit_group.pack(fill=tk.X, padx=5, pady=5)
        
        for anim in ["Fade Out", "Fly Out", "Shrink"]:
            btn = tk.Button(
                exit_group, 
                text=anim, 
                bg='#0078D7',
                fg='white',
                activebackground='#005499',
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
            bg='#0078D7', 
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
                bg='#0078D7',
                fg='white',
                activebackground='#005499',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Show/hide options
        show_group = tk.LabelFrame(
            parent, 
            text="Show", 
            bg='#0078D7', 
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
                bg='#0078D7',
                fg='white',
                activebackground='#0078D7',
                activeforeground='white',
                selectcolor='#0078D7'
            )
            cb.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_help_tab(self, parent):
        """Create content for Help tab"""
        help_buttons = ["Help", "About", "Check for Updates"]
        
        for text in help_buttons:
            btn = tk.Button(
                parent, 
                text=text, 
                bg='#0078D7',
                fg='white',
                activebackground='#005499',
                activeforeground='white',
                bd=0
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_central_area(self):
        """Create the central tabbed area"""
        self.central_tabs = ttk.Notebook(self)
        self.central_tabs.pack(fill=tk.BOTH, expand=True)
        
        # Add a default tab
        default_tab = tk.Frame(self.central_tabs)
        self.central_tabs.add(default_tab, text="Untitled")
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X)
    
    def show_minimized(self):
        """Minimize the window"""
        self.iconify()
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            self.geometry(self.normal_geometry)
            self.maximize_btn.config(text="🗖")
            self.is_maximized = False
        else:
            self.normal_geometry = self.geometry()
            self.state('zoomed')
            self.maximize_btn.config(text="🗗")
            self.is_maximized = True
    
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