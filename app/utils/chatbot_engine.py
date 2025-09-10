import openai
from typing import List, Dict
from .pdf_processor import PDFProcessor
import os
from dotenv import load_dotenv

load_dotenv()

class ChatbotEngine:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        self.system_prompt = """
        You are AdiDev, a helpful chatbot assistant trained on specific documents. 
        Your responses should be based primarily on the provided context from the documents.
        If you cannot find relevant information in the context, politely say so and ask for clarification.
        Be friendly, helpful, and accurate in your responses.
        """
    
    def initialize_from_pdfs(self, pdf_directory: str, vector_store_path: str = None):
        """Initialize chatbot with PDF data"""
        # Process PDFs
        documents = self.pdf_processor.process_pdfs_from_directory(pdf_directory)
        
        if not documents:
            raise ValueError("No documents found in the directory")
        
        # Create vector store
        self.pdf_processor.create_vector_store(documents)
        
        # Save vector store if path provided
        if vector_store_path:
            self.pdf_processor.save_vector_store(vector_store_path)
        
        print(f"Initialized with {len(documents)} document chunks")
    
    def load_existing_knowledge(self, vector_store_path: str):
        """Load existing vector store"""
        self.pdf_processor.load_vector_store(vector_store_path)
        print("Loaded existing knowledge base")
    
    def get_relevant_context(self, query: str, max_chunks: int = 3) -> str:
        """Get relevant context from documents"""
        try:
            similar_docs = self.pdf_processor.search_similar_documents(query, k=max_chunks)
            context = ""
            
            for doc in similar_docs:
                context += f"Source: {doc.metadata.get('source', 'Unknown')}\n"
                context += f"Content: {doc.page_content}\n\n"
            
            return context
        except Exception as e:
            print(f"Error getting context: {e}")
            return ""
    
    def generate_response(self, user_message: str, chat_history: List[Dict] = None) -> str:
        """Generate response using OpenAI API or fallback"""
        try:
            # Get relevant context
            context = self.get_relevant_context(user_message)
            
            # Try OpenAI first if API key is available
            if self.openai_api_key:
                return self._generate_openai_response(user_message, context, chat_history)
            else:
                return self._generate_fallback_response(user_message, context)
                    
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while processing your request. Please try again."
    
    def _generate_openai_response(self, user_message: str, context: str, chat_history: List[Dict] = None) -> str:
        """Generate response using OpenAI API"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            # Prepare messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add chat history if provided
            if chat_history:
                messages.extend(chat_history[-10:])  # Last 10 messages for context
            
            # Add current query with context
            prompt = f"""
            Context from documents:
            {context}
            
            User question: {user_message}
            
            Please answer based on the provided context. If the context doesn't contain relevant information, 
            politely say that you don't have that information in your knowledge base.
            """
            
            messages.append({"role": "user", "content": prompt})
            
            # Get response from OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return self._generate_fallback_response(user_message, context)
    
    def _generate_fallback_response(self, user_message: str, context: str) -> str:
        """Generate intelligent response without OpenAI"""
        if context.strip():
            # Extract all content lines
            lines = context.split('\n')
            content_lines = [line.replace('Content:', '').strip() for line in lines if line.startswith('Content:')]
            
            if content_lines:
                # Combine all relevant content for better analysis
                full_content = " ".join(content_lines)
                
                # Analyze user question for better response
                user_lower = user_message.lower()
                
                # Smart keyword matching for better responses
                if any(word in user_lower for word in ['experience', 'work', 'job', 'career', 'employment', 'position']):
                    response = self._extract_experience_info(full_content)
                elif any(word in user_lower for word in ['skill', 'technology', 'programming', 'language', 'tool']):
                    response = self._extract_skills_info(full_content)
                elif any(word in user_lower for word in ['education', 'degree', 'university', 'college', 'study', 'academic']):
                    response = self._extract_education_info(full_content)
                elif any(word in user_lower for word in ['project', 'portfolio', 'built', 'developed', 'created']):
                    response = self._extract_projects_info(full_content)
                elif any(word in user_lower for word in ['contact', 'email', 'phone', 'address', 'linkedin']):
                    response = self._extract_contact_info(full_content)
                elif any(word in user_lower for word in ['about', 'who', 'summary', 'overview', 'profile']):
                    response = self._extract_profile_info(full_content)
                elif any(word in user_lower for word in ['certification', 'certified', 'certificate']):
                    response = self._extract_certifications_info(full_content)
                else:
                    # General search - return most relevant content
                    response = self._extract_general_info(full_content, user_message)
                
                return response if response else "I found some information but couldn't extract the specific details you're looking for. Could you please rephrase your question?"
            else:
                return "I found some relevant information but had trouble processing it. Could you please rephrase your question?"
        else:
            return "I don't have specific information about that in my knowledge base. Could you please provide more details or try asking about: experience, skills, education, projects, contact information, or certifications?"
    
    def _extract_experience_info(self, content: str) -> str:
        """Extract work experience information"""
        # Look for experience-related keywords and context
        experience_indicators = ['hackathon', 'achieved', 'position', 'building', 'website', 'volunteer']
        found_info = []
        
        for indicator in experience_indicators:
            if indicator.lower() in content.lower():
                # Find the context around this indicator
                start = max(0, content.lower().find(indicator.lower()) - 50)
                end = min(len(content), content.lower().find(indicator.lower()) + 100)
                context = content[start:end].strip()
                if context and context not in found_info:
                    found_info.append(context)
        
        if found_info:
            return f"Based on the resume, here's Aditya's experience: {' '.join(found_info[:2])}"
        
        # Fallback - look for any project or achievement info
        if 'hackathon' in content.lower():
            return "Aditya has participated in hackathons and achieved notable positions, including building responsive websites."
        
        return "I found some experience information but need more context to provide specific details."
    
    def _extract_skills_info(self, content: str) -> str:
        """Extract technical skills information"""
        skills_section = ""
        
        # Look for technical skills section
        if 'technical skills' in content.lower():
            start = content.lower().find('technical skills')
            skills_section = content[start:start+200]
        
        # Extract AI tools and platforms
        ai_tools = []
        if 'aws' in content.lower(): ai_tools.append('AWS')
        if 'canva ai' in content.lower(): ai_tools.append('Canva AI')
        if 'cursor ai' in content.lower(): ai_tools.append('Cursor AI')
        if 'chatgpt' in content.lower(): ai_tools.append('ChatGPT')
        if 'claude' in content.lower(): ai_tools.append('Claude')
        if 'gemini' in content.lower(): ai_tools.append('Gemini')
        if 'automl' in content.lower(): ai_tools.append('AutoML')
        if 'openai' in content.lower(): ai_tools.append('OpenAI API')
        
        response_parts = []
        
        if skills_section:
            response_parts.append(f"Technical Skills: {skills_section}")
        
        if ai_tools:
            response_parts.append(f"AI Tools & Platforms: {', '.join(ai_tools)}")
        
        if response_parts:
            return f"Aditya's skills include: {' | '.join(response_parts)}"
        
        return "I found some skills information but need more context to provide specific details."
    
    def _extract_education_info(self, content: str) -> str:
        """Extract education information"""
        education_info = []
        
        # Look for degree information
        if 'bachelor of technology' in content.lower():
            education_info.append('Bachelor of Technology in Computer Science and Engineering')
        
        if 'lovely professional' in content.lower():
            education_info.append('Lovely Professional University')
        
        # Look for years
        if '2023 - 2027' in content:
            education_info.append('(2023 - 2027)')
        
        if education_info:
            return f"Education: {' '.join(education_info)}"
        
        return "I found some education information but need more context to provide specific details."
    
    def _extract_projects_info(self, content: str) -> str:
        """Extract projects information"""
        projects = []
        
        # Look for specific projects
        if 'fitness-and-sports website' in content.lower():
            projects.append('Responsive Fitness-and-Sports website (Top 10 position in CodeBlocks Hackathon 2024)')
        
        if 'stress' in content.lower() and 'meditation' in content.lower():
            projects.append('Stress reduction application using OpenAI API with guided exercises and meditation')
        
        if projects:
            return f"Aditya's projects include: {'; '.join(projects)}"
        
        return "I found some project information but need more context to provide specific details."
    
    def _extract_contact_info(self, content: str) -> str:
        """Extract contact information"""
        contact_info = []
        
        # Look for phone number
        if '+91 6306580926' in content:
            contact_info.append('Phone: +91 6306580926')
        
        # Look for email
        if 'dhimanaditya56@gmail.com' in content:
            contact_info.append('Email: dhimanaditya56@gmail.com')
        
        # Look for location
        if 'lucknow' in content.lower():
            contact_info.append('Location: Lucknow, Uttar Pradesh')
        
        if contact_info:
            return f"Contact Information: {' | '.join(contact_info)}"
        
        return "I found some contact information but need more context to provide specific details."
    
    def _extract_certifications_info(self, content: str) -> str:
        """Extract certifications information"""
        certifications = []
        
        if 'oracle cloud infrastructure' in content.lower():
            certifications.append('Oracle Cloud Infrastructure 2025 Certified')
        
        if 'project management' in content.lower():
            certifications.append('Project Management Professionalism')
        
        if certifications:
            return f"Certifications: {', '.join(certifications)}"
        
        return "I found some certification information but need more context to provide specific details."
    
    def _extract_profile_info(self, content: str) -> str:
        """Extract general profile information"""
        profile_elements = []
        
        # Extract key highlights
        if 'computer science' in content.lower():
            profile_elements.append('Computer Science and Engineering student')
        
        if 'hackathon' in content.lower():
            profile_elements.append('Hackathon participant with top achievements')
        
        if 'oracle cloud' in content.lower():
            profile_elements.append('Oracle Cloud certified professional')
        
        if profile_elements:
            return f"Aditya Kumar is a {', '.join(profile_elements)}. He has experience with AI tools, web development, and has achieved notable positions in hackathons."
        
        return "I found some profile information but need more context to provide specific details."
    
    def _extract_general_info(self, content: str, query: str) -> str:
        """Extract general information based on query"""
        # Return the most relevant content chunk
        if len(content) > 300:
            return f"Based on the available information: {content[:300]}..."
        else:
            return f"Based on the available information: {content}"
