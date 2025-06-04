import tkinter as tk

class GraphEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Graph Editor")
        self.geometry("800x400")

        self.canvas = tk.Canvas(self, bg="white", width=800, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Draw axes
        self.canvas.create_line(0, 200, 800, 200, fill="gray")  # X-axis
        self.canvas.create_line(0, 0, 0, 400, fill="gray")      # Y-axis

        # Draw sample keyframe curve (line)
        self.canvas.create_line(100, 150, 300, 50, fill="red", width=2)

if __name__ == "__main__":
    app = GraphEditorWindow()
    app.mainloop()
