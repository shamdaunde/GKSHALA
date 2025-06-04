import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import sys

class PowerPointApp:
    def __init__(self):
        # Initialize database
        self.setup_database()
        
        # Create login window
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        
        # Login widgets
        tk.Label(self.login_window, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()
        
        tk.Label(self.login_window, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()
        
        tk.Button(self.login_window, text="Login", command=self.validate_login).pack(pady=10)
        
        # Main application window (initially hidden)
        self.main_window = None
        self.login_window.mainloop()
    
    def setup_database(self):
        """Initialize SQLite database with sample user"""
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
        self.cursor.execute("INSERT INTO users VALUES ('admin', 'admin123')")
        self.conn.commit()
    
    def validate_login(self):
        """Check login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if self.cursor.fetchone():
            self.login_window.destroy()
            self.create_main_app()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def create_main_app(self):
        """Main application window with all components"""
        self.main_window = tk.Tk()
        self.main_window.title("PowerPoint-Like App")
        self.main_window.geometry("1200x800")
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 1. Ribbon Menu
        self.create_ribbon_menu()
        
        # 2. Toolbar
        self.create_toolbar()
        
        # 3. Workspace
        self.create_workspace()
        
        # 4. Status Bar
        self.create_statusbar()
        
        self.main_window.mainloop()
    
    def create_ribbon_menu(self):
        """Dynamic ribbon menu with tabs"""
        ribbon_frame = ttk.Frame(self.main_window)
        ribbon_frame.pack(fill=tk.X)
        
        notebook = ttk.Notebook(ribbon_frame)
        
        # Home Tab
        home_tab = ttk.Frame(notebook)
        ttk.Button(home_tab, text="Paste", width=10).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(home_tab, text="Cut", width=10).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(home_tab, text="Copy", width=10).grid(row=0, column=2, padx=2, pady=2)
        notebook.add(home_tab, text="Home")
        
        # Insert Tab
        insert_tab = ttk.Frame(notebook)
        ttk.Button(insert_tab, text="Table", width=10).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(insert_tab, text="Image", width=10).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(insert_tab, text="Shape", width=10).grid(row=0, column=2, padx=2, pady=2)
        notebook.add(insert_tab, text="Insert")
        
        notebook.pack(fill=tk.X)
    
    def create_toolbar(self):
        """Context-aware toolbar"""
        toolbar_frame = ttk.Frame(self.main_window, height=40)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Tool buttons
        tools = ["Save", "Undo", "Redo", "Font", "Size", "Bold", "Italic"]
        for i, tool in enumerate(tools):
            ttk.Button(toolbar_frame, text=tool).pack(side=tk.LEFT, padx=2)
    
    def create_workspace(self):
        """Main workspace with slide canvas"""
        workspace_frame = tk.Frame(self.main_window, bg="white")
        workspace_frame.pack(fill=tk.BOTH, expand=True)
        
        # Slide canvas
        canvas = tk.Canvas(workspace_frame, bg="white", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Sample slide
        canvas.create_rectangle(100, 50, 1100, 650, outline="lightgray", width=2)
        canvas.create_text(600, 100, text="Click to add title", font=("Arial", 24), fill="gray")
        canvas.create_text(600, 350, text="Click to add content", font=("Arial", 16), fill="lightgray")
        
        # 3D Viewport placeholder
        canvas.create_rectangle(150, 150, 1050, 600, outline="blue", dash=(5,5))
        canvas.create_text(600, 375, text="3D Viewport Area", fill="blue")
    
    def create_statusbar(self):
        """Status bar at bottom"""
        status_frame = ttk.Frame(self.main_window, height=24)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Label(status_frame, text="Ready").pack(side=tk.LEFT, padx=10)
        ttk.Label(status_frame, text="Slide 1 of 1").pack(side=tk.RIGHT, padx=10)
    
    def on_close(self):
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.conn.close()
            self.main_window.destroy()
            sys.exit()

if __name__ == "__main__":
    app = PowerPointApp()