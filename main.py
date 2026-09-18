import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from backend import knihy


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kniznica")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    for kniha in knihy:
        print(kniha.ziskaj_data())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
