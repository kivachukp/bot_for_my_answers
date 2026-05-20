from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# =========================================
# LOAD ENV
# =========================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================================
# FLASK
# =========================================

app = Flask(__name__)

# CORS FIX
CORS(app)

# =========================================
# TELEGRAM
# =========================================

def send_telegram_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(url, json=payload)

    return response.json()

# =========================================
# TEST ROUTE
# =========================================

@app.route('/')
def home():

    return jsonify({
        "status": "Bot server is running"
    })

# =========================================
# RSVP FORM
# =========================================

@app.route('/send', methods=['POST'])
def send():

    try:

        data = request.get_json()

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

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================================
# CONTACT FORM
# =========================================

@app.route('/contact', methods=['POST'])
def contact():

    try:

        data = request.get_json()

        name = data.get('name', 'Не указано')
        email = data.get('email', 'Не указано')
        message = data.get('message', 'Пусто')

        telegram_message = f"""
📨 Новое сообщение с сайта!

👤 Имя: {name}

📧 Email: {email}

💬 Сообщение:
{message}
"""

        result = send_telegram_message(telegram_message)

        return jsonify({
            "success": True,
            "telegram_response": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================================
# START SERVER
# =========================================

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 8000))

    app.run(
        host='0.0.0.0',
        port=port
    )