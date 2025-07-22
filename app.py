import google.generativeai as genai
import os
from flask import Flask, render_template, request, jsonify

# Import the Python functions that the AI will be able to call
from utils import send_my_letter, fetch_news
from db_interface import get_user_preference, add_preference, delete_preference

app = Flask(__name__)

# Load the API key from the environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY3"))

# Create the model and pass the functions directly as tools.
# The SDK automatically handles schema generation, function execution,
# and sending the results back to the model to generate a final response.
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    tools=[fetch_news, send_my_letter, get_user_preference, add_preference, delete_preference],
    system_instruction="""You are a helpful and friendly AI assistant.
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
        # Start a chat session with automatic function calling enabled.
        # This allows for a stateful conversation where the model can make multiple
        # function calls if needed to fulfill a single user request.
        chat = model.start_chat(enable_automatic_function_calling=True)
        
        # Send the user's message and get the final response.
        # The SDK handles the entire loop of:
        # 1. Model -> function_call
        # 2. SDK -> executes function
        # 3. SDK -> sends result to Model
        # 4. Model -> final text response
        response = chat.send_message(user_message)

        # The final, user-facing text from the model.
        return jsonify({"ai": response.text})
    except Exception as e:
        # Log the full error for easier debugging
        print(f"An error occurred during AI processing: {e}")
        # Provide a user-friendly error message
        return jsonify({"ai": f"Sorry, an error occurred: {str(e)}"})

if __name__ == "__main__":
    # Set debug=False in a production environment
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug_mode)