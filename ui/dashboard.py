from services.market_data import get_market_data

from datetime import datetime
import time

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Heading
        heading = QLabel("Trading Dashboard")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:white;
            padding: 10px;
        """)

        main_layout.addWidget(heading)
        # =========================
# Toolbar
# =========================

        toolbar = QHBoxLayout()

        asset_label = QLabel("Asset:")

        asset_box = QComboBox()
        asset_box.addItems([
           "EUR/USD",
           "GBP/USD",
           "USD/JPY",
           "BTC/USD",
           "KES/USD",
        ])

        time_label = QLabel("Timeframe:")

        time_box = QComboBox()
        time_box.addItems([
               "1 Minute",
               "5 Minutes",
               "15 Minutes",
                "1 Hour",
        ])

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_dashboard)

        toolbar.addWidget(asset_label)
        toolbar.addWidget(asset_box)
        toolbar.addSpacing(20)
        toolbar.addWidget(time_label)
        toolbar.addWidget(time_box)
        toolbar.addStretch()
        toolbar.addWidget(refresh_button)

        main_layout.addLayout(toolbar)
        status_layout = QHBoxLayout()

        self.connection_label = QLabel("🟢 Connected")
        self.connection_label.setStyleSheet("""
color:lightgreen;
font-size:14px;
font-weight:bold;
""")

        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("""
        color:white;
        font-size:14px;
        """)

        status_layout.addWidget(self.connection_label)
        status_layout.addStretch()
        status_layout.addWidget(self.clock_label)

        main_layout.addLayout(status_layout)

        # Dashboard cards
        cards_layout = QHBoxLayout()

        price_card, self.price_label = self.create_card("Price", "1.17452")
        cards_layout.addWidget(price_card)

        rsi_card, self.rsi_label = self.create_card("RSI", "48.3")
        cards_layout.addWidget(rsi_card)

        ema_card, self.ema_label = self.create_card("EMA", "1.17431")
        cards_layout.addWidget(ema_card)

        signal_card, self.signal_label = self.create_card("Signal", "🟢 BUY")
        cards_layout.addWidget(signal_card)

        main_layout.addLayout(cards_layout)
        # =========================
# Chart Area
# =========================

        chart_frame = QFrame()

        chart_frame.setStyleSheet("""
         QFrame{
              background-color:#252526;
             border:2px solid #3E3E42;
             border-radius:12px;
        }
            """)

        chart_layout = QVBoxLayout()

        chart_title = QLabel("Live Price Chart")
        chart_title.setAlignment(Qt.AlignCenter)

        chart_title.setStyleSheet("""
        font-size:18px;
        font-weight:bold;
        color:white;
        padding:10px;
        """)

        chart_placeholder = QLabel("📈 Chart Coming Soon...")
        chart_placeholder.setAlignment(Qt.AlignCenter)

        chart_placeholder.setStyleSheet("""
        font-size:20px;
        color:gray;
        """)

        chart_layout.addWidget(chart_title)
        chart_layout.addStretch()
        chart_layout.addWidget(chart_placeholder)
        chart_layout.addStretch()

        chart_frame.setLayout(chart_layout)
        main_layout.addWidget(chart_frame)
        self.setStyleSheet("""
        background-color: #1E1E1E;
     """)
        self.timer = QTimer()

        self.timer.timeout.connect(self.update_clock)

        self.timer.start(1000)

        self.update_clock()

        self.setLayout(main_layout)

    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
        QFrame{
        background-color:#2D2D30;
        border:2px solid #3E3E42;
        border-radius:12px;
        }
        """)

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("""
        font-size:15px;
        font-weight:bold;
        color:#C8C8C8;
        """)

        value_label = QLabel(value)
        value_label.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        color:white;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label) 
  
        card.setLayout(layout)
        return card, value_label
    def refresh_dashboard(self):
         self.connection_label.setText("🟡 Updating...")
         
         price, rsi, ema, signal = get_market_data()
        

         self.price_label.setText(str(price))
         self.rsi_label.setText(str(rsi))
         self.ema_label.setText(str(ema))
         self.signal_label.setText(signal)
         self.connection_label.setText("🟢 Connected")
    def update_clock(self):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.clock_label.setText(f"🕒 {current_time}")