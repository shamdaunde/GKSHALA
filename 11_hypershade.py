import tkinter as tk

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class HypershadeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Hypershade")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(expand=True, fill="both")

        # Add sample nodes (rectangles)
        rect1 = self.canvas.create_rectangle(50, 50, 150, 100, fill="lightblue")
        rect2 = self.canvas.create_rectangle(200, 150, 300, 200, fill="lightgreen")

        # Create invisible widgets for tooltips over canvas rectangles
        self._add_tooltip_to_rect(rect1, "lambert1")
        self._add_tooltip_to_rect(rect2, "file1")

    def _add_tooltip_to_rect(self, rect_id, text):
        # Create a transparent widget on top of the rectangle area to show tooltip
        x1, y1, x2, y2 = self.canvas.coords(rect_id)
        width = int(x2 - x1)
        height = int(y2 - y1)
        # Use a Frame placed over canvas
        frame = tk.Frame(self.canvas, width=width, height=height)
        frame.place(x=x1, y=y1)
        ToolTip(frame, text)

if __name__ == "__main__":
    app = HypershadeWindow()
    app.mainloop()
