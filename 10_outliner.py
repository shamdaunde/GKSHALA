import tkinter as tk
from tkinter import ttk

class OutlinerWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Outliner")
        self.geometry("300x600")

        # Treeview for Hierarchy
        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text="Scene Objects")

        # Add Sample Items
        root = self.tree.insert("", "end", text="World", open=True)
        cube = self.tree.insert(root, "end", text="pCube1")
        light = self.tree.insert(root, "end", text="light1")

        self.tree.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = OutlinerWindow()
    app.mainloop()
