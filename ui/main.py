import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from Class.kniha import Kniha

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kniznica")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
