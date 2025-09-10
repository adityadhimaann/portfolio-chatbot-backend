import PyPDF2
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

class Document:
    def __init__(self, page_content: str, metadata: Dict = None):
        self.page_content = page_content
        self.metadata = metadata or {}

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
        # Use a lightweight embedding model
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_store = None
        self.documents = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks with improved logic for resume content"""
        if not text:
            return []
        
        # Clean and normalize the text
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())  # Remove extra whitespace
        
        # For resume content, try to identify sections first
        chunks = []
        
        # Define section patterns that are common in resumes
        section_patterns = [
            'EDUCATION', 'EXPERIENCE', 'SKILLS', 'PROJECTS', 'CERTIFICATIONS', 
            'CONTACT', 'TECHNICAL SKILLS', 'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE',
            'ACADEMIC', 'ACHIEVEMENTS', 'AWARDS'
        ]
        
        # Try to split by sections first
        sections_found = []
        
        for pattern in section_patterns:
            pos = text.upper().find(pattern)
            if pos != -1:
                sections_found.append((pos, pattern))
        
        # Sort sections by position
        sections_found.sort()
        
        if sections_found:
            # Create chunks based on sections
            for i, (pos, _) in enumerate(sections_found):
                if i == 0:
                    # Add content before first section as introduction
                    if pos > 0:
                        intro_chunk = text[:pos].strip()
                        if len(intro_chunk) > 50:  # Only add if substantial
                            chunks.append(intro_chunk)
                
                # Get section content
                start_pos = pos
                end_pos = sections_found[i + 1][0] if i + 1 < len(sections_found) else len(text)
                section_content = text[start_pos:end_pos].strip()
                
                # If section is too long, split it further
                if len(section_content) > self.chunk_size:
                    # Split by sentences or logical breaks
                    sub_chunks = self._split_large_section(section_content, self.chunk_size)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(section_content)
        else:
            # Fallback to sentence-based chunking if no sections found
            sentences = text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Add period back if it doesn't end with punctuation
                if not sentence.endswith(('.', '!', '?', ':')):
                    sentence += '.'
                
                # Check if adding this sentence would exceed chunk size
                if len(current_chunk + ' ' + sentence) <= self.chunk_size:
                    current_chunk = current_chunk + ' ' + sentence if current_chunk else sentence
                else:
                    # Save current chunk and start new one
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
            
            # Add the last chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
        
        # Filter out very short chunks and ensure minimum content quality
        filtered_chunks = []
        for chunk in chunks:
            # Remove chunks that are too short or contain only formatting
            if len(chunk.strip()) > 30 and not chunk.strip().isupper():
                filtered_chunks.append(chunk.strip())
        
        return filtered_chunks if filtered_chunks else [text[:self.chunk_size]]  # Fallback
    
    def _split_large_section(self, section: str, max_size: int) -> List[str]:
        """Split large sections while preserving context"""
        chunks = []
        
        # Try to split by logical breaks first
        logical_breaks = [' | ', ' • ', ' - ', '. ', ', ']
        
        for break_char in logical_breaks:
            if break_char in section:
                parts = section.split(break_char)
                current_chunk = ""
                
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    
                    # Re-add the break character except for the last part
                    part_with_break = part + break_char
                    
                    if len(current_chunk + part_with_break) <= max_size:
                        current_chunk += part_with_break
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip(break_char))
                        current_chunk = part_with_break
                
                if current_chunk:
                    chunks.append(current_chunk.rstrip(break_char))
                
                return chunks
        
        # If no logical breaks found, split by size
        words = section.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk + ' ' + word) <= max_size:
                current_chunk = current_chunk + ' ' + word if current_chunk else word
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = word
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def process_pdfs_from_directory(self, directory_path: str) -> List[Document]:
        """Process all PDF files in a directory"""
        documents = []
        
        for filename in os.listdir(directory_path):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory_path, filename)
                print(f"Processing: {filename}")
                
                text = self.extract_text_from_pdf(pdf_path)
                if text.strip():
                    # Split text into chunks
                    chunks = self.split_text(text)
                    
                    # Create Document objects
                    for i, chunk in enumerate(chunks):
                        doc = Document(
                            page_content=chunk,
                            metadata={
                                "source": filename,
                                "chunk": i,
                                "total_chunks": len(chunks)
                            }
                        )
                        documents.append(doc)
        
        return documents
    
    def create_vector_store(self, documents: List[Document]):
        """Create vector store from documents"""
        if not documents:
            raise ValueError("No documents provided")
        
        self.documents = documents
        
        # Extract text content
        texts = [doc.page_content for doc in documents]
        
        # Create embeddings
        print("Creating embeddings...")
        embeddings = self.embeddings.encode(texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.vector_store = faiss.IndexFlatL2(dimension)
        self.vector_store.add(embeddings.astype('float32'))
        
        print(f"Created vector store with {len(documents)} documents")
    
    def save_vector_store(self, path: str):
        """Save vector store to disk"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        os.makedirs(path, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.vector_store, os.path.join(path, "index.faiss"))
        
        # Save documents
        with open(os.path.join(path, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)
        
        print(f"Vector store saved to {path}")
    
    def load_vector_store(self, path: str):
        """Load vector store from disk"""
        index_path = os.path.join(path, "index.faiss")
        docs_path = os.path.join(path, "documents.pkl")
        
        if not os.path.exists(index_path) or not os.path.exists(docs_path):
            raise ValueError(f"Vector store not found at {path}")
        
        # Load FAISS index
        self.vector_store = faiss.read_index(index_path)
        
        # Load documents
        with open(docs_path, "rb") as f:
            self.documents = pickle.load(f)
        
        print(f"Vector store loaded from {path}")
    
    def search_similar_documents(self, query: str, k: int = 3) -> List[Document]:
        """Search for similar documents"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        
        # Encode query
        query_embedding = self.embeddings.encode([query])
        
        # Search
        distances, indices = self.vector_store.search(query_embedding.astype('float32'), k)
        
        # Return documents
        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])
        
        return results
