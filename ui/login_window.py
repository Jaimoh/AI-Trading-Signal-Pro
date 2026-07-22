
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow
from PySide6.QtWidgets import QMessageBox
import services.auth_service as auth_service
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit
)

from PySide6.QtCore import Qt


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Trading Signal Analyzer Pro")

        self.resize(400, 300)

        layout = QVBoxLayout()

        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")

        self.register_button = QPushButton("Register")

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.open_register)

        self.setLayout(layout)
    #def handle_login(self):

        username = self.username.text()
        password = self.password.text()

    def handle_login(self):

     username = self.username.text()
     password = self.password.text()

     user = auth_service.login(username, password)

     if user:

        self.main_window = MainWindow(user)
        self.main_window.show()

        self.close()

     else:

        QMessageBox.warning(
            self,
            "Login Failed",
            "Invalid username or password."
        )
    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()  
         