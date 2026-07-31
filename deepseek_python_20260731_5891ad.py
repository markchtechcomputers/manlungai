# ai_chatbot.py - AI Assistant for Manlung Shop
import openai
import os
from dotenv import load_dotenv

# Load your API key from a .env file (security best practice)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ManlungAIAssistant:
    def __init__(self):
        # This is the "brain" of your AI
        self.system_prompt = """
        You are "Manlung AI" - the official AI assistant for Adict Manlung's music store.
        
        About Adict Manlung:
        - Kenyan hip-hop artist
        - Independent artist from Nairobi
        - Known for raw, unfiltered storytelling
        - Popular songs: "Money Bag", "Cold", "Still Outside", "Black Africa", "Unfinished Business", "My Gee"
        - Has performed at Flock Show with Tashlie Brands
        
        Store Information:
        - Digital singles: KSh 199-499
        - Physical CDs: KSh 1,299-1,499
        - Merch: Hoodies (KSh 4,999), Tees (KSh 2,999), Caps (KSh 3,000)
        - Payment: Paystack
        - Shipping: DHL Worldwide
        
        Your job:
        1. Be friendly and helpful
        2. Answer questions about Adict Manlung's music, shows, and merchandise
        3. Provide accurate pricing information
        4. Direct fans to the website for purchases
        5. Never share sensitive business information
        
        Keep responses concise, energetic, and aligned with hip-hop culture.
        """
        
        self.conversation_history = []
    
    def ask(self, user_question):
        """Process user question and return AI response"""
        # Add user question to history
        self.conversation_history.append({
            "role": "user", 
            "content": user_question
        })
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history
        
        # Get response from AI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            return f"Sorry, I'm having trouble right now. Please email adictmanlung@gmail.com for help. Error: {str(e)}"
    
    def clear_history(self):
        """Start a fresh conversation"""
        self.conversation_history = []


# Quick test - run this file directly to test
if __name__ == "__main__":
    assistant = ManlungAIAssistant()
    
    print("=== Manlung AI Assistant Test ===")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Fan asks: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        response = assistant.ask(question)
        print(f"Manlung AI: {response}\n")