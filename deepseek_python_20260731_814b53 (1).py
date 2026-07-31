from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Manlung AI</title></head>
    <body>
        <h1>🎤 Manlung AI Assistant</h1>
        <p>Send POST requests to /api/ask with {'question': 'your text'}</p>
    </body>
    </html>
    """

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Manlung AI, assistant for Adict Manlung's music site."},
                {"role": "user", "content": question}
            ]
        )
        return jsonify({'answer': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel needs this
app = app