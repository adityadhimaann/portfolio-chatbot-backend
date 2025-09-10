import json
import os
from typing import List, Dict, Optional
from .pdf_processor import PDFProcessor

class EnhancedChatbotEngine:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.structured_data = None
        self.load_structured_data()
        
        self.system_prompt = """
        You are AdiDev, an intelligent chatbot assistant trained specifically on Aditya Kumar's resume and professional profile.
        You have access to structured, detailed information about Aditya's background, skills, projects, and achievements.
        Provide accurate, detailed, and helpful responses based on the structured data available.
        Be conversational, professional, and highlight Aditya's strengths and accomplishments.
        """
    
    def load_structured_data(self):
        """Load structured resume data"""
        try:
            # Try multiple possible paths
            possible_paths = [
                "../data/structured_resume_data.json",
                "../../data/structured_resume_data.json", 
                "/Users/aditya/Chatbot/data/structured_resume_data.json",
                "data/structured_resume_data.json"
            ]
            
            data_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    data_path = path
                    break
            
            if data_path:
                with open(data_path, 'r') as f:
                    self.structured_data = json.load(f)
                print("✅ Loaded structured resume data")
            else:
                print("⚠️ Structured data file not found")
        except Exception as e:
            print(f"❌ Error loading structured data: {e}")
    
    def initialize_from_pdfs(self, pdf_directory: str, vector_store_path: str = None):
        """Initialize chatbot with PDF data"""
        documents = self.pdf_processor.process_pdfs_from_directory(pdf_directory)
        
        if not documents:
            raise ValueError("No documents found in the directory")
        
        self.pdf_processor.create_vector_store(documents)
        
        if vector_store_path:
            self.pdf_processor.save_vector_store(vector_store_path)
        
        print(f"Initialized with {len(documents)} document chunks")
    
    def load_existing_knowledge(self, vector_store_path: str):
        """Load existing vector store"""
        self.pdf_processor.load_vector_store(vector_store_path)
        print("Loaded existing knowledge base")
    
    def generate_response(self, user_message: str, chat_history: List[Dict] = None) -> str:
        """Generate enhanced response using structured data and context"""
        try:
            # First try to answer using structured data
            structured_response = self._generate_structured_response(user_message)
            if structured_response:
                return structured_response
            
            # Fallback to vector search
            context = self.get_relevant_context(user_message)
            return self._generate_fallback_response(user_message, context)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your question right now. Could you please try rephrasing it?"
    
    def _generate_structured_response(self, user_message: str) -> Optional[str]:
        """Generate response using structured data"""
        if not self.structured_data:
            return None
        
        user_lower = user_message.lower().strip()
        
        # Exact matches for suggestion buttons
        if user_lower == "who is aditya?":
            return self._format_personal_info()
        elif user_lower == "technical skills":
            return self._format_all_skills()
        elif user_lower == "projects":
            return self._format_projects_info()
        elif user_lower == "contact info":
            return self._format_contact_info()
        
        # Contact information - Check this first for better matching
        if any(word in user_lower for word in ['contact', 'email', 'phone', 'reach', 'address']):
            return self._format_contact_info()
        
        # Projects questions
        if any(word in user_lower for word in ['project', 'portfolio', 'built', 'developed', 'created', 'application']):
            return self._format_projects_info()
        
        # Personal/About questions (but not if asking about projects)
        if any(word in user_lower for word in ['who', 'about', 'profile', 'summary']) and not any(word in user_lower for word in ['project', 'skill', 'education', 'experience']):
            return self._format_personal_info()
        
        # Generic "tell me about" - try to be more specific
        if 'tell me about' in user_lower:
            if any(word in user_lower for word in ['project', 'built', 'developed']):
                return self._format_projects_info()
            elif any(word in user_lower for word in ['skill', 'technology']):
                return self._format_all_skills()
            elif any(word in user_lower for word in ['education', 'study']):
                return self._format_education_info()
            else:
                return self._format_personal_info()
        
        # Education questions
        if any(word in user_lower for word in ['education', 'degree', 'university', 'college', 'study', 'academic']):
            return self._format_education_info()
        
        # Skills questions
        if any(word in user_lower for word in ['skill', 'technology', 'programming', 'language', 'tool', 'tech stack']):
            if any(word in user_lower for word in ['technical', 'programming', 'coding', 'language']):
                return self._format_technical_skills()
            elif any(word in user_lower for word in ['tool', 'ai', 'platform']):
                return self._format_tools_skills()
            else:
                return self._format_all_skills()
        
        # Experience questions
        if any(word in user_lower for word in ['experience', 'work', 'job', 'employment', 'career']):
            return self._format_experience_info()
        
        # Certifications questions
        if any(word in user_lower for word in ['certification', 'certified', 'certificate', 'credential']):
            return self._format_certifications_info()
        
        # Achievements questions
        if any(word in user_lower for word in ['achievement', 'award', 'hackathon', 'winner', 'accomplishment']):
            return self._format_achievements_info()
        
        # Specific technology questions
        if any(tech in user_lower for tech in ['react', 'javascript', 'python', 'html', 'css', 'mongodb', 'mysql']):
            return self._format_technology_specific_response(user_message)
        
        return None
    
    def _format_personal_info(self) -> str:
        """Format personal information response"""
        personal = self.structured_data.get('personal', {})
        education = self.structured_data.get('education', {})
        
        response = f"Hi! I'm {personal.get('name', 'Aditya Kumar')}, a passionate {personal.get('role', 'Web Developer')} "
        response += f"based in {personal.get('location', 'Lucknow, Uttar Pradesh')}. "
        
        if education.get('degree'):
            response += f"I'm currently pursuing {education['degree']} at {education.get('university', 'Lovely Professional University')} "
            response += f"({education.get('years', '2023-2027')}). "
        
        response += "I have extensive experience in web development, AI tools, and have achieved notable success in hackathons. "
        response += "I'm passionate about building innovative digital solutions and have worked on various projects ranging from responsive websites to AI applications."
        
        return response
    
    def _format_contact_info(self) -> str:
        """Format contact information response"""
        contact = self.structured_data.get('contact', {})
        personal = self.structured_data.get('personal', {})
        
        response = f"You can reach {personal.get('name', 'Aditya')} through the following contact information:\n\n"
        
        if contact.get('email'):
            response += f"📧 Email: {contact['email']}\n"
        if contact.get('phone'):
            response += f"📱 Phone: {contact['phone']}\n"
        if personal.get('location'):
            response += f"📍 Location: {personal['location']}\n"
        
        response += "\nFeel free to reach out for collaboration opportunities, project discussions, or any inquiries!"
        
        return response
    
    def _format_education_info(self) -> str:
        """Format education information response"""
        education = self.structured_data.get('education', {})
        
        if not education:
            return "I don't have specific education information available."
        
        response = "🎓 Education Background:\n\n"
        response += f"Degree: {education.get('degree', 'Bachelor of Technology in Computer Science and Engineering')}\n"
        response += f"University: {education.get('university', 'Lovely Professional University')}\n"
        response += f"Duration: {education.get('years', '2023 - 2027')}\n\n"
        response += "Currently studying Computer Science and Engineering with focus on web development, AI technologies, and software engineering principles."
        
        return response
    
    def _format_technical_skills(self) -> str:
        """Format technical skills response"""
        skills = self.structured_data.get('skills', {})
        technical = skills.get('technical', [])
        
        if not technical:
            return "I don't have specific technical skills information available."
        
        response = "💻 Technical Skills:\n\n"
        
        # Categorize skills
        frontend = [skill for skill in technical if skill.lower() in ['html', 'css', 'javascript', 'react', 'jquery', 'tailwind css']]
        backend = [skill for skill in technical if skill.lower() in ['python', 'java', 'node.js']]
        database = [skill for skill in technical if skill.lower() in ['mongodb', 'mysql']]
        
        if frontend:
            response += f"🎨 Frontend: {', '.join(frontend)}\n"
        if backend:
            response += f"⚙️ Backend: {', '.join(backend)}\n"
        if database:
            response += f"🗄️ Database: {', '.join(database)}\n"
        
        response += f"\n📋 All Technical Skills: {', '.join(technical)}"
        
        return response
    
    def _format_tools_skills(self) -> str:
        """Format tools and platforms response"""
        skills = self.structured_data.get('skills', {})
        tools = skills.get('tools', [])
        
        if not tools:
            return "I don't have specific tools information available."
        
        response = "🛠️ AI Tools & Platforms:\n\n"
        
        # Categorize tools
        ai_tools = [tool for tool in tools if 'ai' in tool.lower() or tool.lower() in ['chatgpt', 'claude', 'gemini', 'automl', 'openai']]
        cloud_tools = [tool for tool in tools if tool.lower() in ['aws', 'oracle cloud']]
        
        if ai_tools:
            response += f"🤖 AI Tools: {', '.join(ai_tools)}\n"
        if cloud_tools:
            response += f"☁️ Cloud Platforms: {', '.join(cloud_tools)}\n"
        
        response += f"\n📋 All Tools: {', '.join(tools)}"
        
        return response
    
    def _format_all_skills(self) -> str:
        """Format all skills response"""
        skills = self.structured_data.get('skills', {})
        
        response = "💼 Complete Skills Overview:\n\n"
        
        if skills.get('technical'):
            response += f"💻 Technical Skills: {', '.join(skills['technical'])}\n\n"
        
        if skills.get('tools'):
            response += f"🛠️ AI Tools & Platforms: {', '.join(skills['tools'])}\n\n"
        
        if skills.get('soft'):
            response += f"🎯 Soft Skills: {', '.join(skills['soft'])}\n\n"
        
        response += "This diverse skill set enables me to work on full-stack development projects, integrate AI capabilities, and manage projects effectively."
        
        return response
    
    def _format_experience_info(self) -> str:
        """Format experience information response"""
        experience = self.structured_data.get('experience', [])
        
        if not experience:
            return "I don't have specific experience information available."
        
        response = "🏆 Professional Experience:\n\n"
        
        for exp in experience:
            response += f"📝 {exp.get('type', 'Experience')}\n"
            response += f"Description: {exp.get('description', 'N/A')}\n"
            
            if exp.get('highlights'):
                response += "Key Highlights:\n"
                for highlight in exp['highlights']:
                    response += f"  • {highlight}\n"
            response += "\n"
        
        return response
    
    def _format_projects_info(self) -> str:
        """Format projects information response"""
        projects = self.structured_data.get('projects', [])
        
        if not projects:
            return "I don't have specific project information available."
        
        response = "🚀 Featured Projects:\n\n"
        
        for i, project in enumerate(projects, 1):
            response += f"{i}. **{project.get('name', 'Unnamed Project')}**\n"
            response += f"   Description: {project.get('description', 'N/A')}\n"
            
            if project.get('technologies'):
                response += f"   Technologies: {', '.join(project['technologies'])}\n"
            
            if project.get('achievement'):
                response += f"   🏅 Achievement: {project['achievement']}\n"
            
            if project.get('features'):
                response += f"   Features: {', '.join(project['features'])}\n"
            
            response += "\n"
        
        return response
    
    def _format_certifications_info(self) -> str:
        """Format certifications response"""
        certifications = self.structured_data.get('certifications', [])
        
        if not certifications:
            return "I don't have specific certification information available."
        
        response = "🏅 Professional Certifications:\n\n"
        
        for cert in certifications:
            response += f"✅ {cert}\n"
        
        response += "\nThese certifications demonstrate expertise in cloud technologies and professional project management."
        
        return response
    
    def _format_achievements_info(self) -> str:
        """Format achievements response"""
        achievements = self.structured_data.get('achievements', [])
        
        if not achievements:
            return "I don't have specific achievement information available."
        
        response = "🎯 Notable Achievements:\n\n"
        
        for achievement in achievements:
            response += f"🏆 {achievement}\n"
        
        response += "\nThese achievements showcase consistent performance in competitive environments and technical innovation."
        
        return response
    
    def _format_technology_specific_response(self, user_message: str) -> str:
        """Format technology-specific response"""
        user_lower = user_message.lower()
        skills = self.structured_data.get('skills', {})
        projects = self.structured_data.get('projects', [])
        
        # Find relevant technology
        tech_mentioned = None
        for tech in skills.get('technical', []):
            if tech.lower() in user_lower:
                tech_mentioned = tech
                break
        
        if not tech_mentioned:
            return None
        
        response = f"💻 Regarding {tech_mentioned}:\n\n"
        response += f"Yes, I have experience with {tech_mentioned}. "
        
        # Find relevant projects
        relevant_projects = []
        for project in projects:
            if project.get('technologies'):
                for tech in project['technologies']:
                    if tech.lower() == tech_mentioned.lower() or tech_mentioned.lower() in tech.lower():
                        relevant_projects.append(project)
                        break
        
        if relevant_projects:
            response += f"I've used {tech_mentioned} in the following projects:\n\n"
            for project in relevant_projects:
                response += f"🚀 {project.get('name', 'Project')}: {project.get('description', 'N/A')}\n"
        
        return response
    
    def get_relevant_context(self, query: str, max_chunks: int = 3) -> str:
        """Get relevant context from documents"""
        try:
            similar_docs = self.pdf_processor.search_similar_documents(query, k=max_chunks)
            context = ""
            
            for doc in similar_docs:
                # Just add the content without source metadata
                context += f"{doc.page_content}\n\n"
            
            return context.strip()
        except Exception as e:
            print(f"Error getting context: {e}")
            return ""
    
    def _generate_fallback_response(self, user_message: str, context: str) -> str:
        """Generate fallback response using context"""
        if context.strip():
            # Clean up the context and provide a more natural response
            cleaned_context = context.replace('\n', ' ').strip()
            if len(cleaned_context) > 400:
                cleaned_context = cleaned_context[:400] + "..."
            
            return f"Here's what I found: {cleaned_context}"
        else:
            return "I don't have specific information about that. Could you please ask about Aditya's education, skills, projects, experience, or contact information?"
