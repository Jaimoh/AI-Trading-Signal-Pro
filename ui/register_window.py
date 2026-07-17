import hashlib
from PySide6.QtWidgets import QMessageBox
import services.database_service as database_service

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)

from PySide6.QtCore import Qt
class RegisterWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register")
        self.resize(450, 600)
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        title = QLabel("Create New Account")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:white;
            padding:10px;
        """)

        layout.addWidget(title)
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First Name")

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last Name")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
                
        layout.addWidget(self.first_name)
        layout.addWidget(self.last_name)
        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm_password)

        self.register_button = QPushButton("Register")

        self.login_button = QPushButton(
            "Already have an account? Login"
        )

        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)
        self.register_button.clicked.connect(self.handle_register)
        self.login_button.clicked.connect(self.back_to_login)

               
        self.setStyleSheet("""
            QWidget{
                background-color:#1E1E1E;
                color:white;
            }

            QLineEdit{
                background-color:#2D2D30;
                border:2px solid #3E3E42;
                border-radius:8px;
                padding:8px;
                color:white;
            }

            QPushButton{
                background-color:#007ACC;
                color:white;
                border-radius:8px;
                padding:10px;
                font-weight:bold;
            }

            QPushButton:hover{
                background-color:#0099FF;
            }
        """)
        self.setLayout(layout)
    def handle_register(self):

        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if not first_name or not last_name or not username \
        or not email or not password or not confirm_password:

         QMessageBox.warning(
            self,
            "Missing Information",
            "Please complete all fields."
         )
         return
        
        if password !=confirm_password:
       
            QMessageBox.warning(
          self,
          "Password Error",
          "Password do not match"
        
       )
            return
      
        if database_service.username_exists(username):

            QMessageBox.warning(
                self,
                "Username Exists",
                "Choose another username."
       
        )
            return
        if database_service.email_exists(email):

             QMessageBox.warning(
             self,
             "Email Exists",
             "This email is already registered."
        
        )
             return
        
        password_hash = hashlib.sha256(
            password.encode()
        ).hexdigest()

        success = database_service.create_user(
            first_name,
            last_name,
            username,
            email,
            password_hash
        )
        if success:

            QMessageBox.information(
                self,
                "Success",
                "Account created successfully."
                
        )
            self.back_to_login()

        else:

            QMessageBox.critical(
                self,
                "Database Error",
                "Unable to create account."
    )
    
    
    def back_to_login(self):
        from ui.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()   
