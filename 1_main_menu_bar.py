import tkinter as tk
from tkinter import Menu

class MainMenuBarWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Main Menu Bar")
        self.geometry("800x600")

        # Create menu bar
        menubar = Menu(self)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Scene")
        file_menu.add_command(label="Open...")
        menubar.add_cascade(label="File", menu=file_menu)

        # Workspace Menu
        workspace_menu = Menu(menubar, tearoff=0)
        workspace_menu.add_command(label="Modeling")
        workspace_menu.add_command(label="Animation")
        menubar.add_cascade(label="Workspace", menu=workspace_menu)

        # Contextual/Polygon Menu
        polygons_menu = Menu(menubar, tearoff=0)
        polygons_menu.add_command(label="Create Cube")
        menubar.add_cascade(label="Polygons", menu=polygons_menu)

        # Attach menu bar to window
        self.config(menu=menubar)

if __name__ == "__main__":
    app = MainMenuBarWindow()
    app.mainloop()
