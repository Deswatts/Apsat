import sys

from apsat_gui.gui import MainWindow, QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())