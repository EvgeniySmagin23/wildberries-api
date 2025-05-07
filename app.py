from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

WB_API_TOKEN = os.getenv("WB_API_TOKEN")

if not WB_API_TOKEN:
    raise ValueError("Не найдена переменная окружения WB_API_TOKEN")

@app.route('/')
def home():
    return "✅ Wildberries Proxy API is running"

@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.get_json(force=True)
        vendorCode = data.get('vendorCode')
        quantity = data.get('quantity')

        if not vendorCode or quantity is None:
            return jsonify({"error": "Missing vendorCode or quantity"}), 400

        url = "https://suppliers-api.wildberries.ru/api/v3/stocks/by-partner-sku"
        headers = {
            "Authorization": WB_API_TOKEN,
            "Content-Type": "application/json"
        }
        payload = {
            "skus": [
                {
                    "vendorCode": str(vendorCode),
                    "quantity": int(quantity)
                }
            ]
        }

        response = requests.put(url, headers=headers, json=payload)

        return jsonify({
            "status": response.status_code,
            "response": response.json() if response.content else {}
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
