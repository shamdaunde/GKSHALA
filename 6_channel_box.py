import tkinter as tk

class ChannelBoxWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Channel Box")
        self.geometry("600x600")  # Wider to allow right-side docking simulation

        # Main area (could be canvas or other central widgets)
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Channel Box (simulated dock on the right)
        dock_frame = tk.Frame(self, bd=2, relief=tk.RIDGE)
        dock_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        label = tk.Label(dock_frame, text="Channel Box", font=("Arial", 12, "bold"))
        label.pack(pady=5)

        channel_list = tk.Listbox(dock_frame)
        channel_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add keyable attributes
        for item in ["Translate X", "Rotate Y", "Scale Z", "Visibility"]:
            channel_list.insert(tk.END, item)

# Run the application
if __name__ == "__main__":
    app = ChannelBoxWindow()
    app.mainloop()
