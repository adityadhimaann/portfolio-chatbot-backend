#!/usr/bin/env python3
"""
Retrain the chatbot with improved text processing
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.pdf_processor import PDFProcessor

def retrain_chatbot():
    """Retrain the chatbot with improved processing"""
    print("Starting improved chatbot retraining...")
    
    # Initialize PDF processor
    processor = PDFProcessor()
    
    # Process the PDF
    pdf_path = "../data/aditya-kumar.pdf"
    print(f"Processing PDF: {pdf_path}")
    
    # Extract text
    text = processor.extract_text_from_pdf(pdf_path)
    print(f"Extracted text length: {len(text)} characters")
    
    if not text.strip():
        print("Error: No text extracted from PDF")
        return False
    
    print("\n--- Raw extracted text (first 500 chars) ---")
    print(text[:500])
    print("...\n")
    
    # Split into improved chunks
    chunks = processor.split_text(text)
    print(f"Created {len(chunks)} improved chunks")
    
    # Display chunk details
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Length: {len(chunk)} characters")
        print(f"Content: {chunk[:200]}...")
    
    # Create documents
    documents = []
    for i, chunk in enumerate(chunks):
        from app.utils.pdf_processor import Document
        doc = Document(
            page_content=chunk,
            metadata={
                "source": "aditya-kumar.pdf",
                "chunk": i,
                "total_chunks": len(chunks)
            }
        )
        documents.append(doc)
    
    # Create vector store
    print(f"\nCreating vector store with {len(documents)} documents...")
    processor.create_vector_store(documents)
    
    # Save the vector store
    processor.save_vector_store("../data/vector_store.pkl")
    print("Vector store saved successfully!")
    
    # Test search functionality
    print("\n--- Testing search functionality ---")
    test_queries = [
        "What is Aditya's education?",
        "What are his technical skills?",
        "Tell me about his projects",
        "What is his contact information?",
        "What certifications does he have?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = processor.search_similar_documents(query, k=2)
        for j, result in enumerate(results):
            if hasattr(result, 'page_content'):
                print(f"Result {j+1}: {result.page_content[:150]}...")
            else:
                print(f"Result {j+1}: {str(result)[:150]}...")
    
    print("\n✅ Chatbot retraining completed successfully!")
    return True

if __name__ == "__main__":
    success = retrain_chatbot()
    if not success:
        sys.exit(1)
