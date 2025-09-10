"""
Initialize the AdiDev chatbot with sample data for testing
"""
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def create_sample_pdf_content():
    """Create a simple text file as sample content if no PDFs exist"""
    data_dir = Path(__file__).parent.parent / 'data'
    sample_file = data_dir / 'sample_content.txt'
    
    if not any(data_dir.glob('*.pdf')) and not sample_file.exists():
        sample_content = """
AdiDev Chatbot Knowledge Base

About AdiDev:
AdiDev is an intelligent chatbot assistant designed to help users by answering questions based on custom PDF documents. This chatbot combines the power of modern AI with your personal knowledge base.

Key Features:
1. PDF Document Processing - Automatically extracts and processes text from PDF files
2. AI-Powered Responses - Uses advanced language models for intelligent responses
3. Vector Search - Finds relevant information quickly using embeddings
4. Session Management - Maintains conversation context
5. Modern UI - Beautiful, responsive chat interface

Technical Stack:
- Backend: Python, Flask, LangChain, FAISS, OpenAI
- Frontend: React, TypeScript, Styled Components
- AI: OpenAI GPT models, HuggingFace embeddings

How to Use:
1. Add your PDF documents to the data directory
2. Configure your OpenAI API key (optional but recommended)
3. Start the application
4. Ask questions about your documents

Example Questions:
- "What is AdiDev?"
- "What are the key features?"
- "How do I use this chatbot?"
- "What technologies are used?"

For best results, add your own PDF documents and ask specific questions about their content.
        """
        
        with open(sample_file, 'w') as f:
            f.write(sample_content)
        
        print(f"Created sample content file: {sample_file}")
        return str(sample_file)
    
    return None

def main():
    print("🚀 Initializing AdiDev Chatbot...")
    
    try:
        from app.utils.chatbot_engine import ChatbotEngine
        
        # Create sample content if no PDFs exist
        sample_file = create_sample_pdf_content()
        if sample_file:
            print("📄 No PDF files found. Created sample content for testing.")
        
        # Initialize chatbot
        chatbot = ChatbotEngine()
        
        # Try to load existing vector store or create new one
        vector_store_path = os.path.join(os.path.dirname(__file__), 'vector_store')
        pdf_directory = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        if os.path.exists(vector_store_path):
            print("📚 Loading existing knowledge base...")
            chatbot.load_existing_knowledge(vector_store_path)
        else:
            print("📚 Creating new knowledge base from documents...")
            chatbot.initialize_from_pdfs(pdf_directory, vector_store_path)
        
        print("✅ AdiDev Chatbot initialized successfully!")
        print("🌐 You can now start the application with: python app.py")
        
    except ImportError as e:
        print(f"❌ Missing dependencies. Please install requirements first:")
        print(f"   pip install -r requirements.txt")
        print(f"   Error: {e}")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        print("📝 Make sure you have:")
        print("   1. Installed all requirements (pip install -r requirements.txt)")
        print("   2. Added PDF files to the data directory (optional for testing)")
        print("   3. Set up your OpenAI API key in .env file (optional)")

if __name__ == "__main__":
    main()
