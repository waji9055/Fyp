from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")  # Needed for session

# Prompt prefix
system_prompt = """
You are a helpful assistant for tourists visiting northern areas. You can answer questions about various hotels, tourist spots, best routes, nearby attractions, and any general information that a tourist may need. Please provide a response in a friendly and informative manner.
"""

# Function to generate Gemini content
def generate_gemini_content(chat_history):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(chat_history)
    return response.text.strip()

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form['question']

    if not user_query:
        return jsonify({'error': 'Please enter a question.'}), 400

    # Get chat history from session
    if 'history' not in session:
        session['history'] = []

    session['history'].append({"role": "user", "text": user_query})

    # Construct conversation string
    conversation = system_prompt + "\n"
    for msg in session['history']:
        role = "You" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['text']}\n"

    try:
        bot_reply = generate_gemini_content(conversation)
        session['history'].append({"role": "assistant", "text": bot_reply})
        session.modified = True  # Mark session as changed
        return jsonify({'response': bot_reply, 'history': session['history']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Optional: route to reset chat
@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify({'status': 'Chat history reset.'})

if __name__ == '__main__':
    app.run(debug=True)
