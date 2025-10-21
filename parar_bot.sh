#!/bin/bash

# Script para parar el Bot de Trading
# Uso: ./parar_bot.sh

echo "🛑 Parando Bot de Trading..."
echo "=========================="

# Buscar procesos del bot
BOT_PROCESSES=$(ps aux | grep "advanced_trading_bot" | grep -v grep)

if [ -z "$BOT_PROCESSES" ]; then
    echo "ℹ️  No se encontraron bots ejecutándose"
else
    echo "📊 Procesos encontrados:"
    echo "$BOT_PROCESSES"
    echo ""
    
    # Obtener PIDs
    PIDS=$(echo "$BOT_PROCESSES" | awk '{print $2}')
    
    echo "🔄 Parando procesos..."
    for PID in $PIDS; do
        echo "  Matando proceso $PID..."
        kill -9 $PID 2>/dev/null
    done
    
    echo "✅ Bot detenido correctamente"
fi

# Verificar que se paró
sleep 2
REMAINING=$(ps aux | grep "advanced_trading_bot" | grep -v grep)

if [ -z "$REMAINING" ]; then
    echo "✅ Confirmado: Bot completamente detenido"
else
    echo "⚠️  Algunos procesos pueden seguir ejecutándose:"
    echo "$REMAINING"
    echo "💡 Ejecuta 'pkill -f advanced_trading_bot' si es necesario"
fi
