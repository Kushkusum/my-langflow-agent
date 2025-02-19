from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("ASTRA_API_KEY")
ASTRA_API_URL = os.getenv("ASTRA_API_URL")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {
            "input_value": user_input,
            "output_type": "chat",
            "input_type": "chat"
        }

        response = requests.post(ASTRA_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            bot_reply = response.json().get("output", "Error processing request")
        else:
            bot_reply = f"Error: {response.status_code}, {response.text}"

        return render_template("index.html", user_input=user_input, bot_reply=bot_reply)

    return render_template("index.html", user_input="", bot_reply="")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Bind to 0.0.0.0 for Render
