#from socket import close

from matplotlib import style
from matplotlib.ticker import MaxNLocator

from services.market_data import get_market_data
from ui.profile_window import ProfileWindow
from services import history_service

from datetime import datetime
import time
#import pyqtgraph as pg
#from pyqtgraph import PlotWidget
import pandas as pd
from matplotlib.patches import Rectangle
import numpy as np
from services.ai_engine import generate_signal






from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
 



from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QPushButton,
    QMessageBox,
    QCheckBox,

)
from PySide6.QtCore import Qt, QTimer, Signal

class Dashboard(QWidget):
    open_profile_requested = Signal()  # Signal to request opening the profile window
    history_requested = Signal()  # Signal to request opening the history window
    def __init__(self,user):
        super().__init__()

        self.user = user
        self.price_history = []
        self.candle_history = []



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

        #asset_box = QComboBox()
        self.asset_box = QComboBox()  # Store the asset_box as an instance variable
        self.asset_box.addItems([
           "EUR/USD",
           "GBP/USD",
           "USD/JPY",
           "BTC/USD",
           "KES/USD",
        ])

        time_label = QLabel("Timeframe:")

        self.time_box = QComboBox()  # Store the time_box as an instance variable
        self.time_box.addItems([
               "1 Minute",
               "5 Minutes",
               "15 Minutes",
                "1 Hour",
        ])

        profile_button = QPushButton("My Profile")
        profile_button.clicked.connect(self.open_profile_requested.emit)

        history_button = QPushButton("History")
        history_button.clicked.connect(self.history_requested.emit)


        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_dashboard)

        self.auto_refresh_checkbox = QCheckBox("Auto Refresh")
        self.auto_refresh_checkbox.setChecked(True) 
        self.auto_refresh_checkbox.stateChanged.connect(self.toggle_auto_refresh)

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout)


        toolbar.addWidget(asset_label)
        toolbar.addWidget(self.asset_box)
        toolbar.addSpacing(20)
        toolbar.addWidget(time_label)
        toolbar.addWidget(self.time_box)
        toolbar.addStretch()
        toolbar.addWidget(profile_button)
        toolbar.addWidget(history_button)
        toolbar.addWidget(refresh_button)
        toolbar.addWidget(self.auto_refresh_checkbox)
        toolbar.addWidget(logout_button)

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

       
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor="#252526")  # Set the background color of the figure # Set the background color of the figure
        self.figure.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1)# Adjust the subplot parameters for better spacing)  
        self.canvas = FigureCanvas(self.figure)
        self.chart = self.figure.add_subplot(111)
        self.chart.set_facecolor("#252526")
        self.chart.set_title(
            "Live Price Chart",
              color="white", 
              fontsize="12")

        self.chart.set_xlabel("Time")
        self.chart.set_ylabel("Price")

        self.chart.grid(True)

        self.chart.grid(
        True, 
        linestyle='--',
        linewidth=0.5,
        alpha=0.3)

        

        

        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.canvas)
       

        chart_frame.setLayout(chart_layout)
        main_layout.addWidget(chart_frame)
        self.setStyleSheet("""
        background-color: #1E1E1E;
     """)
        self.timer = QTimer()

        self.timer.timeout.connect(self.update_clock)

        self.timer.start(1000)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_dashboard)
        self.refresh_timer.start(5000)  # Refresh every minute

        self.update_clock()
        QTimer.singleShot(200, self.refresh_dashboard)  # Initial refresh when the dashboard is created

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

        # --------------------------------
        # Get market data
        # --------------------------------
        market = get_market_data()

        open_price = market["open"]
        high_price = market["high"]
        low_price = market["low"]
        close_price = market["close"]

        # --------------------------------
        # Add new candle
        # --------------------------------
        self.candle_history.append({
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price
        })

        # Keep maximum of 100 candles
        if len(self.candle_history) > 100:
            self.candle_history.pop(0)

        # --------------------------------
        # Create price series
        # --------------------------------
        prices = pd.Series(
            [candle["close"] for candle in self.candle_history],
            dtype="float64"
        )

        # --------------------------------
        # Calculate EMA 10
        # --------------------------------
        ema_series = prices.ewm(
            span=10,
            adjust=False
        ).mean()

        ema = float(ema_series.iloc[-1])

        # --------------------------------
        # Calculate Bollinger Bands 20
        # --------------------------------
        sma20 = prices.rolling(window=20).mean()
        std20 = prices.rolling(window=20).std()

        if len(prices) >= 20:
            upper_band = float(
                sma20.iloc[-1] + (2 * std20.iloc[-1])
            )

            lower_band = float(
                sma20.iloc[-1] - (2 * std20.iloc[-1])
            )
        else:
            upper_band = None
            lower_band = None

        # --------------------------------
        # Calculate RSI 14
        # --------------------------------
        if len(prices) >= 15:

            delta = prices.diff()

            gains = delta.clip(lower=0)
            losses = -delta.clip(upper=0)

            avg_gain = gains.rolling(window=14).mean()
            avg_loss = losses.rolling(window=14).mean()

            if avg_loss.iloc[-1] == 0:
                rsi = 100.0
            else:
                rs = avg_gain.iloc[-1] / avg_loss.iloc[-1]
                rsi = 100 - (100 / (1 + rs))

            if pd.isna(rsi):
                rsi = 50.0

        else:
            # Not enough candles yet
            rsi = 50.0

        rsi = round(float(rsi), 1)

        print(f"Price: {close_price:.5f}")
        print(f"EMA: {ema:.5f}")
        print(f"RSI: {rsi:.1f}")

        if upper_band is not None:
            print(f"Upper Band: {upper_band:.5f}")
            print(f"Lower Band: {lower_band:.5f}")
        else:
            print("Bollinger Bands: waiting for 20 candles")

        print("----------------")

        # --------------------------------
        # Generate trading signal
        # --------------------------------
        signal, confidence = generate_signal(
            close_price,
            ema,
            rsi,
            upper_band,
            lower_band
        )

        # --------------------------------
        # Update dashboard cards
        # --------------------------------
        self.price_label.setText(
            f"{close_price:.5f}"
        )

        self.rsi_label.setText(
            f"{rsi:.1f}"
        )

        self.ema_label.setText(
            f"{ema:.5f}"
        )

        self.signal_label.setText(
            f"{signal} ({confidence}%)"
        )

        # --------------------------------
        # Signal color
        # --------------------------------
        if "BUY" in signal:

            self.signal_label.setStyleSheet("""
                font-size:24px;
                font-weight:bold;
                color:#00FF66;
            """)

        elif "SELL" in signal:

            self.signal_label.setStyleSheet("""
                font-size:24px;
                font-weight:bold;
                color:#FF4444;
            """)

        else:

            self.signal_label.setStyleSheet("""
                font-size:24px;
                font-weight:bold;
                color:#FFD700;
            """)

        # --------------------------------
        # Save signal to database
        # --------------------------------
        asset = self.asset_box.currentText()
        timeframe = self.time_box.currentText()

        history_service.save_signal(
            self.user["id"],
            asset,
            timeframe,
            signal,
            close_price,
            rsi,
            ema
        )

        # --------------------------------
        # Update connection status
        # --------------------------------
        self.connection_label.setText(
            "🟢 Connected"
        )

        # --------------------------------
        # Update chart
        # --------------------------------
        self.update_chart()

    def update_clock(self):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.clock_label.setText(f"🕒 {current_time}")
    def logout(self):

        reply = QMessageBox.question(
        self,
        "Logout",
        "Are you sure you want to log out?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

        if reply == QMessageBox.Yes:

            from ui.login_window import LoginWindow

            self.login_window = LoginWindow()
            self.login_window.show()

            self.window().close()
  
    def toggle_auto_refresh(self, state):
        if self.auto_refresh_checkbox.isChecked():
            self.refresh_timer.start(5000)
            self.connection_label.setText("🟢 Auto Refresh ON")
              # Refresh every minute
        else:
            self.refresh_timer.stop()
            self.connection_label.setText("🔴 Auto Refresh OFF")

    def update_chart(self):

        # --------------------------------
        # Clear previous chart
        # --------------------------------
        self.figure.clear()

        self.chart = self.figure.add_subplot(111)
        self.chart.set_facecolor("#1E1E1E")

        # --------------------------------
        # Need at least 2 candles
        # --------------------------------
        if len(self.candle_history) < 2:
            return

        # --------------------------------
        # Create DataFrame
        # --------------------------------
        df = pd.DataFrame(self.candle_history)

        if df.empty:
            return

        # --------------------------------
        # EMA 10
        # MUST match refresh_dashboard()
        # --------------------------------
        df["EMA10"] = df["close"].ewm(
            span=10,
            adjust=False
        ).mean()

        # --------------------------------
        # Bollinger Bands
        # --------------------------------
        df["SMA20"] = df["close"].rolling(
            window=20
        ).mean()

        df["STD20"] = df["close"].rolling(
            window=20
        ).std()

        df["UpperBand"] = (
            df["SMA20"] + (2 * df["STD20"])
        )

        df["LowerBand"] = (
            df["SMA20"] - (2 * df["STD20"])
        )

        # --------------------------------
        # Time index
        # --------------------------------
        df.index = pd.date_range(
            end=datetime.now(),
            periods=len(df),
            freq="min"
        )

        # --------------------------------
        # X positions
        # --------------------------------
        x = list(range(len(df)))

        # --------------------------------
        # Draw candlesticks
        # --------------------------------
        candle_width = 0.35

        for i, (_, row) in enumerate(df.iterrows()):

            open_price = row["open"]
            high_price = row["high"]
            low_price = row["low"]
            close_price = row["close"]

            # Green candle = bullish
            # Red candle = bearish
            color = (
                "lime"
                if close_price >= open_price
                else "red"
            )

            # ----------------------------
            # Wick
            # ----------------------------
            self.chart.plot(
                [i, i],
                [low_price, high_price],
                color=color,
                linewidth=1
            )

            # ----------------------------
            # Candle body
            # ----------------------------
            body_bottom = min(
                open_price,
                close_price
            )

            body_height = abs(
                close_price - open_price
            )

            if body_height < 0.00001:
                body_height = 0.00001

            rect = Rectangle(
                (
                    i - candle_width / 2,
                    body_bottom
                ),
                candle_width,
                body_height,
                facecolor=color,
                edgecolor=color
            )

            self.chart.add_patch(rect)

        # --------------------------------
        # EMA 10
        # --------------------------------
        self.chart.plot(
            x,
            df["EMA10"],
            color="orange",
            linewidth=2.5,
            label="EMA 10"
        )

        # --------------------------------
        # Upper Bollinger Band
        # --------------------------------
        self.chart.plot(
            x,
            df["UpperBand"],
            color="deepskyblue",
            linewidth=1,
            linestyle="--",
            label="Upper Band"
        )

        # --------------------------------
        # Lower Bollinger Band
        # --------------------------------
        self.chart.plot(
            x,
            df["LowerBand"],
            color="deepskyblue",
            linewidth=1,
            linestyle="--",
            label="Lower Band"
        )

        # --------------------------------
        # Fill Bollinger Band area
        # --------------------------------
        self.chart.fill_between(
            x,
            df["UpperBand"].values,
            df["LowerBand"].values,
            color="deepskyblue",
            alpha=0.08
        )

        # --------------------------------
        # Y-axis padding
        # --------------------------------
        price_range = (
            df["high"].max()
            - df["low"].min()
        )

        if price_range == 0:
            price_range = 0.001

        padding = price_range * 0.15

        self.chart.set_ylim(
            df["low"].min() - padding,
            df["high"].max() + padding
        )

        # --------------------------------
        # X-axis
        # --------------------------------
        self.chart.set_xticks(x)

        self.chart.set_xticklabels(
            [
                t.strftime("%H:%M")
                for t in df.index
            ],
            rotation=45,
            color="white"
        )

        # --------------------------------
        # Y-axis
        # --------------------------------
        self.chart.tick_params(
            axis="y",
            colors="white"
        )

        self.chart.tick_params(
            axis="x",
            colors="white"
        )

        self.chart.set_ylabel(
            "Price",
            color="white"
        )

        # --------------------------------
        # Grid
        # --------------------------------
        self.chart.grid(
            True,
            linestyle="--",
            alpha=0.3,
            color="#404040"
        )

        # --------------------------------
        # Spines
        # --------------------------------
        self.chart.spines["top"].set_visible(False)
        self.chart.spines["right"].set_visible(False)

        self.chart.spines["left"].set_color("#555")
        self.chart.spines["bottom"].set_color("#555")

        # --------------------------------
        # Legend
        # --------------------------------
        self.chart.legend(
            loc="upper left",
            frameon=False,
            fontsize=9
        )

        # --------------------------------
        # Layout
        # --------------------------------
        self.figure.tight_layout()

        # --------------------------------
        # Refresh canvas
        # --------------------------------
        self.canvas.draw_idle()