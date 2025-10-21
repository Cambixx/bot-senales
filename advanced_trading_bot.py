import time
import requests
import pandas as pd
import numpy as np
import logging
from binance.client import Client
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.volatility import BollingerBands
from ta.volume import VolumeWeightedAveragePrice
from datetime import datetime, timedelta
from config_secure import *

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE) if SAVE_LOGS_TO_FILE else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedTradingBot:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        self.alerted_symbols = set()
        self.last_signals = {}
        self.session_stats = {
            'signals_sent': 0,
            'errors': 0,
            'start_time': datetime.now()
        }
        
        # Validar configuración
        self._validate_config()
        
    def _validate_config(self):
        """Valida la configuración del bot"""
        if len(SYMBOLS) > 10:
            logger.warning("⚠️  Monitoreando más de 10 símbolos puede afectar el rendimiento")
        
        if CHECK_INTERVAL < 60:
            logger.warning("⚠️  Intervalos muy cortos pueden causar rate limiting")
            
        logger.info(f"✅ Bot configurado para {len(SYMBOLS)} símbolos")
    
    def send_telegram_message(self, text):
        """Envía mensaje a Telegram con manejo de errores mejorado"""
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID, 
            "text": text, 
            "parse_mode": MESSAGE_FORMAT
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Error Telegram API: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error enviando mensaje: {e}")
            return False
    
    def get_klines(self, symbol, interval, limit=200):
        """Obtiene datos de velas con manejo de errores mejorado"""
        try:
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            df = pd.DataFrame(klines, columns=[
                "open_time","open","high","low","close","volume",
                "close_time","quote_asset_volume","number_of_trades",
                "taker_buy_base","taker_buy_quote","ignore"
            ])
            
            # Convertir tipos de datos
            numeric_columns = ["open","high","low","close","volume","quote_asset_volume"]
            for col in numeric_columns:
                df[col] = df[col].astype(float)
            
            # Convertir timestamps
            df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
            df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
            
            return df
        except Exception as e:
            logger.error(f"Error obteniendo datos para {symbol}: {e}")
            self.session_stats['errors'] += 1
            return None
    
    def calculate_indicators(self, df):
        """Calcula todos los indicadores técnicos con validación"""
        try:
            if len(df) < max(RSI_PERIOD, BB_PERIOD, ADX_PERIOD, STOCH_K) + 10:
                logger.warning("Datos insuficientes para calcular indicadores")
                return None
                
            indicators = {}
            
            # RSI
            indicators['rsi'] = RSIIndicator(df["close"], window=RSI_PERIOD).rsi()
            
            # EMAs
            indicators['ema_fast'] = EMAIndicator(df["close"], window=EMA_FAST).ema_indicator()
            indicators['ema_slow'] = EMAIndicator(df["close"], window=EMA_SLOW).ema_indicator()
            
            # MACD
            macd = MACD(df["close"], window_slow=EMA_SLOW, window_fast=EMA_FAST, window_sign=EMA_SIGNAL)
            indicators['macd'] = macd.macd()
            indicators['macd_signal'] = macd.macd_signal()
            indicators['macd_histogram'] = macd.macd_diff()
            
            # Bollinger Bands
            bb = BollingerBands(df["close"], window=BB_PERIOD, window_dev=BB_STD)
            indicators['bb_upper'] = bb.bollinger_hband()
            indicators['bb_middle'] = bb.bollinger_mavg()
            indicators['bb_lower'] = bb.bollinger_lband()
            indicators['bb_width'] = (indicators['bb_upper'] - indicators['bb_lower']) / indicators['bb_middle']
            
            # ADX
            indicators['adx'] = ADXIndicator(df["high"], df["low"], df["close"], window=ADX_PERIOD).adx()
            
            # Stochastic
            stoch = StochasticOscillator(df["high"], df["low"], df["close"], window=STOCH_K, smooth_window=STOCH_D)
            indicators['stoch_k'] = stoch.stoch()
            indicators['stoch_d'] = stoch.stoch_signal()
            
            # Volumen - usar SMA simple de pandas
            indicators['volume_sma'] = df["volume"].rolling(window=20).mean()
            
            return indicators
        except Exception as e:
            logger.error(f"Error calculando indicadores: {e}")
            return None
    
    def analyze_trend_strength(self, indicators):
        """Analiza la fuerza de la tendencia con puntuación"""
        try:
            # ADX para fuerza de tendencia
            adx_strong = indicators['adx'].iloc[-1] > ADX_TREND_THRESHOLD
            
            # MACD para momentum
            macd_positive = indicators['macd'].iloc[-1] > indicators['macd_signal'].iloc[-1]
            macd_increasing = indicators['macd'].iloc[-1] > indicators['macd'].iloc[-2]
            
            # EMAs para tendencia
            ema_bullish = indicators['ema_fast'].iloc[-1] > indicators['ema_slow'].iloc[-1]
            ema_separation = (indicators['ema_fast'].iloc[-1] - indicators['ema_slow'].iloc[-1]) / indicators['ema_slow'].iloc[-1]
            
            # Puntuación de tendencia
            trend_score = sum([
                adx_strong,
                macd_positive,
                macd_increasing,
                ema_bullish,
                ema_separation > 0.01  # EMAs separadas al menos 1%
            ])
            
            return {
                'adx_strong': adx_strong,
                'macd_positive': macd_positive,
                'macd_increasing': macd_increasing,
                'ema_bullish': ema_bullish,
                'ema_separation': ema_separation,
                'trend_score': trend_score,
                'trend_strength': 'FUERTE' if trend_score >= 4 else 'MODERADA' if trend_score >= 2 else 'DÉBIL'
            }
        except Exception as e:
            logger.error(f"Error analizando tendencia: {e}")
            return {'trend_score': 0, 'trend_strength': 'DÉBIL'}
    
    def check_long_signal(self, symbol, df, indicators):
        """Verifica señales LONG con análisis avanzado"""
        try:
            # Valores actuales
            current_price = df["close"].iloc[-1]
            current_volume = df["volume"].iloc[-1]
            avg_volume = indicators['volume_sma'].iloc[-1]
            
            # Indicadores principales
            rsi = indicators['rsi'].iloc[-1]
            bb_upper = indicators['bb_upper'].iloc[-1]
            bb_lower = indicators['bb_lower'].iloc[-1]
            bb_middle = indicators['bb_middle'].iloc[-1]
            stoch_k = indicators['stoch_k'].iloc[-1]
            stoch_d = indicators['stoch_d'].iloc[-1]
            
            # Análisis de tendencia
            trend_analysis = self.analyze_trend_strength(indicators)
            
            # Condiciones de entrada
            conditions = {
                'rsi_oversold': rsi < RSI_OVERSOLD,
                'rsi_rising': rsi > indicators['rsi'].iloc[-2],  # RSI subiendo
                'price_above_bb_lower': current_price > bb_lower,
                'price_near_support': current_price <= bb_middle + (bb_upper - bb_middle) * 0.3,
                'stoch_oversold': stoch_k < 20 and stoch_d < 20,
                'stoch_bullish_cross': stoch_k > stoch_d and indicators['stoch_k'].iloc[-2] <= indicators['stoch_d'].iloc[-2],
                'volume_confirmation': current_volume > (avg_volume * VOLUME_MULTIPLIER),
                'trend_support': trend_analysis['trend_score'] >= 2,
                'macd_bullish': indicators['macd'].iloc[-1] > indicators['macd'].iloc[-2],
                'bb_squeeze': indicators['bb_width'].iloc[-1] < indicators['bb_width'].iloc[-5]  # Bollinger se contrae
            }
            
            # Contar condiciones cumplidas
            conditions_met = sum(conditions.values())
            
            # Determinar fuerza de señal
            if conditions_met >= STRONG_SIGNAL_CONDITIONS:
                signal_strength = 'FUERTE'
            elif conditions_met >= MIN_CONDITIONS_FOR_SIGNAL:
                signal_strength = 'MODERADA'
            else:
                signal_strength = 'DÉBIL'
            
            # Validar que sea una señal válida
            is_valid_signal = conditions_met >= MIN_CONDITIONS_FOR_SIGNAL
            
            return {
                'signal': is_valid_signal,
                'strength': signal_strength,
                'conditions_met': conditions_met,
                'total_conditions': len(conditions),
                'conditions': conditions,
                'trend_analysis': trend_analysis,
                'current_price': current_price,
                'indicators': {
                    'rsi': rsi,
                    'stoch_k': stoch_k,
                    'stoch_d': stoch_d,
                    'bb_position': ((current_price - bb_lower) / (bb_upper - bb_lower)) * 100,
                    'volume_ratio': current_volume / avg_volume,
                    'bb_width': indicators['bb_width'].iloc[-1]
                }
            }
            
        except Exception as e:
            logger.error(f"Error verificando señal LONG para {symbol}: {e}")
            return {'signal': False}
    
    def calculate_risk_levels(self, current_price, bb_upper, bb_lower):
        """Calcula niveles de riesgo y objetivos con análisis técnico"""
        # Stop Loss dinámico
        stop_loss = min(
            current_price * (1 - STOP_LOSS_PERCENTAGE),  # Stop loss por porcentaje
            bb_lower * 0.99  # Stop loss por Bollinger Bands
        )
        
        # Take Profits
        take_profit_1 = current_price * (1 + TAKE_PROFIT_1_PERCENTAGE)
        take_profit_2 = current_price * (1 + TAKE_PROFIT_2_PERCENTAGE)
        
        # Calcular ratios riesgo/recompensa
        risk_amount = current_price - stop_loss
        reward_1 = take_profit_1 - current_price
        reward_2 = take_profit_2 - current_price
        
        risk_reward_1 = reward_1 / risk_amount if risk_amount > 0 else 0
        risk_reward_2 = reward_2 / risk_amount if risk_amount > 0 else 0
        
        return {
            'stop_loss': stop_loss,
            'take_profit_1': take_profit_1,
            'take_profit_2': take_profit_2,
            'risk_amount': risk_amount,
            'risk_reward_1': risk_reward_1,
            'risk_reward_2': risk_reward_2,
            'is_good_risk_reward': risk_reward_1 >= MIN_RISK_REWARD_RATIO
        }
    
    def create_signal_message(self, symbol, signal_data, risk_levels):
        """Crea mensaje de señal con información detallada"""
        price = signal_data['current_price']
        strength = signal_data['strength']
        conditions_met = signal_data['conditions_met']
        total_conditions = signal_data['total_conditions']
        indicators = signal_data['indicators']
        trend = signal_data['trend_analysis']
        
        # Emojis según fuerza
        emoji_map = {
            'FUERTE': '🚀',
            'MODERADA': '📈', 
            'DÉBIL': '⚠️'
        }
        emoji = emoji_map.get(strength, '📊')
        
        # Color según fuerza
        color_map = {
            'FUERTE': '🟢',
            'MODERADA': '🟡',
            'DÉBIL': '🔴'
        }
        color = color_map.get(strength, '⚪')
        
        message = f"""
{emoji} <b>SEÑAL LONG {strength}</b> {color}
<b>{symbol}</b>

💰 <b>Precio:</b> ${price:.4f}
📊 <b>Confirmaciones:</b> {conditions_met}/{total_conditions}

📈 <b>Indicadores Técnicos:</b>
• RSI: {indicators['rsi']:.1f}
• Stoch K/D: {indicators['stoch_k']:.1f}/{indicators['stoch_d']:.1f}
• Posición BB: {indicators['bb_position']:.1f}%
• Volumen: {indicators['volume_ratio']:.1f}x promedio
• Ancho BB: {indicators['bb_width']:.3f}

🎯 <b>Análisis de Tendencia:</b>
• Fuerza: {trend['trend_strength']} ({trend['trend_score']}/5)
• ADX: {'✅' if trend['adx_strong'] else '❌'}
• MACD: {'✅' if trend['macd_positive'] else '❌'}
• EMAs: {'✅' if trend['ema_bullish'] else '❌'}

🛡️ <b>Gestión de Riesgo:</b>
• Stop Loss: ${risk_levels['stop_loss']:.4f}
• TP1 (3%): ${risk_levels['take_profit_1']:.4f}
• TP2 (6%): ${risk_levels['take_profit_2']:.4f}
• R/R Ratio: {risk_levels['risk_reward_1']:.1f}:1 {'✅' if risk_levels['is_good_risk_reward'] else '⚠️'}

⏰ {datetime.now().strftime('%H:%M:%S')}
📅 {datetime.now().strftime('%d/%m/%Y')}
"""
        return message
    
    def check_signals(self):
        """Función principal de análisis de señales"""
        for symbol in SYMBOLS:
            try:
                logger.info(f"Analizando {symbol}...")
                
                # Obtener datos
                df = self.get_klines(symbol, INTERVAL)
                if df is None or len(df) < 50:
                    logger.warning(f"Insuficientes datos para {symbol}")
                    continue
                
                # Calcular indicadores
                indicators = self.calculate_indicators(df)
                if indicators is None:
                    continue
                
                # Verificar señal LONG
                signal_data = self.check_long_signal(symbol, df, indicators)
                
                if signal_data['signal']:
                    # Verificar tiempo mínimo entre señales
                    now = datetime.now()
                    if symbol in self.last_signals:
                        time_diff = (now - self.last_signals[symbol]).total_seconds()
                        if time_diff < MIN_TIME_BETWEEN_SIGNALS:
                            logger.info(f"Señal para {symbol} ignorada (muy reciente)")
                            continue
                    
                    # Calcular niveles de riesgo
                    risk_levels = self.calculate_risk_levels(
                        signal_data['current_price'],
                        indicators['bb_upper'].iloc[-1],
                        indicators['bb_lower'].iloc[-1]
                    )
                    
                    # Crear y enviar mensaje
                    message = self.create_signal_message(symbol, signal_data, risk_levels)
                    
                    if self.send_telegram_message(message):
                        logger.info(f"✅ Señal {signal_data['strength']} enviada: {symbol}")
                        self.alerted_symbols.add(symbol)
                        self.last_signals[symbol] = now
                        self.session_stats['signals_sent'] += 1
                    else:
                        logger.error(f"❌ Error enviando señal para {symbol}")
                else:
                    # Remover de alertas si ya no cumple condiciones
                    if symbol in self.alerted_symbols:
                        self.alerted_symbols.discard(symbol)
                        
            except Exception as e:
                logger.error(f"Error procesando {symbol}: {e}")
                self.session_stats['errors'] += 1
    
    def send_startup_notification(self):
        """Envía notificación de inicio del bot"""
        if SEND_STARTUP_NOTIFICATION:
            message = f"""
🤖 <b>Bot de Trading Iniciado</b>

📊 <b>Configuración:</b>
• Símbolos: {len(SYMBOLS)} ({', '.join(SYMBOLS[:3])}{'...' if len(SYMBOLS) > 3 else ''})
• Timeframe: {INTERVAL}
• Verificación: cada {CHECK_INTERVAL}s

⚙️ <b>Parámetros:</b>
• RSI: {RSI_PERIOD} períodos
• EMAs: {EMA_FAST}/{EMA_SLOW}
• BB: {BB_PERIOD} períodos
• ADX: {ADX_PERIOD} períodos

⏰ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}
"""
            self.send_telegram_message(message)
    
    def send_error_notification(self, error_msg):
        """Envía notificación de error"""
        if SEND_ERROR_NOTIFICATIONS:
            message = f"""
❌ <b>Error en Bot de Trading</b>

🔍 <b>Error:</b> {error_msg}
⏰ <b>Hora:</b> {datetime.now().strftime('%H:%M:%S')}

📊 <b>Estadísticas de sesión:</b>
• Señales enviadas: {self.session_stats['signals_sent']}
• Errores: {self.session_stats['errors']}
• Tiempo activo: {datetime.now() - self.session_stats['start_time']}
"""
            self.send_telegram_message(message)
    
    def run(self):
        """Función principal del bot"""
        logger.info("🤖 Bot de Trading Avanzado iniciado...")
        logger.info(f"📊 Monitoreando: {', '.join(SYMBOLS)}")
        logger.info(f"⏱️  Intervalo: {INTERVAL} | Verificación cada {CHECK_INTERVAL}s")
        logger.info("=" * 50)
        
        # Enviar notificación de inicio
        self.send_startup_notification()
        
        try:
            while True:
                self.check_signals()
                logger.info(f"⏳ Esperando {CHECK_INTERVAL}s para próxima verificación...")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            logger.info("\n🛑 Bot detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error crítico: {e}")
            self.send_error_notification(str(e))
        finally:
            logger.info("👋 Bot finalizado")

if __name__ == "__main__":
    bot = AdvancedTradingBot()
    bot.run()
