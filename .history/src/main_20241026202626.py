import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from src.components.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
