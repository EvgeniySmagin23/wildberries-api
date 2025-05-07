
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Wildberries API is running"

@app.route("/update_stock", methods=["POST"])
def update_stock():
    data = request.get_json()
    nmId = data.get("nmId")
    quantity = data.get("quantity", 1)
    
    payload = [{"nmId": nmId, "quantity": quantity}]
    headers = {
        "Authorization": "ВАШ_ТОКЕН",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://api-seller.wildberries.ru/content/v1/stocks", json=payload, headers=headers)
        return jsonify({"status": response.status_code, "data": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
