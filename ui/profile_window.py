import email
from multiprocessing.dummy import connection
import sqlite3


from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)

from PySide6.QtCore import Qt, Signal


from services import database_service


class ProfileWindow(QWidget):
    user_updated = Signal(dict)  # Signal to notify when the user is updated

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

        #layout.addWidget(self.save_button)
        layout.addWidget(
            self.save_button,
            alignment=Qt.AlignCenter

        )

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
                min-width:180px;
                max-width:180px;
                min-height:38px;
                max-height:38px;
                border:none;
                border-radius:10px;
                font-size:14px;
                font-weight:bold;
             

                
            }
            QPushButton:hover{
                background:#1A8CFF;
            }
            QPushButton:pressed{
                background:#005A9E;
            }
        """)
        self.save_button.setFixedHeight(38)
        self.save_button.setFixedWidth(180)

        self.setLayout(layout)
    def save_changes(self):
        new_first_name = self.first_name.text().strip()
        new_last_name = self.last_name.text().strip()
        new_username = self.username.text().strip()
        new_email = self.email.text().strip()

        if not new_first_name or not new_last_name or not new_username or not new_email:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if database_service.username_exists_except(new_username, self.user["id"]):
            QMessageBox.warning(self, "Input Error", "Username already exists.")
            return

        if database_service.email_exists_except(new_email, self.user["id"]):
            QMessageBox.warning(self, "Input Error", "Email already exists.")
            return

        database_service.update_user(
            self.user["id"],
            new_first_name,
            new_last_name,
            new_username,
            new_email
        )

        updated_user = database_service.get_user_by_id(self.user["id"])
        self.user_updated.emit(updated_user)

        QMessageBox.information(self, "Success", "Profile updated successfully.")

    #def get_user(username):

       # connection = sqlite3.connect(database_service.DB_PATH)
        #connection.row_factory = sqlite3.Row
       # cursor = connection.cursor()

       # cursor.execute(
        #"""
        #SELECT *
        #FROM users
        #WHERE username = ?
       # """,
       # (username,)
    #)

       # user = cursor.fetchone()

       # connection.close()

       # if user is None:
       #     return None

      #  return dict(user)
