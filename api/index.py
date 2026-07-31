from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Check if OpenAI API key is set
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    You are "Manlung AI" - official assistant for Adict Manlung.
                    About: Kenyan hip-hop artist, independent from Nairobi.
                    Songs: Money Bag, Cold, Still Outside, Black Africa, Unfinished Business, My Gee.
                    Merch: Hoodies (KSh 4,999), Tees (KSh 2,999), Caps (KSh 3,000).
                    Digital singles: KSh 199-499, Physical CDs: KSh 1,299-1,499.
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
