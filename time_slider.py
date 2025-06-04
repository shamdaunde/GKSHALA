import tkinter as tk

class TimeSlider(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Horizontal Slider (Scale)
        self.slider = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        self.slider.pack(fill=tk.X, expand=True)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GKSHALA - Time Slider")
    root.geometry("800x100")

    time_slider = TimeSlider(root)
    time_slider.pack(fill=tk.X, padx=10, pady=10)

    root.mainloop()
