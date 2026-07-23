from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QStatusBar,
)
from ui.dashboard import Dashboard
from ui.profile_window import ProfileWindow
from PySide6.QtCore import Qt
from ui.history_window import HistoryWindow



class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()

        self.user = user

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

        layout.addWidget(title)

        self.welcome_label = QLabel(
            f"Welcome, {self.user['first_name']}!"
    )
        layout.addWidget(self.welcome_label)
        self.welcome_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: maroon;
            padding: 10px;
            """)

        self.dashboard = Dashboard(self.user)
       
       
        layout.addWidget(self.dashboard)

        self.dashboard.open_profile_requested.connect(self.show_profile)
        self.dashboard.history_requested.connect(self.show_history)
        #self.profile_window.user_updated.connect(self.update_user)

      
        
      
        #self.profile_window = ProfileWindow(self.user)
        #self.profile_window.show()  # Hide the profile window initially

        central_widget.setLayout(layout)

        # Status bar
        status = QStatusBar()
        status.showMessage("Ready")
        self.setStatusBar(status)
    def update_user(self, updated_user):
       # print("✅ MainWindow received updated user")
        #print(updated_user)
        self.user = updated_user   
        
        self.welcome_label.setText(
            f"Welcome, {self.user['first_name']}!")
        
        self.dashboard.user = updated_user  # Update the user in the dashboard as well
    def show_profile(self):

        self.profile_window = ProfileWindow(self.user)

        self.profile_window.user_updated.connect(self.update_user)

        self.profile_window.show()

    def show_history(self):
        self.history_window = HistoryWindow(self.user)
        self.history_window.show()