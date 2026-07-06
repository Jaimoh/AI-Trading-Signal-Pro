import services.database_service as database_service
import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow


def main():
    database_service.initialize_database()
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()