import os
import json
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

app = Flask(__name__)

# Берём из переменных окружения
WB_TOKEN       = os.getenv("WB_TOKEN")
WAREHOUSE_ID   = int(os.getenv("WB_WAREHOUSE_ID"))
WB_API_HOST    = "https://suppliers-api.wildberries.ru"
WB_STOCKS_PATH = "/content/v1/stocks"

@app.route("/update_stock", methods=["POST"])
def update_stock():
    try:
        body = request.get_json(force=True)
        sku      = body.get("nmId")
        quantity = body.get("quantity")
        if not sku or quantity is None:
            return jsonify(error="nmId and quantity required"), 400

        payload = {
            "stocks": [
                {
                    "sku":      str(sku),
                    "whId":     WAREHOUSE_ID,
                    "quantity": int(quantity)
                }
            ]
        }
        headers = {
            "Authorization": WB_TOKEN,
            "Content-Type":  "application/json"
        }
        resp = requests.post(
            WB_API_HOST + WB_STOCKS_PATH,
            headers=headers,
            json=payload,
            timeout=10
        )
        # Пробрасываем ответ Wildberries напрямую
        return (resp.text, resp.status_code, {"Content-Type": "application/json"})

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    # порт берётся из Render (или 10000 по умолчанию)
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
