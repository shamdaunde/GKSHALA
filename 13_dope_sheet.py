from PySide2.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QApplication
import sys

class DopeSheetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GKSHALA - Dope Sheet")
        self.resize(800, 400)
        
        # Keyframe Timeline Table
        table = QTableWidget(5, 50)  # Rows: Tracks, Columns: Frames
        table.setHorizontalHeaderLabels([str(i) for i in range(1, 51)])
        table.setVerticalHeaderLabels(["pCube1", "light1", "Camera", "Control"])
        
        # Add Sample Keyframes
        table.setItem(0, 10, QTableWidgetItem("🔑"))  # Keyframe at frame 11
        
        self.setCentralWidget(table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DopeSheetWindow()
    window.show()
    sys.exit(app.exec_())