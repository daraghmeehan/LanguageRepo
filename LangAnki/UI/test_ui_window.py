import sys
import PyQt5
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

# below two to make scaling right on my laptop
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class LangAnki_UI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi("LangAnki v1.ui", self)



if __name__ == "__main__":
    app = QApplication([])
    window = LangAnki_UI()
    window.show()
    sys.exit(app.exec_())