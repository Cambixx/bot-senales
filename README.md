# 🤖 Bot de Trading Avanzado

Bot de análisis técnico para señales de trading con múltiples indicadores y gestión de riesgo.

## ✨ **Características**

- 🔍 **6+ Indicadores Técnicos**: RSI, MACD, Bollinger Bands, Stochastic, ADX, Volume
- 📊 **Análisis Avanzado**: 10 condiciones de entrada con sistema de puntuación
- 🛡️ **Gestión de Riesgo**: Stop loss dinámico y take profits escalonados
- 📱 **Notificaciones**: Alertas detalladas en Telegram
- 🔒 **Configuración Segura**: Variables de entorno para proteger claves
- 📈 **Análisis de Tendencia**: Puntuación 0-5 para validar señales
- 📝 **Logging Completo**: Registro detallado de actividad

## 🚀 **Inicio Rápido**

### **1. Configuración Inicial**
```bash
# Copiar archivo de configuración
cp env_example.txt .env

# Editar con tus claves
nano .env
```

### **2. Instalar Dependencias**
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### **3. Probar Configuración**
```bash
python test_bot.py
```

### **4. Iniciar Bot**
```bash
./iniciar_bot.sh
```

## 📱 **Configuración de Telegram**

1. Crear bot con @BotFather
2. Obtener token
3. Enviar mensaje al bot
4. Obtener Chat ID:
```bash
python get_chat_id.py
```

## ⚙️ **Configuración de Binance**

1. Crear API key en Binance
2. Configurar permisos (solo lectura)
3. Agregar claves al archivo `.env`

## 🎯 **Uso Diario**

### **Iniciar Bot**
```bash
./iniciar_bot.sh
```

### **Parar Bot**
```bash
./parar_bot.sh
```

### **Ver Logs**
```bash
tail -f trading_bot.log
```

## 📊 **Señales del Bot**

El bot envía señales cuando se cumplen múltiples condiciones:

- **RSI Oversold** (< 30)
- **Stochastic Oversold** (< 20)
- **Precio cerca de soporte**
- **Volumen confirmado** (1.5x promedio)
- **Tendencia alcista** (ADX > 25)
- **MACD positivo**
- **EMAs alineadas**

## 🛡️ **Gestión de Riesgo**

- **Stop Loss**: 2% o Bollinger Lower
- **Take Profit 1**: 3% de ganancia
- **Take Profit 2**: 6% de ganancia
- **Risk/Reward**: Mínimo 1.5:1

## 📁 **Estructura del Proyecto**

```
trading_bot/
├── advanced_trading_bot.py    # Bot principal
├── test_bot.py               # Bot de prueba
├── config_secure.py          # Configuración segura
├── .env                      # Variables de entorno
├── requirements.txt          # Dependencias
├── iniciar_bot.sh           # Script de inicio
├── parar_bot.sh             # Script de parada
├── get_chat_id.py           # Obtener Chat ID
└── trading_bot.log          # Logs del sistema
```

## 🔧 **Solución de Problemas**

### **Error de Chat ID**
```bash
python get_chat_id.py
```

### **Error de conexión**
```bash
python test_bot.py
```

### **Bot no responde**
```bash
./parar_bot.sh
./iniciar_bot.sh
```

## 📚 **Documentación**

- `GUIA_USO_PERSONAL.md` - Guía completa de uso
- `COMANDOS_RAPIDOS.md` - Comandos esenciales

## ⚠️ **Seguridad**

- ❌ Nunca compartir archivo `.env`
- ❌ Nunca subir claves a repositorios públicos
- ✅ Usar variables de entorno
- ✅ Hacer backup de configuración

## 🎉 **¡Listo para Trading!**

Con este bot tienes un sistema completo de análisis técnico para señales de trading con gestión de riesgo integrada.

**¡Que tengas buenos trades!** 📈🚀
