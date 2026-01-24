from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QMenuBar, \
    QMenu, QToolBar, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caja registradora")
        self.showFullScreen() # para que ocupe toda la pantalla

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.texto = QLabel("Hola mundo")
        layout.addWidget(self.texto)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()