import time
import requests
import pandas as pd
from binance.client import Client
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# ----------------------------
# CONFIGURACIÓN
TELEGRAM_TOKEN = "8260160763:AAHyBSsei56QlraABkdLRWaR_WVINQD7TpE"
CHAT_ID = "6495316406"

BINANCE_API_KEY = "BvEn74pFINfn2frOuvnq8eXnQ7SZP2P2udA1xk3XB2HNYstw0wvyDUqm8dv9qacv"
BINANCE_API_SECRET = "UbFhS8QABsOn2AMYoR0ZWkterGDt9qbaYCWx9ODb6wxu34kmiTxKcwIDM16FTFtx"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # criptos a monitorear
INTERVAL = "1m"  # timeframe
RSI_PERIOD = 14
EMA_PERIOD = 20
CHECK_INTERVAL = 60  # segundos entre comprobaciones
# ----------------------------

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
alerted_symbols = set()  # para no spamear alertas repetidas

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def get_klines(symbol, interval, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","quote_asset_volume","number_of_trades",
        "taker_buy_base","taker_buy_quote","ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

def check_signals():
    global alerted_symbols
    for symbol in SYMBOLS:
        try:
            df = get_klines(symbol, INTERVAL)
            
            # RSI y EMA
            rsi = RSIIndicator(df["close"], window=RSI_PERIOD).rsi()
            ema = EMAIndicator(df["close"], window=EMA_PERIOD).ema_indicator()
            last_rsi = rsi.iloc[-1]
            last_ema = ema.iloc[-1]
            last_price = df["close"].iloc[-1]
            
            # Señal LONG
            if last_rsi < 30 and last_price > last_ema:
                if symbol not in alerted_symbols:
                    message = (
                        f"🚀 <b>SEÑAL LONG</b>\n"
                        f"{symbol}\n"
                        f"Precio: {last_price:.2f}\n"
                        f"RSI: {last_rsi:.2f}\n"
                        f"EMA20: {last_ema:.2f}"
                    )
                    send_telegram_message(message)
                    print(f"Alerta enviada: {symbol} - Precio: {last_price:.2f}")
                    alerted_symbols.add(symbol)
            else:
                # si ya no cumple la condición, quitamos de alertas para reactivar luego
                alerted_symbols.discard(symbol)
        except Exception as e:
            print(f"Error al procesar {symbol}: {e}")

if __name__ == "__main__":
    print(f"Bot MULTI-LONG corriendo para {', '.join(SYMBOLS)}...")
    while True:
        check_signals()
        time.sleep(CHECK_INTERVAL)
