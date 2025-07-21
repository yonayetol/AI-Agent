from flask import Flask, render_template, request, jsonify
from utils import send_my_letter, fetch_news
from db_interface import get_user_preference, add_preference, delete_preference

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query")
    user_id = data.get("user_id")
    if query:
        news = fetch_news(query)
        return jsonify({"type": "news", "results": news})
    elif user_id:
        prefs = get_user_preference(user_id)
        return jsonify({"type": "preferences", "results": prefs})
    else:
        return jsonify({"error": "No query or user_id provided"}), 400

@app.route("/email", methods=["POST"])
def email():
    data = request.json
    email = data.get("email")
    message = data.get("message")
    if email and message:
        send_my_letter(email, message)
        return jsonify({"type": "email", "message": "Email sent successfully!"})
    else:
        return jsonify({"error": "Email and message required"}), 400

@app.route("/preferences/add", methods=["POST"])
def add_pref():
    data = request.json
    user_id = data.get("user_id")
    topic = data.get("topic")
    if user_id and topic:
        add_preference(user_id, topic)
        return jsonify({"message": "Preference added"})
    else:
        return jsonify({"error": "user_id and topic required"}), 400

@app.route("/preferences/delete", methods=["POST"])
def del_pref():
    data = request.json
    topic = data.get("topic")
    if topic:
        delete_preference(topic)
        return jsonify({"message": "Preference deleted"})
    else:
        return jsonify({"error": "topic required"}), 400

@app.route("/preferences/get", methods=["POST"])
def get_pref():
    data = request.json
    user_id = data.get("user_id")
    if user_id:
        prefs = get_user_preference(user_id)
        return jsonify({"preferences": prefs})
    else:
        return jsonify({"error": "user_id required"}), 400

if __name__ == "__main__":
    app.run(debug=True) 