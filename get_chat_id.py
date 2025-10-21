#!/usr/bin/env python3
"""
Script para obtener el Chat ID correcto de Telegram
Ejecutar después de enviar un mensaje al bot
"""

import requests
import os
from dotenv import load_dotenv

def get_chat_id():
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        print("❌ TELEGRAM_TOKEN no encontrado en .env")
        return
    
    # Obtener actualizaciones
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['ok'] and data['result']:
            print("📱 Chats encontrados:")
            for update in data['result']:
                if 'message' in update:
                    chat = update['message']['chat']
                    print(f"  Chat ID: {chat['id']}")
                    print(f"  Tipo: {chat['type']}")
                    print(f"  Usuario: {chat.get('first_name', 'N/A')}")
                    print(f"  Username: @{chat.get('username', 'N/A')}")
                    print("  ---")
        else:
            print("❌ No hay mensajes recientes")
            print("💡 Envía un mensaje a tu bot primero, luego ejecuta este script")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("🔍 Obteniendo Chat ID de Telegram...")
    print("💡 Asegúrate de haber enviado un mensaje a tu bot primero")
    print("=" * 50)
    get_chat_id()
