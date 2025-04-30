import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define Flask app
app = Flask(__name__)

# Prompt template for tourist hotel guidance
prompt = """
You are a helpful assistant for tourists visiting northern areas. You can answer questions about various hotels, tourist spots, best routes, nearby attractions, and any general information that a tourist may need. Please provide a response in a friendly and informative manner. 
The user may ask anything related to tourist hotels or travel. Here’s the user’s question:
"""

# Function to generate content using Google Gemini API
def generate_gemini_content(user_input, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the correct model name for Gemini (e.g., "gemini-pro")
    response = model.generate_content(prompt + user_input)
    return response.text.strip()

# Route to display the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user query and generate a response
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form['question']
    if user_query:
        try:
            # Generate the response using Gemini API
            response = generate_gemini_content(user_query, prompt)
            return jsonify({'response': response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Please enter a question.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
