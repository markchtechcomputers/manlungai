# chat_web.py - Web interface for your AI chatbot
from flask import Flask, request, jsonify, render_template_string
from ai_chatbot import ManlungAIAssistant
import os

app = Flask(__name__)
assistant = ManlungAIAssistant()

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Manlung AI Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 20px;
            border-bottom: 2px solid #e94560;
        }
        .chat-box {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            margin: 20px 0;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
        }
        .user-message {
            background: #e94560;
            text-align: right;
            margin-left: 20%;
        }
        .ai-message {
            background: #1a1a3e;
            margin-right: 20%;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 15px 30px;
            background: #e94560;
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #c73652;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎤 Manlung AI Assistant</h1>
        <p>Ask me anything about Adict Manlung's music, merch, and shows!</p>
    </div>
    
    <div class="chat-box" id="chatBox">
        <div class="message ai-message">
            🤖 Hi! I'm Manlung AI. Ask me about Adict Manlung's music, merch, or upcoming shows!
        </div>
    </div>
    
    <div class="input-area">
        <input type="text" id="questionInput" placeholder="Ask a question..." onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('questionInput');
            const chatBox = document.getElementById('chatBox');
            const question = input.value.trim();
            
            if (!question) return;
            
            // Add user message
            chatBox.innerHTML += `<div class="message user-message">🙋 ${question}</div>`;
            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
            
            // Show loading
            chatBox.innerHTML += `<div class="message ai-message">🤔 Thinking...</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: question})
                });
                const data = await response.json();
                
                // Remove loading message
                const messages = chatBox.getElementsByClassName('ai-message');
                if (messages.length > 0 && messages[messages.length-1].textContent === '🤔 Thinking...') {
                    messages[messages.length-1].remove();
                }
                
                // Add AI response
                chatBox.innerHTML += `<div class="message ai-message">🤖 ${data.answer}</div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                
            } catch (error) {
                chatBox.innerHTML += `<div class="message ai-message">❌ Error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    answer = assistant.ask(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)