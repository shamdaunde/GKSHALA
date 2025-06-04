import tkinter as tk

class Viewport(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=800, height=600, bg="black")
        self.pack(expand=True, fill=tk.BOTH)
        self.draw_placeholder()

    def draw_placeholder(self):
        # This simulates a "3D View" placeholder
        self.create_text(400, 300, text="3D Viewport Placeholder", fill="white", font=("Arial", 16))

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GKSHALA - Viewport Simulation")
    root.geometry("800x600")

    viewport = Viewport(root)

    root.mainloop()
