#from tkinter import messagebox

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox


#from services import history_service
import services.history_service as history_service
from PySide6.QtWidgets import QHeaderView
from PySide6.QtGui import QColor




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
        
        self.total_label = QLabel("Total Trades: 0")
        self.buy_label = QLabel("🟢  Buy : 0")
        self.sell_label = QLabel("🔴  Sell : 0")
        self.hold_label = QLabel("🟡  Hold : 0")

        stats_layout = QHBoxLayout()

      

        stats_layout.addWidget(self.total_label)
        stats_layout.addStretch()
        stats_layout.addWidget(self.buy_label)
        stats_layout.addWidget(self.sell_label)
        stats_layout.addWidget(self.hold_label)

        layout.addLayout(stats_layout)

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
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    

        layout.addWidget(self.table)
        button_layout = QHBoxLayout()

        delete_button = QPushButton("🗑 Delete Selected")
        delete_button.clicked.connect(self.delete_selected_signal)

        clear_button = QPushButton("🧹 Clear All")
        clear_button.clicked.connect(self.clear_all_signals)

        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

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
        #print(signals)


        #signals = history_service.get_user_signals(
         # self.user["id"]
        #)

        self.table.setRowCount(len(signals))

        for row, signal in enumerate(signals):
            date_item = QTableWidgetItem(signal["created_at"])
            date_item.setData(
            Qt.UserRole, 
            signal["id"])

        
            self.table.setItem(
                row, 
                0,
                date_item
            )
            
            #self.table.item(row, 0).setData
                      #  Qt.UserRole, signal["id"]
            #)
            
             # Store the signal ID in the first column's UserRole data

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

           # self.table.setItem(
           # row,
            #3,
            #QTableWidgetItem(signal["signal"])
            #)
            signal_item = QTableWidgetItem(signal["signal"])
            if signal["signal"] == "🟢 BUY":
                signal_item.setForeground(QColor("green"))
            elif signal["signal"] == "🔴 SELL":
                signal_item.setForeground(QColor("red"))
            elif signal["signal"] == "🟡 HOLD":
                signal_item.setForeground(QColor("orange"))

            self.table.setItem(
            row,
            3,
            signal_item
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
        self.update_statistics()

    def delete_selected_signal(self):

        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
            self,
            "No Selection",
            "Please select a signal to delete."
            )
            return

        signal_id_item = self.table.item(selected_row, 0)

        signal_id = signal_id_item.data(Qt.UserRole)

        reply = QMessageBox.question(
        self,
        "Delete Signal",
        "This action cannot be undone. \n\n Delete this signal?",
        QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            history_service.delete_signal(signal_id)
            self.load_history()
            self.update_statistics()
    def clear_all_signals(self):
        reply = QMessageBox.question(
            self,
            "Clear History",
            "This action cannot be undone.\n\nAre you sure you want to delete all signals?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            signals = history_service.get_user_signals(self.user["id"])

        for signal in signals:
            history_service.delete_signal(signal["id"])

            self.load_history()
            self.update_statistics()

        QMessageBox.information(
            self,
            "History Cleared",
            "All trading history has been deleted."
        )
    def update_statistics(self):
        signals = history_service.get_user_signals(self.user["id"])
        total_trades = len(signals)
        buy_trades = sum(1 for s in signals if s["signal"] == "🟢 BUY")
        sell_trades = sum(1 for s in signals if s["signal"] == "🔴 SELL")
        hold_trades = sum(1 for s in signals if s["signal"] == "🟡 HOLD")

        self.total_label.setText(f"Total Trades: {total_trades}")
        self.buy_label.setText(f"🟢  Buy : {buy_trades}")
        self.sell_label.setText(f"🔴  Sell : {sell_trades}")
        self.hold_label.setText(f"🟡  Hold : {hold_trades}")