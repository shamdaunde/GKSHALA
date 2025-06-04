import tkinter as tk
from tkinter import ttk, font
from tkinter import messagebox

class PowerPointLikeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("PowerPoint-Like Application")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Color theme
        self.theme = {
            'primary': '#2b579a',
            'secondary': '#3178c6',
            'accent': '#e6a23c',
            'background': '#f5f5f5',
            'text': '#333333',
            'highlight': '#ffd700'
        }
        
        # Current active tab
        self.active_tab = None
        
        # Create UI
        self.create_menubar()
        self.create_ribbon()
        self.create_toolbar()
        self.create_workspace()
        self.create_statusbar()
        
    def create_menubar(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self, bg=self.theme['background'], fg=self.theme['text'])
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=lambda: self.new_presentation())
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Print", command=lambda: None)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: None)
        edit_menu.add_command(label="Redo", command=lambda: None)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: None)
        edit_menu.add_command(label="Copy", command=lambda: None)
        edit_menu.add_command(label="Paste", command=lambda: None)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Normal", command=lambda: None)
        view_menu.add_command(label="Slide Sorter", command=lambda: None)
        view_menu.add_command(label="Reading View", command=lambda: None)
        view_menu.add_separator()
        view_menu.add_command(label="Ruler", command=self.toggle_ruler)
        view_menu.add_command(label="Gridlines", command=self.toggle_gridlines)
        view_menu.add_command(label="Guides", command=self.toggle_guides)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.config(menu=menubar)
    
    def create_ribbon(self):
        """Create the ribbon menu with tabs"""
        self.ribbon_frame = tk.Frame(self, bg=self.theme['primary'], height=120)
        self.ribbon_frame.pack(fill=tk.X)
        
        # Ribbon tabs
        self.ribbon_tabs = ttk.Notebook(self.ribbon_frame)
        self.ribbon_tabs.pack(fill=tk.BOTH)
        
        # Create all tabs
        self.create_home_tab()
        self.create_insert_tab()
        self.create_design_tab()
        self.create_transitions_tab()
        self.create_animations_tab()
        self.create_slideshow_tab()
        self.create_review_tab()
        self.create_view_tab()
        
        # Set default tab
        self.ribbon_tabs.select(0)
        self.active_tab = "Home"
    
    def create_home_tab(self):
        """Home tab with clipboard, slides, font, etc."""
        home_tab = ttk.Frame(self.ribbon_tabs)
        
        # Clipboard group
        clipboard_group = ttk.LabelFrame(home_tab, text="Clipboard", padding=5)
        clipboard_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(clipboard_group, text="Paste", width=10).pack(pady=2)
        ttk.Button(clipboard_group, text="Cut", width=10).pack(pady=2)
        ttk.Button(clipboard_group, text="Copy", width=10).pack(pady=2)
        ttk.Button(clipboard_group, text="Format Painter", width=10).pack(pady=2)
        
        # Slides group
        slides_group = ttk.LabelFrame(home_tab, text="Slides", padding=5)
        slides_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(slides_group, text="New Slide", width=10).pack(pady=2)
        ttk.Button(slides_group, text="Layout", width=10).pack(pady=2)
        ttk.Button(slides_group, text="Reset", width=10).pack(pady=2)
        
        # Font group
        font_group = ttk.LabelFrame(home_tab, text="Font", padding=5)
        font_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        font_family = ttk.Combobox(font_group, values=["Arial", "Calibri", "Times New Roman"], width=12)
        font_family.pack(pady=2)
        font_family.set("Calibri")
        
        font_size = ttk.Combobox(font_group, values=["8", "10", "12", "14", "16", "18", "20", "24", "28", "32", "36"], width=5)
        font_size.pack(pady=2)
        font_size.set("12")
        
        ttk.Button(font_group, text="Bold", width=10).pack(pady=2)
        ttk.Button(font_group, text="Italic", width=10).pack(pady=2)
        ttk.Button(font_group, text="Underline", width=10).pack(pady=2)
        
        self.ribbon_tabs.add(home_tab, text="Home")
    
    def create_insert_tab(self):
        """Insert tab with shapes, images, charts, etc."""
        insert_tab = ttk.Frame(self.ribbon_tabs)
        
        # Tables group
        tables_group = ttk.LabelFrame(insert_tab, text="Tables", padding=5)
        tables_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(tables_group, text="Table", width=10).pack(pady=2)
        
        # Images group
        images_group = ttk.LabelFrame(insert_tab, text="Images", padding=5)
        images_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(images_group, text="Pictures", width=10).pack(pady=2)
        ttk.Button(images_group, text="Screenshot", width=10).pack(pady=2)
        
        # Shapes group
        shapes_group = ttk.LabelFrame(insert_tab, text="Shapes", padding=5)
        shapes_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        shapes = ["Rectangle", "Oval", "Arrow", "Star", "Equation"]
        for shape in shapes:
            ttk.Button(shapes_group, text=shape, width=10).pack(pady=2)
        
        # Comments group
        comments_group = ttk.LabelFrame(insert_tab, text="Comments", padding=5)
        comments_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(comments_group, text="New Comment", width=10).pack(pady=2)
        
        self.ribbon_tabs.add(insert_tab, text="Insert")
    
    def create_design_tab(self):
        """Design tab with themes, variants, etc."""
        design_tab = ttk.Frame(self.ribbon_tabs)
        
        # Themes group
        themes_group = ttk.LabelFrame(design_tab, text="Themes", padding=5)
        themes_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        themes = ["Office", "Facet", "Ion", "Retrospect"]
        for theme in themes:
            ttk.Button(themes_group, text=theme, width=10).pack(pady=2)
        
        # Variants group
        variants_group = ttk.LabelFrame(design_tab, text="Variants", padding=5)
        variants_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        variants = ["Color Variants", "Font Variants", "Effect Variants"]
        for variant in variants:
            ttk.Button(variants_group, text=variant, width=12).pack(pady=2)
        
        self.ribbon_tabs.add(design_tab, text="Design")
    
    def create_transitions_tab(self):
        """Transitions tab with slide transitions"""
        transition_tab = ttk.Frame(self.ribbon_tabs)
        
        # Transition to this slide group
        transition_group = ttk.LabelFrame(transition_tab, text="Transition to This Slide", padding=5)
        transition_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        transitions = ["None", "Fade", "Push", "Wipe", "Split"]
        for transition in transitions:
            ttk.Button(transition_group, text=transition, width=10).pack(pady=2)
        
        # Timing group
        timing_group = ttk.LabelFrame(transition_tab, text="Timing", padding=5)
        timing_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(timing_group, text="Duration", width=10).pack(pady=2)
        ttk.Button(timing_group, text="Advance Slide", width=10).pack(pady=2)
        
        self.ribbon_tabs.add(transition_tab, text="Transitions")
    
    def create_animations_tab(self):
        """Animations tab with animation effects"""
        animation_tab = ttk.Frame(self.ribbon_tabs)
        
        # Animation group
        animation_group = ttk.LabelFrame(animation_tab, text="Animation", padding=5)
        animation_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        animations = ["None", "Appear", "Fade", "Fly In", "Float In"]
        for animation in animations:
            ttk.Button(animation_group, text=animation, width=10).pack(pady=2)
        
        # Advanced animation group
        advanced_group = ttk.LabelFrame(animation_tab, text="Advanced Animation", padding=5)
        advanced_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(advanced_group, text="Add Animation", width=12).pack(pady=2)
        ttk.Button(advanced_group, text="Animation Pane", width=12).pack(pady=2)
        
        self.ribbon_tabs.add(animation_tab, text="Animations")
    
    def create_slideshow_tab(self):
        """Slideshow tab with presentation settings"""
        slideshow_tab = ttk.Frame(self.ribbon_tabs)
        
        # Start slideshow group
        start_group = ttk.LabelFrame(slideshow_tab, text="Start Slideshow", padding=5)
        start_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(start_group, text="From Beginning", width=12).pack(pady=2)
        ttk.Button(start_group, text="From Current Slide", width=12).pack(pady=2)
        
        # Set up group
        setup_group = ttk.LabelFrame(slideshow_tab, text="Set Up", padding=5)
        setup_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(setup_group, text="Set Up Slide Show", width=12).pack(pady=2)
        ttk.Button(setup_group, text="Rehearse Timings", width=12).pack(pady=2)
        
        self.ribbon_tabs.add(slideshow_tab, text="Slide Show")
    
    def create_review_tab(self):
        """Review tab with proofing tools"""
        review_tab = ttk.Frame(self.ribbon_tabs)
        
        # Proofing group
        proofing_group = ttk.LabelFrame(review_tab, text="Proofing", padding=5)
        proofing_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(proofing_group, text="Spelling", width=10).pack(pady=2)
        ttk.Button(proofing_group, text="Thesaurus", width=10).pack(pady=2)
        
        # Comments group
        comments_group = ttk.LabelFrame(review_tab, text="Comments", padding=5)
        comments_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(comments_group, text="New Comment", width=10).pack(pady=2)
        ttk.Button(comments_group, text="Delete", width=10).pack(pady=2)
        
        self.ribbon_tabs.add(review_tab, text="Review")
    
    def create_view_tab(self):
        """View tab with presentation views"""
        view_tab = ttk.Frame(self.ribbon_tabs)
        
        # Presentation views group
        views_group = ttk.LabelFrame(view_tab, text="Presentation Views", padding=5)
        views_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(views_group, text="Normal", width=10).pack(pady=2)
        ttk.Button(views_group, text="Slide Sorter", width=10).pack(pady=2)
        ttk.Button(views_group, text="Reading View", width=10).pack(pady=2)
        
        # Show group
        show_group = ttk.LabelFrame(view_tab, text="Show", padding=5)
        show_group.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        ttk.Button(show_group, text="Ruler", width=10).pack(pady=2)
        ttk.Button(show_group, text="Gridlines", width=10).pack(pady=2)
        ttk.Button(show_group, text="Guides", width=10).pack(pady=2)
        
        self.ribbon_tabs.add(view_tab, text="View")
    
    def create_toolbar(self):
        """Create the dynamic toolbar that changes with ribbon tabs"""
        self.toolbar_frame = tk.Frame(self, bg=self.theme['background'], height=40)
        self.toolbar_frame.pack(fill=tk.X)
        
        # Default toolbar (Home tab tools)
        self.update_toolbar("Home")
    
    def update_toolbar(self, tab_name):
        """Update the toolbar based on the active ribbon tab"""
        # Clear previous toolbar
        for widget in self.toolbar_frame.winfo_children():
            widget.destroy()
        
        # Add tools based on active tab
        if tab_name == "Home":
            tools = ["Paste", "Cut", "Copy", "Format Painter", "New Slide", "Font", "Font Size", "Bold", "Italic"]
        elif tab_name == "Insert":
            tools = ["Table", "Pictures", "Shapes", "Icons", "Chart", "SmartArt", "Screenshot"]
        elif tab_name == "Design":
            tools = ["Themes", "Variants", "Customize", "Slide Size", "Format Background"]
        elif tab_name == "Transitions":
            tools = ["None", "Fade", "Push", "Wipe", "Split", "Duration", "Advance Slide"]
        elif tab_name == "Animations":
            tools = ["None", "Appear", "Fade", "Fly In", "Float In", "Add Animation", "Animation Pane"]
        elif tab_name == "Slide Show":
            tools = ["From Beginning", "From Current Slide", "Set Up Slide Show", "Rehearse Timings"]
        elif tab_name == "Review":
            tools = ["Spelling", "Thesaurus", "New Comment", "Delete Comment"]
        elif tab_name == "View":
            tools = ["Normal", "Slide Sorter", "Reading View", "Ruler", "Gridlines", "Guides"]
        
        # Add tools to toolbar
        for tool in tools:
            btn = tk.Button(self.toolbar_frame, text=tool, bg=self.theme['background'], 
                           relief=tk.FLAT, padx=8, pady=4)
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_workspace(self):
        """Create the main workspace area"""
        self.workspace_frame = tk.Frame(self, bg='white')
        self.workspace_frame.pack(fill=tk.BOTH, expand=True)
        
        # Slide canvas
        self.slide_canvas = tk.Canvas(self.workspace_frame, bg='white', highlightthickness=0)
        self.slide_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add a sample slide
        self.draw_sample_slide()
        
        # Ruler (initially hidden)
        self.ruler_frame = tk.Frame(self.workspace_frame, bg='lightgray', height=20)
        self.ruler_visible = False
        
        # Comment box (initially hidden)
        self.comment_frame = tk.Frame(self.workspace_frame, bg='white', width=200, 
                                    borderwidth=1, relief=tk.SUNKEN)
        self.comment_visible = False
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.workspace_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.slide_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.slide_canvas.yview)
    
    def draw_sample_slide(self):
        """Draw a sample slide in the workspace"""
        self.slide_canvas.delete("all")
        width = self.slide_canvas.winfo_width()
        height = self.slide_canvas.winfo_height()
        
        # Slide background
        self.slide_canvas.create_rectangle(50, 50, width-50, height-50, 
                                         fill='white', outline='lightgray', width=2)
        
        # Title placeholder
        self.slide_canvas.create_text(width/2, 80, text="Click to add title", 
                                    font=('Arial', 24), fill='lightgray')
        
        # Content placeholder
        self.slide_canvas.create_text(width/2, height/2, text="Click to add text", 
                                    font=('Arial', 16), fill='lightgray')
    
    def create_statusbar(self):
        """Create the status bar at bottom"""
        self.statusbar = tk.Frame(self, bg=self.theme['primary'], height=24)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label
        self.status_label = tk.Label(self.statusbar, text="Ready", bg=self.theme['primary'], 
                                   fg='white', anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Zoom control
        zoom_frame = tk.Frame(self.statusbar, bg=self.theme['primary'])
        zoom_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(zoom_frame, text="Zoom Out", width=8).pack(side=tk.LEFT)
        zoom_label = tk.Label(zoom_frame, text="100%", bg=self.theme['primary'], fg='white')
        zoom_label.pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Zoom In", width=8).pack(side=tk.LEFT)
    
    def toggle_ruler(self):
        """Toggle ruler visibility"""
        self.ruler_visible = not self.ruler_visible
        if self.ruler_visible:
            self.ruler_frame.pack(fill=tk.X, before=self.slide_canvas)
        else:
            self.ruler_frame.pack_forget()
    
    def toggle_gridlines(self):
        """Toggle gridlines visibility"""
        messagebox.showinfo("Info", "Gridlines toggled")
    
    def toggle_guides(self):
        """Toggle guides visibility"""
        messagebox.showinfo("Info", "Guides toggled")
    
    def new_presentation(self):
        """Create a new presentation"""
        self.draw_sample_slide()
        self.status_label.config(text="New presentation created")
    
    def open_file(self):
        """Open a presentation file"""
        file_path = filedialog.askopenfilename(filetypes=[("Presentation Files", "*.pptx"), ("All Files", "*.*")])
        if file_path:
            self.status_label.config(text=f"Opened: {file_path}")
    
    def save_file(self):
        """Save the current presentation"""
        messagebox.showinfo("Info", "Presentation saved")
    
    def save_file_as(self):
        """Save the current presentation with a new name"""
        file_path = filedialog.asksaveasfilename(defaultextension=".pptx", 
                                               filetypes=[("Presentation Files", "*.pptx")])
        if file_path:
            self.status_label.config(text=f"Saved as: {file_path}")

if __name__ == "__main__":
    app = PowerPointLikeApp()
    app.mainloop()