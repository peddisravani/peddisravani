from flask import Flask, request, jsonify
from ml.recommend import get_recommendations
from ml.preprocess import clean_text
from database import PRODUCTS

app = Flask(__name__)

@app.route("/api/health")
def health():
    return {"status": "ok"}

@app.route("/api/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "")
    query = clean_text(query)
    results = [p for p in PRODUCTS if query in p["title"].lower()]
    return jsonify(results)

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    product_id = data.get("product_id")
    return jsonify(get_recommendations(product_id))

if __name__ == "__main__":
    app.run()
