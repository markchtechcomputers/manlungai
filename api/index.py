# api/index.py - Main Vercel serverless function
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Manlung AI</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: white;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
                text-align: center;
            }
            h1 { font-size: 48px; color: #e94560; }
            .feature { 
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
            }
            input, button {
                padding: 15px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin: 5px;
            }
            input { width: 60%; background: #1a1a3e; color: white; }
            button { background: #e94560; color: white; cursor: pointer; }
            button:hover { background: #c73652; }
            #response { 
                margin-top: 20px; 
                padding: 20px;
                background: rgba(255,255,255,0.05);
                border-radius: 10px;
                min-height: 50px;
            }
        </style>
    </head>
    <body>
        <h1>🎤 Manlung AI</h1>
        <p>Ask me about Adict Manlung's music, merch, and shows!</p>
        
        <div class="feature">
            <p style="font-size:14px; color:#aaa;">Powered by OpenAI</p>
            <input type="text" id="question" placeholder="e.g., What songs does Adict Manlung have?" />
            <button onclick="askQuestion()">Ask</button>
        </div>
        
        <div id="response">💡 Ask me a question above!</div>
        
        <div style="margin-top: 30px; font-size: 14px; color: #666;">
            🔥 Songs: Money Bag | Cold | Still Outside | Black Africa | Unfinished Business | My Gee
        </div>

        <script>
            async function askQuestion() {
                const question = document.getElementById('question').value;
                const responseDiv = document.getElementById('response');
                
                if (!question) {
                    responseDiv.innerHTML = '⚠️ Please type a question!';
                    return;
                }
                
                responseDiv.innerHTML = '🤔 Thinking...';
                
                try {
                    const res = await fetch('/api/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: question })
                    });
                    const data = await res.json();
                    responseDiv.innerHTML = '🤖 ' + data.answer;
                } catch (error) {
                    responseDiv.innerHTML = '❌ Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are "Manlung AI" - the official AI assistant for Adict Manlung.
                    
                    About: Kenyan hip-hop artist, independent from Nairobi.
                    Popular songs: Money Bag, Cold, Still Outside, Black Africa, 
                    Unfinished Business, My Gee.
                    
                    Merch: Hoodies (KSh 4,999), Tees (KSh 2,999), Caps (KSh 3,000),
                    Digital singles (KSh 199-499), Physical CDs (KSh 1,299-1,499).
                    
                    Be helpful, concise, and energetic.
                    """
                },
                {"role": "user", "content": question}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel requires this
app = app
