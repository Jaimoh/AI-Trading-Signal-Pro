import sqlite3
from services.database_service import DB_PATH

def save_signal(
    user_id,
    asset,
    timeframe,
    signal,
    price,
    rsi,
    ema
):

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO signals
        (
            user_id,
            asset,
            timeframe,
            signal,
            price,
            rsi,
            ema
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            asset,
            timeframe,
            signal,
            price,
            rsi,
            ema
        )
    )

    connection.commit()
    connection.close()

    return True
def get_user_signals(user_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM signals
        WHERE user_id = ?
        """,
        (user_id,)
    )

    signals = cursor.fetchall()

    connection.close()

    return [dict(signal) for signal in signals]

def delete_signal(signal_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM signals
        WHERE id = ?
        """,
        (signal_id,)
    )

    connection.commit()
    connection.close()

    return True


def get_user_trades(user_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM trades
        WHERE user_id = ?
        """,
        (user_id,)
    )

    trades = cursor.fetchall()

    connection.close()

    return [dict(trade) for trade in trades]