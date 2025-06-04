import tkinter as tk

class ScriptEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GKSHALA - Script Editor")
        self.geometry("600x400")

        # Vertical PanedWindow (Splitter)
        splitter = tk.PanedWindow(self, orient=tk.VERTICAL)
        splitter.pack(expand=True, fill="both")

        # History Pane
        self.history_pane = tk.Text(splitter)
        self.history_pane.insert("1.0", "MEL Command History...")
        splitter.add(self.history_pane)

        # Input Pane
        self.input_pane = tk.Text(splitter)
        self.input_pane.insert("1.0", "Enter MEL or Python here...")
        splitter.add(self.input_pane)

if __name__ == "__main__":
    app = ScriptEditorWindow()
    app.mainloop()
