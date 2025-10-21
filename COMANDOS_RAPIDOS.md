# ⚡ Comandos Rápidos - Bot de Trading

## 🚀 **INICIAR BOT**
```bash
./iniciar_bot.sh
```

## 🛑 **PARAR BOT**
```bash
./parar_bot.sh
```

## 🧪 **PROBAR CONFIGURACIÓN**
```bash
python test_bot.py
```

## 🎯 **EJECUTAR BOT DIRECTAMENTE**
```bash
source venv/bin/activate
python advanced_trading_bot.py
```

## 📊 **VER LOGS**
```bash
tail -f trading_bot.log
```

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error de Chat ID:**
```bash
python get_chat_id.py
```

### **Error de conexión:**
```bash
python test_bot.py
```

### **Bot no responde:**
```bash
./parar_bot.sh
./iniciar_bot.sh
```

---

## 📱 **FLUJO DIARIO**

### **Mañana:**
1. `./iniciar_bot.sh`
2. Verificar notificación en Telegram
3. Revisar que analiza símbolos

### **Durante el día:**
- Revisar notificaciones de Telegram
- Verificar señales recibidas

### **Noche:**
1. `./parar_bot.sh`
2. Revisar estadísticas del día

---

## ⚙️ **CONFIGURACIÓN**

### **Editar parámetros:**
```bash
nano .env
```

### **Ver configuración:**
```bash
cat .env
```

### **Backup configuración:**
```bash
cp .env .env.backup
```

---

## 🆘 **EMERGENCIAS**

### **Bot colgado:**
```bash
pkill -f python
```

### **Reiniciar todo:**
```bash
./parar_bot.sh
source venv/bin/activate
./iniciar_bot.sh
```

### **Ver procesos:**
```bash
ps aux | grep python
```

---

**¡Listo para trading!** 🚀📈
