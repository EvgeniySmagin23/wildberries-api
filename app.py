from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Либо храните в ENV (через Render Environment → Variables → Add), либо впишите прямо сюда:
WB_TOKEN       = os.getenv("WB_TOKEN", "<eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwNDE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MjMyMjcxOSwiaWQiOiIwMTk2YTZjNi0wZDU5LTdlMTEtOWQ5MS0zOTIzOWRlM2QzZDYiLCJpaWQiOjEwNzMzOTUwNywib2lkIjoxMjE2OTE2LCJzIjo3OTM0LCJzaWQiOiI2ZDJlNmJhYS0zM2IxLTRmMTctODQyMC0yYTJkODNlOTliMGQiLCJ0IjpmYWxzZSwidWlkIjoxMDczMzk1MDd9.WcBlF6-OSo2ezXwfpo_sSLeGHiO-tcKXVNExoyoAO1A-cGGJlu1AY1efoeaKRd2DsD0C78QdoZBKBtr2BPjKrw>")        # Bearer-токен
WAREHOUSE_ID   = os.getenv("WB_WAREHOUSE_ID", "717599")      # Ваш ID склада

@app.route("/")
def index():
    return "✅ Wildberries API is running"

@app.route("/update_stock", methods=["POST"])
def update_stock():
    data = request.get_json()
    nmId     = data.get("nmId")
    quantity = data.get("quantity", 1)

    # здесь sku = supplierArticle или штрихкод, но можно использовать nmId, 
    # если ваш подходящий API это поддерживает
    payload = {
        "stocks": [
            {
                "sku": str(nmId),
                "amount": int(quantity)
            }
        ]
    }

    url = f"https://marketplace-api.wildberries.ru/api/v3/stocks/{WAREHOUSE_ID}"
    headers = {
        "Authorization": f"Bearer {WB_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.put(url, json=payload, headers=headers, timeout=10)
        return jsonify({
            "ok": resp.status_code in (200, 204),
            "status": resp.status_code,
            "body": resp.text
        }), (200 if resp.status_code in (200,204) else 400)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
