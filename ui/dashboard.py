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
import mplfinance as mpf

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
        self.refresh_timer.start(6000)  # Refresh every minute

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
         
    
         market = get_market_data()

         open_price = market["open"]
         high_price = market["high"]
         low_price = market["low"]
         close_price = market["close"]
         rsi = market["rsi"]
         ema = market["ema"]
         signal = market["signal"]

         self.candle_history.append({
             "open": open_price,
             "high": high_price,
             "low": low_price,
             "close": close_price
         })

         if len(self.candle_history) > 40:
             self.candle_history.pop(0)




         self.price_label.setText(f"{close_price:.5f}")
         self.rsi_label.setText(str(rsi))
         self.ema_label.setText(str(ema))
         self.signal_label.setText(signal)
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
         self.connection_label.setText("🟢 Connected")
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
        self.figure.clear()
       # Clear the previous chart
        self.chart = self.figure.add_subplot(111)
        self.chart.set_facecolor("#1E1E1E")  

        df = pd.DataFrame(self.candle_history)  
        print(df.describe())
        if df.empty:
            return

        df["EMA10"] = df["close"].ewm(span=10, adjust=False).mean()


        df.index = pd.date_range(
            end=datetime.now(),
            periods=len(df),
            freq="min"  # Assuming each candle represents 1 minute
        )
        mc = mpf.make_marketcolors(
            up="lime",
            down="red",
            edge="inherit",
            wick="inherit",
            volume="inherit"
        )
        self.style = mpf.make_mpf_style(
            base_mpf_style="charles",
            marketcolors=mc,
            gridstyle="--",
            facecolor="#1E1E1E",
            edgecolor="#3E3E42",
            figcolor="#1E1E1E",
            gridcolor="#3E3E42",
            y_on_right=True
        )

        mpf.plot(
            df,
            type="candle",
            ax=self.chart,
            style= self.style,
            volume=False,
            show_nontrading=False,
            update_width_config=dict(
                candle_linewidth=1.0,
                candle_width=0.6, 
                volume_linewidth=1.0
                )
        )


        self.chart.plot(
            df.index, 
            df["EMA10"], 
            color="orange", 
            label="EMA 10", 
            linewidth=1.8
            )

        self.chart.legend(loc="upper left", 
                          fontsize=8, 
                          facecolor="#1E1E1E", 
                          edgecolor="white", 
                          labelcolor="white"
                          )

        self.chart.tick_params(
            
            axis='x',
            colors='white',
            labelsize=10    
        )
        self.chart.spines['bottom'].set_color('white')
        self.chart.spines['left'].set_color('white')
        self.chart.spines['top'].set_color('white')
        self.chart.spines['right'].set_color('white')

        self.chart.xaxis.label.set_color('white')
        self.chart.yaxis.label.set_color('white')

        self.chart.margins(x=0.01,)  # Adjust margins to prevent clipping of tick labels

        self.chart.yaxis.set_major_locator(MaxNLocator(nbins=8))  # Limit to 6 ticks on the y-axis

        for label in self.chart.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment('right')
            label.set_color("white")

        self.figure.subplots_adjust(
                left=0.1,
                right=0.95,
                top=0.9, 
                bottom=0.2   
            )  # Adjust layout to prevent clipping of tick labels

        self.canvas.draw_idle()


        