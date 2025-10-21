# Configuración SEGURA del Bot de Trading
# Usa variables de entorno para proteger secretos

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ================================
# CONFIGURACIÓN DE API (SEGURA)
# ================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')

# Validar que las variables estén configuradas
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN no está configurado en las variables de entorno")
if not CHAT_ID:
    raise ValueError("CHAT_ID no está configurado en las variables de entorno")
if not BINANCE_API_KEY:
    raise ValueError("BINANCE_API_KEY no está configurado en las variables de entorno")
if not BINANCE_API_SECRET:
    raise ValueError("BINANCE_API_SECRET no está configurado en las variables de entorno")

# ================================
# CONFIGURACIÓN DE TRADING
# ================================
# Símbolos a monitorear (máximo 10 recomendado)
SYMBOLS = os.getenv('SYMBOLS', 'BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT').split(',')

# Timeframe para análisis (1m, 5m, 15m, 1h, 4h, 1d)
INTERVAL = os.getenv('INTERVAL', '5m')

# Intervalo entre verificaciones (en segundos)
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))

# ================================
# CONFIGURACIÓN DE INDICADORES
# ================================
# RSI
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# EMAs
EMA_FAST = 12
EMA_SLOW = 26
EMA_SIGNAL = 9

# Bollinger Bands
BB_PERIOD = 20
BB_STD = 2

# ADX (fuerza de tendencia)
ADX_PERIOD = 14
ADX_TREND_THRESHOLD = 25

# Stochastic
STOCH_K = 14
STOCH_D = 3

# Volumen
VOLUME_MULTIPLIER = 1.5  # Volumen debe ser X veces el promedio

# ================================
# CONFIGURACIÓN DE SEÑALES
# ================================
# Mínimo de condiciones que debe cumplir para generar señal
MIN_CONDITIONS_FOR_SIGNAL = 3

# Condiciones para señal FUERTE
STRONG_SIGNAL_CONDITIONS = 5

# Tiempo mínimo entre señales del mismo símbolo (en segundos)
MIN_TIME_BETWEEN_SIGNALS = 1800  # 30 minutos

# ================================
# CONFIGURACIÓN DE RIESGO
# ================================
# Porcentaje de stop loss (1% = 0.01)
STOP_LOSS_PERCENTAGE = 0.02  # 2%

# Porcentajes de take profit
TAKE_PROFIT_1_PERCENTAGE = 0.03  # 3%
TAKE_PROFIT_2_PERCENTAGE = 0.06  # 6%

# Ratio riesgo/recompensa mínimo
MIN_RISK_REWARD_RATIO = 1.5

# ================================
# CONFIGURACIÓN DE LOGGING
# ================================
# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL = "INFO"

# Guardar logs en archivo
SAVE_LOGS_TO_FILE = True
LOG_FILE = "trading_bot.log"

# ================================
# CONFIGURACIÓN DE NOTIFICACIONES
# ================================
# Enviar notificaciones de inicio/parada del bot
SEND_STARTUP_NOTIFICATION = True
SEND_ERROR_NOTIFICATIONS = True

# Formato de mensajes
MESSAGE_FORMAT = "HTML"  # HTML o Markdown
