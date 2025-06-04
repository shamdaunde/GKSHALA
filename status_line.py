import tkinter as tk

class StatusLine(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bd=1, relief=tk.RAISED, padx=5, pady=2)
        
        # Buttons
        new_file_btn = tk.Button(self, text="New File")
        new_file_btn.pack(side=tk.LEFT, padx=2)

        open_btn = tk.Button(self, text="Open")
        open_btn.pack(side=tk.LEFT, padx=2)

        # Separator (just space or visual line)
        separator = tk.Label(self, text="|", fg="gray")
        separator.pack(side=tk.LEFT, padx=5)

        grid_snap_btn = tk.Button(self, text="Grid Snap")
        grid_snap_btn.pack(side=tk.LEFT, padx=2)

        vertex_snap_btn = tk.Button(self, text="Vertex Snap")
        vertex_snap_btn.pack(side=tk.LEFT, padx=2)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GKSHALA - Status Line with Tkinter")
    root.geometry("800x600")

    # Add StatusLine toolbar at the top
    toolbar = StatusLine(root)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    root.mainloop()
