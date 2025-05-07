from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

WB_API_TOKEN = os.getenv("WB_API_TOKEN")
WAREHOUSE_ID = os.getenv("WB_WAREHOUSE_ID")

if not WB_API_TOKEN or not WAREHOUSE_ID:
    raise ValueError("Не найдены переменные окружения WB_API_TOKEN и/или WB_WAREHOUSE_ID")

try:
    WAREHOUSE_ID = int(WAREHOUSE_ID)
except ValueError:
    raise ValueError("WAREHOUSE_ID должен быть числом")

@app.route('/')
def home():
    return "✅ Wildberries Proxy API is running"

@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.get_json(force=True)
        nmId = data.get('nmId')
        quantity = data.get('quantity')

        if not nmId or quantity is None:
            return jsonify({"error": "Missing nmId or quantity"}), 400

        url = "https://marketplace-api.wildberries.ru/api/v3/stocks/{WAREHOUSE_ID}"
        headers = {
            "Authorization": WB_API_TOKEN,
            "Content-Type": "application/json"
        }
        payload = {
            "stocks": [
                {
                    "sku": int(nmId),
                    "amount": int(quantity),
                    "warehouseId": WAREHOUSE_ID
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
