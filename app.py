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

    payload = [{
        "nmId": nmId,
        "quantity": quantity
    }]
    headers = {
        "Authorization": "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwNDE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MjMyMjcxOSwiaWQiOiIwMTk2YTZjNi0wZDU5LTdlMTEtOWQ5MS0zOTIzOWRlM2QzZDYiLCJpaWQiOjEwNzMzOTUwNywib2lkIjoxMjE2OTE2LCJzIjo3OTM0LCJzaWQiOiI2ZDJlNmJhYS0zM2IxLTRmMTctODQyMC0yYTJkODNlOTliMGQiLCJ0IjpmYWxzZSwidWlkIjoxMDczMzk1MDd9.WcBlF6-OSo2ezXwfpo_sSLeGHiO-tcKXVNExoyoAO1A-cGGJlu1AY1efoeaKRd2DsD0C78QdoZBKBtr2BPjKrw",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            "https://api-seller.wildberries.ru/content/v1/stocks",
            json=payload,
            headers=headers
        )
        return jsonify({"status": response.status_code, "data": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
