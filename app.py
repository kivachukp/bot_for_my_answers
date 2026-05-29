from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv


app = Flask(__name__)

# =========================================
# TELEGRAM CONFIG
# =========================================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# =========================================
# SEND MESSAGE TO TELEGRAM
# =========================================

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=payload)

    return response.json()


# =========================================
# API ROUTE
# =========================================

@app.route('/send', methods=['POST'])
def send():
    data = request.json

    name = data.get('name', 'Не указано')
    phone = data.get('phone', 'Не указано')
    messenger = data.get('messenger', 'Не указано')
    idea = data.get('idea', 'Не указано')

    message = f"""
📩 Новая заявка!

👤 Имя: {name}

📞 Телефон: {phone}

💬 Мессенджер: {messenger}

💡 Идея:
{idea}
"""

    result = send_telegram_message(message)

    return jsonify({
        "success": True,
        "telegram_response": result
    })


# =========================================
# START SERVER
# =========================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)