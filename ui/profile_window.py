from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)

from PySide6.QtCore import Qt

from services import database_service


class ProfileWindow(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("My Profile")
        self.resize(450, 400)

        layout = QVBoxLayout()

        title = QLabel("My Profile")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:white;
        """)

        layout.addWidget(title)

        self.first_name = QLineEdit(user["first_name"])
        self.last_name = QLineEdit(user["last_name"])
        self.username = QLineEdit(user["username"])
        self.email = QLineEdit(user["email"])

        layout.addWidget(self.first_name)
        layout.addWidget(self.last_name)
        layout.addWidget(self.username)
        layout.addWidget(self.email)

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)

        layout.addWidget(self.save_button)

        self.setStyleSheet("""
            QWidget{
                background:#1E1E1E;
                color:white;
            }

            QLineEdit{
                background:#2D2D30;
                color:white;
                border:2px solid #3E3E42;
                border-radius:8px;
                padding:8px;
            }

            QPushButton{
                background:#007ACC;
                color:white;
                padding:10px;
                border-radius:8px;
            }
        """)

        self.setLayout(layout)
    def save_changes(self):
        print("Save button clicked")

        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        username = self.username.text().strip()
        email = self.email.text().strip() 

        if not first_name or not last_name or not username or not email:

            QMessageBox.warning(
            self,
            "Missing Information",
            "Please complete all fields."
           )
            return    
        if database_service.username_exists_except(
            username,
            self.user["id"]
        ):
            QMessageBox.warning(
                self,
                "Username Already Exists",
                "Please choose a different username."
            )
            return
        if database_service.email_exists_except(
            email,
            self.user["id"]
        ):
            QMessageBox.warning(
                self,
                "Email Already Exists",
                "Please choose a different email."
            )
            return
        database_service.update_user(
            self.user["id"],
            first_name,
            last_name,
            username,
            email
        )
        QMessageBox.information(
            self,
            "Changes Saved",
            "Your profile has been updated successfully."
        )
        self.user = database_service.get_user(username)
        self.close()

        