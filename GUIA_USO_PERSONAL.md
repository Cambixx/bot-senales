# 🤖 Guía de Uso Personal - Bot de Trading

## 📋 **Índice**
- [Inicio Rápido](#inicio-rápido)
- [Métodos de Ejecución](#métodos-de-ejecución)
- [Configuración](#configuración)
- [Monitoreo](#monitoreo)
- [Solución de Problemas](#solución-de-problemas)
- [Comandos Útiles](#comandos-útiles)

---

## 🚀 **Inicio Rápido**

### **Método 1: Script Automático (Recomendado)**
```bash
cd /Users/carlosrabago/Proyectos/trading_bot
./start_bot.sh
```

### **Método 2: Manual**
```bash
cd /Users/carlosrabago/Proyectos/trading_bot
source venv/bin/activate
python advanced_trading_bot.py
```

### **Método 3: Bot de Prueba**
```bash
cd /Users/carlosrabago/Proyectos/trading_bot
source venv/bin/activate
python test_bot.py
```

---

## 🛠️ **Métodos de Ejecución**

### **Bot de Trading Avanzado**
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar bot
python advanced_trading_bot.py
```
**Características:**
- ✅ 6+ indicadores técnicos (RSI, MACD, Bollinger Bands, Stochastic, ADX)
- ✅ Sistema de logging completo
- ✅ Gestión de riesgo con stop loss y take profits
- ✅ Notificaciones detalladas en Telegram
- ✅ Configuración segura con variables de entorno
- ✅ Análisis de tendencia con puntuación
- ✅ 10 condiciones de entrada para señales precisas

### **Bot de Prueba**
```bash
python test_bot.py
```
**Uso:** Verificar configuración y conexiones

---

## ⚙️ **Configuración**

### **Archivo de Configuración: `.env`**
```bash
# Editar configuración
nano .env
```

**Variables principales:**
```env
# Telegram
TELEGRAM_TOKEN=tu_token_aqui
CHAT_ID=tu_chat_id_aqui

# Binance
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui

# Trading
SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT
INTERVAL=5m
CHECK_INTERVAL=300
```

### **Configuración Avanzada: `config_secure.py`**
Para ajustar parámetros técnicos:
- RSI: 14 períodos
- EMAs: 12/26
- Bollinger Bands: 20 períodos
- ADX: 14 períodos

---

## 📊 **Monitoreo del Bot**

### **Logs en Tiempo Real**
```bash
# Ver logs en consola
tail -f trading_bot.log
```

### **Estadísticas de Sesión**
El bot muestra:
- 📊 Señales enviadas
- ❌ Errores encontrados
- ⏰ Tiempo de actividad
- 📈 Símbolos analizados

### **Notificaciones de Telegram**
- 🚀 Señales de trading
- ⚠️ Errores críticos
- 📊 Estadísticas de sesión
- 🔄 Notificaciones de inicio/parada

---

## 🛑 **Cómo Parar el Bot**

### **Método 1: Interrupción de Teclado**
```bash
# En la terminal donde corre el bot
Ctrl + C
```

### **Método 2: Si está en Segundo Plano**
```bash
# Encontrar el proceso
ps aux | grep python

# Matar el proceso (reemplaza PID con el número)
kill -9 PID
```

### **Método 3: Matar Todos los Procesos Python**
```bash
# CUIDADO: Esto mata TODOS los procesos Python
pkill -f python
```

### **Método 4: Usando el Nombre del Archivo**
```bash
# Matar solo el bot de trading
pkill -f advanced_trading_bot.py
```

---

## 🔧 **Solución de Problemas**

### **Error: "chat not found"**
```bash
# 1. Verificar Chat ID
python get_chat_id.py

# 2. Enviar mensaje al bot en Telegram
# 3. Actualizar .env con el Chat ID correcto
```

### **Error: "API key invalid"**
```bash
# 1. Verificar claves en .env
cat .env

# 2. Probar conexión
python test_bot.py

# 3. Crear nuevas claves si es necesario
```

### **Error: "Module not found"**
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt
```

### **Bot no envía señales**
```bash
# 1. Verificar configuración
python test_bot.py

# 2. Revisar logs
tail -f trading_bot.log

# 3. Verificar condiciones de mercado
# (RSI < 30, precio > EMA, etc.)
```

---

## 📱 **Comandos Útiles**

### **Verificación Rápida**
```bash
# Verificar configuración
python test_bot.py

# Obtener Chat ID
python get_chat_id.py

# Ver logs
tail -f trading_bot.log
```

### **Gestión de Procesos**
```bash
# Ver procesos Python
ps aux | grep python

# Matar bot específico
pkill -f advanced_trading_bot.py

# Ver puertos en uso
lsof -i :8000
```

### **Gestión de Archivos**
```bash
# Ver archivos de log
ls -la *.log

# Limpiar logs antiguos
rm -f *.log.old

# Ver tamaño de archivos
du -sh *
```

### **Entorno Virtual**
```bash
# Activar
source venv/bin/activate

# Desactivar
deactivate

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 🎯 **Flujo de Trabajo Recomendado**

### **Inicio del Día**
1. **Verificar configuración:**
   ```bash
   python test_bot.py
   ```

2. **Iniciar bot:**
   ```bash
   ./start_bot.sh
   # Seleccionar opción 3 (Bot Avanzado)
   ```

3. **Monitorear:**
   - Revisar notificaciones en Telegram
   - Verificar logs en consola
   - Confirmar que está analizando símbolos

### **Durante el Día**
- 📱 Revisar notificaciones de Telegram
- 📊 Verificar señales recibidas
- ⚠️ Atender errores si aparecen

### **Fin del Día**
1. **Parar bot:**
   ```bash
   Ctrl + C
   ```

2. **Revisar estadísticas:**
   - Señales enviadas
   - Errores encontrados
   - Rendimiento del día

---

## 📞 **Soporte y Mantenimiento**

### **Archivos Importantes**
- `.env` - Configuración de claves
- `config_secure.py` - Parámetros técnicos
- `trading_bot.log` - Logs del sistema
- `requirements.txt` - Dependencias

### **Backup Recomendado**
```bash
# Crear backup de configuración
cp .env .env.backup
cp config_secure.py config_secure.py.backup
```

### **Actualizaciones**
```bash
# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar versión de Python
python --version
```

---

## ⚠️ **Notas de Seguridad**

### **Nunca Compartir:**
- ❌ Archivo `.env`
- ❌ Claves de API
- ❌ Tokens de Telegram
- ❌ Logs con información sensible

### **Buenas Prácticas:**
- ✅ Usar `config_secure.py` para producción
- ✅ Hacer backup de configuración
- ✅ Monitorear logs regularmente
- ✅ Mantener dependencias actualizadas

---

## 🎉 **¡Listo para Trading!**

Con esta guía tienes todo lo necesario para:
- ✅ Iniciar y parar el bot
- ✅ Configurar parámetros
- ✅ Monitorear funcionamiento
- ✅ Solucionar problemas
- ✅ Mantener el sistema

**¡Que tengas buenos trades!** 📈🚀
