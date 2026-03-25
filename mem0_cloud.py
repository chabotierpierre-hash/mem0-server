from flask import Flask, jsonify
from mem0 import MemoryClient

app = Flask(__name__)

API_KEY = "m0-Y8lRYZ843Vu8RS4zcL09oT2zJpToLhWmuvTTTPH4"
USER_ID = "deepseek_user"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)