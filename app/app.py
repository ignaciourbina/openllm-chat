import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Construct the path to the .env file in the parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)

# --- Logger Setup ---
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'app.log'
# Rotating file handler: 5 MB per file, keep 5 backup files
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
# --- End Logger Setup ---


# Initialize the OpenAI client to connect to the OpenLLM server
client = OpenAI(
    base_url="http://localhost:3000/v1",
    api_key=os.environ.get("OPENAI_API_KEY", "na")  # Use a dummy key if not set
)

@app.route('/')
def index():
    app.logger.info("Serving index page.")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        app.logger.warning("Chat request with no message.")
        return jsonify({"error": "No message provided"}), 400

    app.logger.info(f"Received message: {user_message}")

    try:
        # Send a request to the model
        completion = client.chat.completions.create(
            model="dolly-v2",  # Specify the model you are serving
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        response = completion.choices[0].message.content
        app.logger.info(f"Model response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error during chat completion: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.logger.info(f"Starting Flask server on port {port}.")
    app.run(debug=True, port=port)
