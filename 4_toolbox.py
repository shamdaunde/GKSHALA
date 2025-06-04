import tkinter as tk

class ToolboxWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Toolbox")
        self.geometry("300x600")

        # Vertical Toolbox (left side)
        toolbox = tk.Frame(self, bd=2, relief=tk.RIDGE, bg="lightgray")
        toolbox.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Transform Tools
        move_btn = tk.Button(toolbox, text="Move Tool", width=20)
        move_btn.pack(pady=5)

        rotate_btn = tk.Button(toolbox, text="Rotate Tool", width=20)
        rotate_btn.pack(pady=5)

        # Viewport Layouts
        single_pane_btn = tk.Button(toolbox, text="Single Pane", width=20)
        single_pane_btn.pack(pady=5)

        four_view_btn = tk.Button(toolbox, text="Four View", width=20)
        four_view_btn.pack(pady=5)

# Run the application
if __name__ == "__main__":
    app = ToolboxWindow()
    app.mainloop()
