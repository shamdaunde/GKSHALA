import tkinter as tk

class ChannelBox(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bd=2, relief=tk.GROOVE)
        
        # Title Label
        title = tk.Label(self, text="Channel Box", bg="lightgray", font=("Arial", 12, "bold"))
        title.pack(fill=tk.X)

        # Listbox
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Add channel attributes
        attributes = ["Translate X", "Rotate Y", "Scale Z"]
        for attr in attributes:
            self.listbox.insert(tk.END, attr)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("GKSHALA - Channel Box")
    root.geometry("800x600")

    channel_box = ChannelBox(root)
    channel_box.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()
