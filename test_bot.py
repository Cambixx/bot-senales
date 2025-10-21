#!/usr/bin/env python3
"""
Bot de prueba para verificar la configuración
"""

import time
import requests
import pandas as pd
import numpy as np
from binance.client import Client
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
INTERVAL = "5m"
RSI_PERIOD = 14
EMA_PERIOD = 20

def send_telegram_message(text):
    """Envía mensaje a Telegram"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("❌ Token o Chat ID no configurado")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"📤 Enviando mensaje... Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Mensaje enviado correctamente")
            return True
        else:
            print(f"❌ Error: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        return False

def test_binance_connection():
    """Prueba la conexión con Binance"""
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        # Obtener información de la cuenta
        account_info = client.get_account()
        print("✅ Conexión con Binance exitosa")
        return True
    except Exception as e:
        print(f"❌ Error conectando con Binance: {e}")
        return False

def test_telegram_connection():
    """Prueba la conexión con Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot de Telegram: {bot_info['result']['first_name']}")
            return True
        else:
            print(f"❌ Error Telegram: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error conectando con Telegram: {e}")
        return False

def get_simple_signal(symbol):
    """Obtiene una señal simple"""
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        
        # Obtener datos
        klines = client.get_klines(symbol=symbol, interval=INTERVAL, limit=100)
        df = pd.DataFrame(klines, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","quote_asset_volume","number_of_trades",
            "taker_buy_base","taker_buy_quote","ignore"
        ])
        df["close"] = df["close"].astype(float)
        
        # Calcular indicadores
        rsi = RSIIndicator(df["close"], window=RSI_PERIOD).rsi()
        ema = EMAIndicator(df["close"], window=EMA_PERIOD).ema_indicator()
        
        last_rsi = rsi.iloc[-1]
        last_ema = ema.iloc[-1]
        last_price = df["close"].iloc[-1]
        
        # Señal simple
        signal = last_rsi < 30 and last_price > last_ema
        
        return {
            'symbol': symbol,
            'price': last_price,
            'rsi': last_rsi,
            'ema': last_ema,
            'signal': signal
        }
    except Exception as e:
        print(f"❌ Error analizando {symbol}: {e}")
        return None

def main():
    print("🧪 Bot de Prueba - Verificando Configuración")
    print("=" * 50)
    
    # Verificar configuración
    print("📋 Verificando configuración...")
    print(f"  Telegram Token: {'✅' if TELEGRAM_TOKEN else '❌'}")
    print(f"  Chat ID: {'✅' if CHAT_ID else '❌'}")
    print(f"  Binance API Key: {'✅' if BINANCE_API_KEY else '❌'}")
    print(f"  Binance API Secret: {'✅' if BINANCE_API_SECRET else '❌'}")
    
    if not all([TELEGRAM_TOKEN, CHAT_ID, BINANCE_API_KEY, BINANCE_API_SECRET]):
        print("❌ Configuración incompleta. Revisa el archivo .env")
        return
    
    # Probar conexiones
    print("\n🔗 Probando conexiones...")
    telegram_ok = test_telegram_connection()
    binance_ok = test_binance_connection()
    
    if not telegram_ok or not binance_ok:
        print("❌ Error en las conexiones. Revisa tus claves.")
        return
    
    # Probar envío de mensaje
    print("\n📤 Probando envío de mensaje...")
    test_message = f"""
🧪 <b>Prueba del Bot de Trading</b>

✅ Conexiones verificadas
⏰ {datetime.now().strftime('%H:%M:%S')}

Si ves este mensaje, la configuración es correcta.
"""
    
    if send_telegram_message(test_message):
        print("✅ Bot funcionando correctamente")
        
        # Probar análisis
        print("\n📊 Probando análisis de señales...")
        for symbol in SYMBOLS:
            signal_data = get_simple_signal(symbol)
            if signal_data:
                print(f"  {symbol}: Precio ${signal_data['price']:.2f}, RSI {signal_data['rsi']:.1f}")
    else:
        print("❌ Error enviando mensaje. Revisa el Chat ID.")

if __name__ == "__main__":
    main()
