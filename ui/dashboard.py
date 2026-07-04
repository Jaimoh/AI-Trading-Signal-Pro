import random

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QPushButton,
)
from PySide6.QtCore import Qt

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
        self.setStyleSheet("""
background-color: #1E1E1E;
""")

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

     price = round(random.uniform(1.17000, 1.18000), 5)

     rsi = round(random.uniform(20, 80), 1)

     ema = round(random.uniform(1.17000, 1.18000), 5)

     signal = random.choice([
        "🟢 BUY",
        "🔴 SELL",
        "🟡 HOLD"
     ])

     self.price_label.setText(str(price))
     self.rsi_label.setText(str(rsi))
     self.ema_label.setText(str(ema))
     self.signal_label.setText(signal)