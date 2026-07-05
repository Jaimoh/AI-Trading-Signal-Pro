from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QStatusBar,
)
from ui.dashboard import Dashboard
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window title
        self.setWindowTitle("AI Trading Signal Analyzer Pro")

        # Window size
        self.resize(1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Main title
        title = QLabel("AI Trading Signal Analyzer Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            padding: 20px;
        """)

        layout.addWidget(Dashboard())

        central_widget.setLayout(layout)

        # Status bar
        status = QStatusBar()
        status.showMessage("Ready")