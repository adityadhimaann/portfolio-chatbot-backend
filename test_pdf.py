#!/usr/bin/env python3

import sys
import os
sys.path.append('/Users/aditya/Chatbot/backend/venv_new/lib/python3.13/site-packages')
sys.path.append('/Users/aditya/Chatbot/backend')

from app.utils.pdf_processor import PDFProcessor
import pickle

def test_pdf_content():
    print("Testing PDF content extraction...")
    
    # Load the processed documents
    with open('/Users/aditya/Chatbot/backend/vector_store/documents.pkl', 'rb') as f:
        documents = pickle.load(f)
    
    print(f"\nTotal documents processed: {len(documents)}")
    
    for i, doc in enumerate(documents):
        print(f"\n--- Document Chunk {i+1} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content (first 200 chars): {doc.page_content[:200]}...")
        print(f"Full content length: {len(doc.page_content)}")
        print(f"Metadata: {doc.metadata}")
    
    # Test search functionality
    processor = PDFProcessor()
    processor.load_vector_store('/Users/aditya/Chatbot/backend/vector_store')
    
    test_queries = [
        "What is Aditya's experience?",
        "What skills does he have?",
        "What is his education?",
        "Tell me about his projects",
        "What is his contact information?"
    ]
    
    print("\n" + "="*50)
    print("TESTING SEARCH FUNCTIONALITY")
    print("="*50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = processor.search_similar_documents(query, k=2)
        for j, result in enumerate(results):
            print(f"Result {j+1}: {result.page_content[:150]}...")

if __name__ == "__main__":
    test_pdf_content()
