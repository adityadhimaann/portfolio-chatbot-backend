# AdiDev Portfolio Chatbot Backend

Advanced chatbot backend with PDF processing, vector storage, and AI-powered responses.

## 🚀 Features

- **AI-Powered Chat**: Intelligent responses about Aditya's portfolio
- **PDF Processing**: Can process and learn from PDF documents
- **Vector Storage**: FAISS-based document embeddings
- **CORS Enabled**: Ready for portfolio website integration
- **Multiple Endpoints**: Various API endpoints for different functionalities

## 📁 Structure

```
/
├── api/
│   ├── index.py              # Main API endpoint
│   ├── chat/
│   │   └── index.py          # Advanced chat functionality
│   ├── requirements.txt      # Python dependencies
│   └── test.py              # Test endpoint
├── app/
│   └── utils/
│       ├── chatbot_engine.py
│       ├── enhanced_chatbot_engine.py
│       └── pdf_processor.py
├── vector_store/            # FAISS vector storage
├── vercel.json              # Vercel deployment config
└── app.py                   # Main Flask application
```

## 🔧 API Endpoints

- `GET /api` - Health check and API information
- `POST /api/chat` - Advanced chat with AI responses
- `GET /api/test` - Test endpoint

## 🌐 Deployment

Deployed on Vercel with Python serverless functions.

## 🔗 Integration

This backend is designed to integrate with the AdiDev portfolio website at www.adidev.works
