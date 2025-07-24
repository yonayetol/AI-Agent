import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify 
from utils import send_my_letter, fetch_news, get_weather, shutdown_pc, take_screenshot, get_current_time, restart_pc, lock_pc
from db_interface import get_user_preference, add_preference, delete_preference

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY2"))

model = genai.GenerativeModel(
    'gemini-2.0-flash',
    tools=[fetch_news, send_my_letter, get_user_preference, add_preference, delete_preference, get_weather, shutdown_pc, take_screenshot, get_current_time, restart_pc, lock_pc],
    system_instruction="""You are All in One, a helpful and friendly AI assistant.
When a user asks about current events, recent statements, or anything that sounds like a news query, you must use the `fetch_news` tool.
Do not apologize for not having real-time information. Instead, use the `fetch_news` tool to find the information.

When a user expresses a desire to remove a preference, use the `delete_preference` tool.
This tool can handle both exact preference names and general keywords.
For example, if a user says "I'm not interested in Ethiopians anymore," you should call `delete_preference` with the keyword 'ethiopians'.

For all other requests, respond as a helpful assistant."""
)

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/ai", methods=["POST"])
def ai():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(user_message)

        return jsonify({"ai": response.text})
    except Exception as e: 
        print(f"An error occurred during AI processing: {e}") 
        return jsonify({"ai": f"Sorry, an error occurred: {str(e)}"})

if __name__ == "__main__": 
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)