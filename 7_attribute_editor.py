import tkinter as tk
from tkinter import ttk

class AttributeEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Attribute Editor")
        self.geometry("400x600")

        # Tabbed Attribute Editor
        tabs = ttk.Notebook(self)
        tabs.pack(expand=True, fill="both")

        # Node Attributes Tab
        node_tab = tk.Text(tabs)
        node_tab.insert("1.0", "Transform Node Attributes...")
        node_tab.pack(expand=True, fill="both")
        tabs.add(node_tab, text="pCube1")

        # Material Tab
        material_tab = tk.Text(tabs)
        material_tab.insert("1.0", "Lambert1 Shader Attributes...")
        material_tab.pack(expand=True, fill="both")
        tabs.add(material_tab, text="lambert1")

if __name__ == "__main__":
    app = AttributeEditorWindow()
    app.mainloop()
