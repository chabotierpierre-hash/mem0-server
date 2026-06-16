from flask import Flask, jsonify
from mem0 import MemoryClient
import os
import requests

app = Flask(__name__)

# 🔐 Remplace par ta vraie clé API Mem0
API_KEY = "m0-Y8lRYZ843Vu8RS4zcL09oT2zJpToLhWmuvTTTPH4"
USER_ID = "deepseek_user"

# 🤖 Telegram (les tokens sont lus depuis les variables d'environnement Render)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram non configuré")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
        print("✅ Message Telegram envoyé")
    except Exception as e:
        print(f"❌ Erreur Telegram : {e}")

@app.route('/')
def home():
    return "🧠 Serveur Mem0 actif !"

@app.route('/memories')
def get_memories():
    try:
        client = MemoryClient(api_key=API_KEY)
        memories = client.get_all(filters={"user_id": USER_ID})
        
        if isinstance(memories, dict) and "results" in memories:
            souvenirs = memories["results"]
        else:
            souvenirs = memories
        
        result = []
        for mem in souvenirs[:50]:
            if isinstance(mem, dict):
                text = mem.get("memory", str(mem))
            else:
                text = str(mem)
            result.append(text[:300])
        
        return jsonify({
            "status": "ok",
            "count": len(result),
            "memories": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test_telegram')
def test_telegram():
    send_telegram("Coucou Pierre, ce message vient de Render ! 🧠✨")
    return "Message Telegram envoyé !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
