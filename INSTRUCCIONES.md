# Bot de señales LONG - Checklist rápido

## 🔹 Activar entorno virtual

Terminal
cd ~/trading_bot
source venv/bin/activate

🔹 Arrancar el bot

Terminal
python multi_long_bot.py

🔹 Detener el bot

Desde la misma terminal: CTRL + C

Si está en segundo plano:

Terminal
ps aux | grep python
kill -9 PID

🔹 Salir del entorno virtual

Terminal
deactivate

Listo. Tu bot deja de ejecutarse y vuelves al Python del sistema.