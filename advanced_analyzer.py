#!/usr/bin/env python3
"""
Advanced PDF Content Analyzer and Enhancer
"""

import sys
import os
import re
from typing import Dict, List, Tuple

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.pdf_processor import PDFProcessor

class AdvancedContentAnalyzer:
    def __init__(self):
        self.processor = PDFProcessor()
        self.structured_data = {}
        
    def extract_and_analyze(self, pdf_path: str) -> Dict:
        """Extract and analyze PDF content with advanced parsing"""
        print("🔍 Starting advanced content analysis...")
        
        # Extract raw text
        raw_text = self.processor.extract_text_from_pdf(pdf_path)
        print(f"📄 Extracted {len(raw_text)} characters from PDF")
        
        # Clean and normalize text
        cleaned_text = self._clean_text(raw_text)
        print(f"🧹 Cleaned text: {len(cleaned_text)} characters")
        
        # Extract structured information
        structured_info = self._extract_structured_info(cleaned_text)
        
        # Display analysis
        self._display_analysis(structured_info)
        
        return structured_info
    
    def _clean_text(self, text: str) -> str:
        """Advanced text cleaning"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common PDF extraction issues
        text = text.replace('|', ' ')
        text = text.replace('•', ' • ')
        
        # Fix phone number formatting
        text = re.sub(r'(\+91\s?)(\d{10})', r'+91 \2', text)
        
        # Fix email formatting
        text = re.sub(r'(\S+@\S+\.\S+)', r' \1 ', text)
        
        return text.strip()
    
    def _extract_structured_info(self, text: str) -> Dict:
        """Extract structured information from text"""
        info = {
            'personal': {},
            'education': {},
            'skills': {'technical': [], 'soft': [], 'tools': []},
            'experience': [],
            'projects': [],
            'certifications': [],
            'achievements': [],
            'contact': {}
        }
        
        # Extract personal information
        info['personal'] = self._extract_personal_info(text)
        
        # Extract contact information
        info['contact'] = self._extract_contact_info(text)
        
        # Extract education
        info['education'] = self._extract_education_info(text)
        
        # Extract skills
        info['skills'] = self._extract_skills_info(text)
        
        # Extract experience
        info['experience'] = self._extract_experience_info(text)
        
        # Extract projects
        info['projects'] = self._extract_projects_info(text)
        
        # Extract certifications
        info['certifications'] = self._extract_certifications_info(text)
        
        # Extract achievements
        info['achievements'] = self._extract_achievements_info(text)
        
        return info
    
    def _extract_personal_info(self, text: str) -> Dict:
        """Extract personal information"""
        personal = {}
        
        # Extract name
        name_match = re.search(r'ADITYA KUMAR', text, re.IGNORECASE)
        if name_match:
            personal['name'] = 'Aditya Kumar'
        
        # Extract title/role
        role_patterns = ['WEB DEVELOPER', 'DEVELOPER', 'SOFTWARE ENGINEER']
        for pattern in role_patterns:
            if pattern.lower() in text.lower():
                personal['role'] = pattern.title()
                break
        
        # Extract location
        location_match = re.search(r'Lucknow\s*,?\s*Uttar Pradesh', text, re.IGNORECASE)
        if location_match:
            personal['location'] = 'Lucknow, Uttar Pradesh'
        
        return personal
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Extract phone
        phone_match = re.search(r'\+91\s?(\d{10})', text)
        if phone_match:
            contact['phone'] = f"+91 {phone_match.group(1)}"
        
        # Extract email
        email_match = re.search(r'(\S+@\S+\.\S+)', text)
        if email_match:
            contact['email'] = email_match.group(1)
        
        return contact
    
    def _extract_education_info(self, text: str) -> Dict:
        """Extract education information"""
        education = {}
        
        # Extract degree
        degree_match = re.search(r'Bachelor\s+of\s+Technology.*?Computer\s+Science.*?Engineering', text, re.IGNORECASE)
        if degree_match:
            education['degree'] = 'Bachelor of Technology in Computer Science and Engineering'
        
        # Extract university
        university_match = re.search(r'Lovely Professional University', text, re.IGNORECASE)
        if university_match:
            education['university'] = 'Lovely Professional University'
        
        # Extract years
        year_match = re.search(r'(2023\s*-\s*2027)', text)
        if year_match:
            education['years'] = '2023 - 2027'
        
        return education
    
    def _extract_skills_info(self, text: str) -> Dict:
        """Extract skills information"""
        skills = {'technical': [], 'soft': [], 'tools': []}
        
        # Technical skills
        tech_skills = [
            'HTML', 'CSS', 'JavaScript', 'React', 'ReactJS', 'jQuery',
            'Tailwind CSS', 'Python', 'Java', 'Node.js', 'Express.js',
            'MongoDB', 'MySQL', 'Git', 'GitHub'
        ]
        
        for skill in tech_skills:
            if skill.lower() in text.lower():
                skills['technical'].append(skill)
        
        # AI Tools
        ai_tools = [
            'AWS', 'Canva AI', 'Cursor AI', 'ChatGPT', 'Claude', 'Gemini',
            'AutoML', 'OpenAI', 'Oracle Cloud'
        ]
        
        for tool in ai_tools:
            if tool.lower() in text.lower():
                skills['tools'].append(tool)
        
        # Soft skills
        soft_skills = [
            'Project Management', 'Effective Communication', 'Critical Thinking',
            'Problem Solving', 'Leadership', 'Team Collaboration'
        ]
        
        for skill in soft_skills:
            if skill.lower() in text.lower():
                skills['soft'].append(skill)
        
        return skills
    
    def _extract_experience_info(self, text: str) -> List[Dict]:
        """Extract experience information"""
        experience = []
        
        # Look for hackathon experience
        if 'hackathon' in text.lower():
            exp = {
                'type': 'Hackathon Participation',
                'description': 'Participated in multiple hackathons with notable achievements',
                'achievements': []
            }
            
            if 'top 10' in text.lower():
                exp['achievements'].append('Top 10 position in CodeBlocks Hackathon 2024')
            
            if 'finalist' in text.lower():
                exp['achievements'].append('Finalist in FinArva AI Hackathon')
                exp['achievements'].append('National Level Hackathon Finalist')
            
            experience.append(exp)
        
        return experience
    
    def _extract_projects_info(self, text: str) -> List[Dict]:
        """Extract projects information"""
        projects = []
        
        # Fitness website project
        if 'fitness' in text.lower() and 'website' in text.lower():
            projects.append({
                'name': 'Responsive Fitness-and-Sports Website',
                'description': 'Built a responsive fitness and sports website',
                'achievement': 'Top 10 position in CodeBlocks Hackathon 2024',
                'technologies': ['HTML', 'CSS', 'JavaScript']
            })
        
        # Stress reduction app
        if 'stress' in text.lower() and 'meditation' in text.lower():
            projects.append({
                'name': 'Stress Reduction Application',
                'description': 'Developed stress reduction application using OpenAI API with guided exercises and meditation',
                'technologies': ['OpenAI API', 'Python'],
                'features': ['Guided exercises', 'Meditation']
            })
        
        # BhasaVitt project
        if 'bhasavitt' in text.lower():
            projects.append({
                'name': 'BhasaVitt',
                'description': 'Multilingual AI model developed for Gromo-AWS-Sarvam AI challenge',
                'achievement': 'National Level Hackathon Finalist (25,000+ participants)',
                'technologies': ['AI/ML', 'Multilingual Processing']
            })
        
        return projects
    
    def _extract_certifications_info(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        if 'oracle cloud infrastructure' in text.lower():
            certifications.append('Oracle Cloud Infrastructure 2025 Certified')
        
        if 'project management professionalism' in text.lower():
            certifications.append('Project Management Professionalism')
        
        return certifications
    
    def _extract_achievements_info(self, text: str) -> List[str]:
        """Extract achievements"""
        achievements = []
        
        if 'top 10' in text.lower() and 'hackathon' in text.lower():
            achievements.append('Top 10 position in CodeBlocks Hackathon 2024')
        
        if 'finalist' in text.lower():
            achievements.append('FinArva AI Hackathon Finalist')
            achievements.append('National Level Hackathon Finalist in Gromo-AWS-Sarvam AI challenge')
        
        if '25,000' in text:
            achievements.append('Competed among 25,000+ participants in national hackathon')
        
        return achievements
    
    def _display_analysis(self, info: Dict):
        """Display the analysis results"""
        print("\n" + "="*50)
        print("📊 ADVANCED CONTENT ANALYSIS RESULTS")
        print("="*50)
        
        print(f"\n👤 Personal Information:")
        for key, value in info['personal'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n📞 Contact Information:")
        for key, value in info['contact'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n🎓 Education:")
        for key, value in info['education'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n💼 Skills:")
        for category, skills in info['skills'].items():
            if skills:
                print(f"   {category.title()}: {', '.join(skills)}")
        
        print(f"\n🏆 Experience:")
        for exp in info['experience']:
            print(f"   Type: {exp.get('type', 'N/A')}")
            print(f"   Description: {exp.get('description', 'N/A')}")
            if exp.get('achievements'):
                print(f"   Achievements: {', '.join(exp['achievements'])}")
        
        print(f"\n🚀 Projects:")
        for project in info['projects']:
            print(f"   Name: {project.get('name', 'N/A')}")
            print(f"   Description: {project.get('description', 'N/A')}")
            if project.get('achievement'):
                print(f"   Achievement: {project['achievement']}")
            if project.get('technologies'):
                print(f"   Technologies: {', '.join(project['technologies'])}")
            print()
        
        print(f"\n🏅 Certifications:")
        for cert in info['certifications']:
            print(f"   • {cert}")
        
        print(f"\n🎯 Achievements:")
        for achievement in info['achievements']:
            print(f"   • {achievement}")
        
        print("\n" + "="*50)

def main():
    analyzer = AdvancedContentAnalyzer()
    pdf_path = "../data/aditya-kumar.pdf"
    
    try:
        structured_info = analyzer.extract_and_analyze(pdf_path)
        
        # Save structured data for use in enhanced chatbot
        import json
        with open("../data/structured_resume_data.json", "w") as f:
            json.dump(structured_info, f, indent=2)
        
        print("✅ Analysis complete! Structured data saved to structured_resume_data.json")
        return structured_info
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

if __name__ == "__main__":
    main()
