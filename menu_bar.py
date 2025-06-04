import tkinter as tk
from tkinter import Menu

class MenuBar(Menu):
    def __init__(self, parent):
        super().__init__(parent)

        # File Menu
        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="New Scene")
        file_menu.add_command(label="Open...")
        file_menu.add_separator()
        file_menu.add_command(label="Save")
        self.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = Menu(self, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_command(label="Redo")
        self.add_cascade(label="Edit", menu=edit_menu)

        # Attach the menu bar to the parent window
        parent.config(menu=self)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GKSHALA - MenuBar with Tkinter")
    root.geometry("800x600")

    menu_bar = MenuBar(root)

    root.mainloop()
