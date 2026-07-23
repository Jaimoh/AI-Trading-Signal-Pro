from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)

from PySide6.QtCore import Qt

from services import history_service


class HistoryWindow(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Trade History")
        self.resize(900, 500)

        layout = QVBoxLayout()

        title = QLabel("Trade History")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:white;
        """)

        layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Asset",
            "Timeframe",
            "Signal",
            "Price",
            "RSI",
            "EMA"
        ])

        layout.addWidget(self.table)

        self.setStyleSheet("""
            QWidget{
                background:#1E1E1E;
                color:white;
            }

            QTableWidget{
                background:#252526;
                color:white;
                gridline-color:#3E3E42;
            }

            QHeaderView::section{
                background:#007ACC;
                color:white;
                padding:6px;
                font-weight:bold;
            }
        """)

        self.setLayout(layout)

        self.load_history()
    def load_history(self):

        signals = history_service.get_user_signals(
          self.user["id"]
        )

        self.table.setRowCount(len(signals))

        for row, signal in enumerate(signals):

            self.table.setItem(
             row,
                0,
            QTableWidgetItem(signal["created_at"])
            )

            self.table.setItem(
            row,
            1,
            QTableWidgetItem(signal["asset"])
         )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(signal["timeframe"])
            )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem(signal["signal"])
            )

        self.table.setItem(
            row,
            4,
            QTableWidgetItem(str(signal["price"]))
        )

        self.table.setItem(
            row,
            5,
            QTableWidgetItem(str(signal["rsi"]))
        )

        self.table.setItem(
            row,
            6,
            QTableWidgetItem(str(signal["ema"]))
        )