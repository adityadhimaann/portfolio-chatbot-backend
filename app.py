from flask import Flask, request, jsonify
from flask_cors import CORS
from app.utils.enhanced_chatbot_engine import EnhancedChatbotEngine
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all origins in production
CORS(app, origins=["http://localhost:3000", 
                  "http://localhost:3001", 
                  "http://localhost:3004",
                  "https://portfolionew.vercel.app",
                  "https://adityadhimaanns-projects.vercel.app"\]\)

# Initialize enhanced chatbot
chatbot = EnhancedChatbotEngine()

# Chat history storage (in production, use a database)
chat_sessions = {}

@app.route('/')
def home():
    return jsonify({
        "message": "AdiDev Chatbot API is running!",
        "status": "active"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get or create chat history for session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_history = chat_sessions[session_id]
        
        # Generate response
        response = chatbot.generate_response(user_message, chat_history)
        
        # Update chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": response})
        
        # Keep only last 20 messages to manage memory
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        chat_sessions[session_id] = chat_history
        
        return jsonify({
            "response": response,
            "session_id": session_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "AdiDev Chatbot API"
    })

# For Vercel serverless deployment
def serverless_app(request_data):
    with app.test_request_context(
        path=request_data.get('path', '/'),
        method=request_data.get('method', 'GET'),
        headers=request_data.get('headers', {}),
        json=request_data.get('body', {})
    ):
        try:
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }

# This is used for local development
if __name__ == '__main__':
    # Automatically load knowledge base if it exists
    try:
        chatbot.load_existing_knowledge()
        print("Loaded existing knowledge base")
    except Exception as e:
        print(f"Warning: Could not auto-initialize chatbot: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
