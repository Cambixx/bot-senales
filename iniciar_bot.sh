#!/bin/bash

# Script simple para iniciar el Bot de Trading
# Uso: ./iniciar_bot.sh

echo "🤖 Iniciando Bot de Trading Personal..."
echo "======================================"

# Verificar si estamos en el directorio correcto
if [ ! -f "advanced_trading_bot.py" ]; then
    echo "❌ No se encuentra advanced_trading_bot.py"
    echo "💡 Asegúrate de estar en el directorio correcto"
    exit 1
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Verificar configuración
echo "⚙️  Verificando configuración..."
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "💡 Copia env_example.txt como .env y configura tus claves"
    exit 1
fi

# Probar conexiones
echo "🔗 Probando conexiones..."
python test_bot.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Configuración correcta"
else
    echo "❌ Error en la configuración"
    echo "💡 Ejecuta: python test_bot.py para más detalles"
    exit 1
fi

# Iniciar bot
echo ""
echo "🚀 Iniciando Bot Avanzado..."
echo "📱 Las notificaciones llegarán a tu Telegram"
echo "⏹️  Para parar: Ctrl + C"
echo "======================================"

python advanced_trading_bot.py
