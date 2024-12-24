import sys
from PyQt6.QtWidgets import QApplication
from controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    sys.exit(app.exec())